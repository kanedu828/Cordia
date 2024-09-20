from cordia.model.shop_item import ShopItem, ShopItemType
from cordia.util.decorators import only_command_invoker
from cordia.util.text_format_util import display_gold
from cordia.view.pages.page import Page
from cordia.data.shop_items import shop_item_data
import discord
from discord.ui import View, Button, Select


class ShopPage(Page):
    def __init__(self, cordia_service, discord_id, page_number=0):
        super().__init__(cordia_service, discord_id)
        self.page_number = page_number
        self.items_per_page = 10
        self.items = []

    async def render(self, interaction: discord.Interaction):
        armory = await self.cordia_service.get_armory(self.discord_id)
        armory = {a.name for a in armory}
        shop_items = shop_item_data.copy()
        shop_items = {k: v for k, v in shop_items.items() if k not in armory}
        self.items = [
            list(shop_items.keys())[i : i + self.items_per_page]
            for i in range(0, len(shop_items.keys()), self.items_per_page)
        ]

        embed = await self._create_shop_embed()
        view = self._create_view()

        await interaction.response.edit_message(embed=embed, view=view)

    async def _create_shop_embed(self):
        embed = discord.Embed(title="Shop", description="", color=discord.Color.gold())

        items_on_page: list[str] = self.items[self.page_number]

        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)

        embed.add_field(name=display_gold(player.gold), value="", inline=False)

        for i in items_on_page:
            si = shop_item_data[i]
            cost_text = "Cost: "
            cost_arr = []
            if si.gold_cost:
                cost_arr.append(f"{display_gold(si.gold_cost)}")
            if si.item_cost:
                cost_arr.append(f"{si.display_item_cost()}")
            cost_text += ", ".join(cost_arr)
            embed.add_field(
                name=si.get_item_data().display_item(), value=cost_text, inline=False
            )

        embed.set_footer(text=f"Page: {self.page_number + 1}/{len(self.items)}")

        return embed

    def _create_view(self):
        view = View(timeout=None)

        select_options = [
            discord.SelectOption(label=shop_item_data[i].get_item_data().name, value=i)
            for i in self.items[self.page_number]
        ]
        buy_item_select = Select(
            placeholder="Select item to buy",
            min_values=1,
            max_values=1,
            options=select_options,
            row=0,
        )
        buy_item_select.callback = self.buy_item_select_callback
        view.add_item(buy_item_select)

        # Add Back button to go back to the home page
        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=2)
        back_button.callback = self.back_button_callback
        view.add_item(back_button)

        prev_button = Button(label="⇦", style=discord.ButtonStyle.primary, row=1)
        prev_button.callback = self.previous_page_callback
        view.add_item(prev_button)
        # disabled if first page
        if self.page_number <= 0:
            prev_button.disabled = True

        next_button = Button(label="⇨", style=discord.ButtonStyle.primary, row=1)
        next_button.callback = self.next_page_callback
        view.add_item(next_button)
        # disable if last page
        if self.page_number >= len(self.items) - 1:
            next_button.disabled = True

        return view

    @only_command_invoker()
    async def buy_item_select_callback(self, interaction: discord.Interaction):
        si = shop_item_data[interaction.data["values"][0]]
        embed = discord.Embed(title="Purchase Item", color=discord.Color.red())
        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)

        # Check item cost if applicable
        if si.item_cost:
            player_item = await self.cordia_service.get_item(
                self.discord_id, si.item_cost[0]
            )
            if not player_item or player_item.count < si.item_cost[1]:
                embed.add_field(
                    name="You do not have enough resources to purchase this item.",
                    value="",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            # Deduct the item cost
            await self.cordia_service.insert_item(
                self.discord_id, si.item_cost[0], -si.item_cost[1]
            )

        # Check if player has enough gold
        if player.gold < si.gold_cost:
            embed.add_field(
                name="You do not have enough resources to purchase this item.", value=""
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Deduct gold
        await self.cordia_service.increment_gold(self.discord_id, -si.gold_cost)

        # Insert item or gear based on the shop item type
        if si.type == ShopItemType.GEAR:
            await self.cordia_service.insert_gear(self.discord_id, si.item_name)
        elif si.type == ShopItemType.ITEM:
            await self.cordia_service.insert_item(self.discord_id, si.item_name, 1)

        # Render the interaction and confirm the purchase
        await self.render(interaction)
        embed.add_field(
            name=f"You successfully purchased {si.get_item_data().display_item()}",
            value="",
        )
        embed.color = discord.Color.green()
        await interaction.followup.send(embed=embed, ephemeral=True)

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def previous_page_callback(self, interaction: discord.Interaction):
        # Decrease the page number and re-render the page
        self.page_number -= 1
        await self.render(interaction)

    @only_command_invoker()
    async def next_page_callback(self, interaction: discord.Interaction):
        # Increase the page number and re-render the page
        self.page_number += 1
        await self.render(interaction)
