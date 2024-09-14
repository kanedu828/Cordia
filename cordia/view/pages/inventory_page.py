import math
from cordia.util.decorators import only_command_invoker
from cordia.util.text_format_util import display_gold
from cordia.view.pages.page import Page
import discord
from discord.ui import View, Button


class InventoryPage(Page):
    def __init__(self, cordia_service, discord_id, page_number=0):
        super().__init__(cordia_service, discord_id)
        self.page_number = page_number
        self.items_per_page = 10
        self.items = []

    async def render(self, interaction: discord.Interaction):
        self.items = await self.cordia_service.get_inventory(self.discord_id)
        embed = await self._create_inventory_embed()
        view = self._create_view()

        await interaction.response.edit_message(embed=embed, view=view)

    async def _create_inventory_embed(self):
        embed = discord.Embed(
            title="Inventory", description="", color=discord.Color.blue()
        )

        start_index = self.page_number * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(self.items))
        items_on_page = self.items[start_index:end_index]

        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)

        embed.add_field(name=display_gold(player.gold), value="", inline=False)

        for i in items_on_page:
            embed.add_field(
                name=i.display_item(), value=i.get_item_data().description, inline=False
            )

        embed.set_footer(
            text=f"Page: {self.page_number + 1}/{math.ceil(len(self.items) / self.items_per_page)}"
        )

        return embed

    def _create_view(self):
        view = View(timeout=None)

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
        if (self.page_number + 1) * self.items_per_page >= len(self.items):
            next_button.disabled = True

        return view

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
