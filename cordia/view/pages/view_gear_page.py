from cordia.model.item import Item
from cordia.service.cordia_service import CordiaService
from cordia.util.decorators import only_command_invoker
from cordia.util.text_format_util import display_gold, get_stars_string
from cordia.view.pages.page import Page
from cordia.data.gear import gear_data
from cordia.data.items import item_data
import discord
from discord.ui import Button, View, Select


class ViewGearPage(Page):
    def __init__(
        self,
        cordia_service: CordiaService,
        discord_id: int,
        gear_id: int,
        is_all: bool,
        page: int = -1,
    ):
        super().__init__(cordia_service, discord_id)
        self.gear_id = gear_id
        self.page = page  # Used to get back to previous state in gear_page
        self.is_all = is_all  # Used to return to all armory if that is origin

    async def render(self, interaction: discord.Interaction):
        gi = await self.cordia_service.get_gear_by_id(self.gear_id)
        pg = await self.cordia_service.get_player_gear_by_gear_id(gi.id)
        player = await self.cordia_service.get_player_by_discord_id(gi.discord_id)
        gd = gi.get_gear_data()
        equipped_tag = "[Equipped] " if pg else ""

        cores = await self.cordia_service.get_cores_for_user(self.discord_id)

        embed = discord.Embed(
            title=f"{equipped_tag}lv.{gd.level} {gd.name}", color=discord.Color.blue()
        )

        embed.add_field(
            name="", value=get_stars_string(gi.stars, gd.get_max_stars()), inline=False
        )
        embed.add_field(
            name=f"**Type**: {gd.type.value.title()}", value="", inline=False
        )
        embed.add_field(name="", value=gi.get_main_stats_string())
        embed.add_field(name="", value=gi.get_secondary_stats_string())

        if gd.spell:
            embed.add_field(
                name=f"Spell: {gd.spell.name}",
                value=f"**Description:** {gd.spell.description}",
                inline=False,
            )
            embed.add_field(
                name="Spell Stats",
                value=gi.get_spell_stats_string(True),
                inline=False,
            )

        if gi.bonus:
            embed.add_field(
                name="Bonus Stats", value=gi.get_bonus_stats_string(), inline=False
            )

        upgrade_cost = gi.get_upgrade_cost()
        upgrade_item: Item = item_data[upgrade_cost["item"][0]]
        upgrade_cost_text = f"{display_gold(upgrade_cost['gold'])}"

        player_upgrade_item = await self.cordia_service.get_item(
            self.discord_id, upgrade_cost["item"][0]
        )

        if upgrade_cost["item"][1]:
            upgrade_cost_text += (
                f"\n**{upgrade_cost['item'][1]}** {upgrade_item.display_item()}"
            )
        if gi.stars >= gd.get_max_stars():
            upgrade_cost_text = "This gear is already fully upgraded!"
        embed.add_field(name="Upgrade Costs", value=upgrade_cost_text, inline=False)
        embed.add_field(
            name="Use Core Costs",
            value=f"{display_gold(gd.get_use_core_cost())}\n**1 Core**",
            inline=False,
        )
        your_resources_text = f"{display_gold(player.gold)}"
        if player_upgrade_item:
            your_resources_text += f"\n{player_upgrade_item.display_item()}"
        for c in cores:
            your_resources_text += f"\n{c.display_item()}"
        if not cores:
            your_resources_text += f"\nYou have no cores"
        embed.add_field(name="Your Resources", value=your_resources_text, inline=False)

        player_upgrade_item_count = 0
        if player_upgrade_item:
            player_upgrade_item_count = player_upgrade_item.count
        has_upgrade_cost = (
            player.gold >= upgrade_cost["gold"]
            and player_upgrade_item_count >= upgrade_cost["item"][1]
        )
        view = self._create_view(
            bool(pg),
            gi.stars >= gd.get_max_stars(),
            has_upgrade_cost,
        )

        cores = await self.cordia_service.get_cores_for_user(self.discord_id)
        if cores:
            options = [
                discord.SelectOption(
                    label=item_data[c.name].name, description="", value=c.name
                )
                for c in cores
            ]
            core_select = Select(
                placeholder="Select a core to use",
                min_values=1,
                max_values=1,
                options=options,
            )
            core_select.callback = self.core_select_callback
            view.add_item(core_select)
        await interaction.response.edit_message(embed=embed, view=view)

    def _create_view(
        self,
        equipped: bool,
        max_stars: bool = False,
        has_upgrade_gold=False,
    ):
        view = View(timeout=None)

        equip_button = Button(label="Equip", style=discord.ButtonStyle.blurple, row=1)
        equip_button.callback = self.equip_button_callback
        equip_button.disabled = equipped

        upgrade_button = Button(
            label="Upgrade", style=discord.ButtonStyle.blurple, row=1
        )
        upgrade_button.callback = self.upgrade_button_callback
        upgrade_button.disabled = max_stars or not has_upgrade_gold

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=2)
        back_button.callback = self.back_button_callback

        home_button = Button(label="Home", style=discord.ButtonStyle.grey, row=2)
        home_button.callback = self.home_button_callback

        view.add_item(equip_button)
        view.add_item(upgrade_button)
        view.add_item(back_button)
        view.add_item(home_button)

        return view

    @only_command_invoker()
    async def equip_button_callback(self, interaction: discord.Interaction):
        # Maybe worth reducing a db call by storing type and class var
        gi = await self.cordia_service.get_gear_by_id(self.gear_id)
        await self.cordia_service.equip_gear(
            self.discord_id, self.gear_id, gi.get_gear_data().type.value
        )
        await self.render(interaction)

    @only_command_invoker()
    async def core_select_callback(self, interaction: discord.Interaction):
        player = await self.cordia_service.get_player_by_discord_id(interaction.user.id)
        core_value = interaction.data["values"][0]
        gear = await self.cordia_service.get_gear_by_id(self.gear_id)
        use_core_cost = gear.get_gear_data().get_use_core_cost()
        embed = discord.Embed(
            title=f"Use Core",
        )
        if player.gold < use_core_cost:
            embed.color = discord.Color.red()
            embed.add_field(
                name="You do not have enough resources!",
                value=f"You need {use_core_cost - player.gold} more gold.",
                inline=False,
            )
            await self.render(interaction)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        bonus_str = gear.get_gear_data().get_bonus_string(core_value)
        await self.cordia_service.update_gear_bonus(self.gear_id, bonus_str)
        await self.cordia_service.insert_item(interaction.user.id, core_value, -1)
        await self.cordia_service.increment_gold(interaction.user.id, -use_core_cost)
        await self.render(interaction)

    @only_command_invoker()
    async def upgrade_button_callback(self, interaction: discord.Interaction):
        gi = await self.cordia_service.get_gear_by_id(self.gear_id)
        upgrade_cost = gi.get_upgrade_cost()["gold"]
        upgrade_item_cost = gi.get_upgrade_cost()["item"]
        embed = discord.Embed(title=f"Upgrade Gear", color=discord.Color.green())

        embed.add_field(
            name="You successfully upgraded your gear!",
            value=f"You have upgraded your **{gi.get_gear_data().name}** to **{gi.stars + 1} stars**!",
            inline=False,
        )
        await self.cordia_service.increment_gear_stars(self.gear_id, 1)
        await self.cordia_service.insert_item(
            self.discord_id, upgrade_item_cost[0], -upgrade_item_cost[1]
        )
        await self.cordia_service.increment_gold(interaction.user.id, -upgrade_cost)
        await self.render(interaction)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.gear_page import GearPage

        gear = await self.cordia_service.get_gear_by_id(self.gear_id)
        gear_page = await GearPage.create(
            self.cordia_service,
            self.discord_id,
            None if self.is_all else gear.get_gear_data().type,
        )
        if self.page >= 0:
            gear_page.armory_page = self.page
            await gear_page.render_armory(interaction)
        else:
            await gear_page.render(interaction)

    @only_command_invoker()
    async def home_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)
