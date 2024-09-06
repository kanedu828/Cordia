from cordia.service.cordia_service import CordiaService
from cordia.util.decorators import only_command_invoker
from cordia.view.pages.page import Page
from cordia.data.gear import gear_data
import discord
from discord.ui import Button, View

class ViewGearPage(Page):
    def __init__(self, cordia_service: CordiaService, discord_id: int, gear_id: int, page: int=-1):
        super().__init__(cordia_service, discord_id)
        self.gear_id = gear_id
        self.page = page # Used to get back to previous state in gear_page

    async def render(self, interaction: discord.Interaction):
        gi = await self.cordia_service.get_gear_by_id(self.gear_id)
        pg = await self.cordia_service.get_player_gear_by_gear_id(gi.id)
        equipped_tag = '[Equipped] ' if pg else ''
        view = self._create_view(bool(pg))

        gd = gear_data[gi.name]
        embed = discord.Embed(
            title=f"{equipped_tag}lv.{gd.level} {gd.name}",
            color=discord.Color.blue()
        )

        embed.add_field(name=f'**Type**: {gd.type.value.title()}', value='', inline=False)
        embed.add_field(name='', value=gi.get_main_stats_string())
        embed.add_field(name='', value=gi.get_secondary_stats_string())

        if gd.spell:
            embed.add_field(
                name=f'Spell: {gd.spell.name}',
                value=f'**Description:** {gd.spell.description}\n**Scaling Stat:** {gd.spell.scaling_stat.title()}\n**Scaling Multiplier**: x{gd.spell.scaling_multiplier}',
                inline=False)
            embed.add_field(name='Spell Stats', value=gd.spell.get_spell_stats_string(), inline=False)

        await interaction.response.edit_message(embed=embed, view=view)

    def _create_view(self, equipped: bool):
        view = View(timeout=None)

        equip_button = Button(label="Equip", style=discord.ButtonStyle.blurple, row=1)
        equip_button.callback = self.equip_button_callback
        equip_button.disabled = equipped

        upgrade_button = Button(label="Upgrade", style=discord.ButtonStyle.blurple, row=1)
        upgrade_button.callback = self.upgrade_button_callback

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
        await self.cordia_service.equip_gear(self.discord_id, self.gear_id, gi.get_gear_data().type.value)
        await self.render(interaction)

    @only_command_invoker()
    async def upgrade_button_callback(self, interaction: discord.Interaction):
        pass

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.gear_page import GearPage
        gear = await self.cordia_service.get_gear_by_id(self.gear_id)
        gear_page = await GearPage.create(self.cordia_service, self.discord_id, gear_data[gear.name].type)
        if self.page >= 0:
            gear_page.armory_page = self.page
            await gear_page.render_armory(interaction)
        else:
            await gear_page.render(interaction)

    @only_command_invoker()
    async def home_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage
        await HomePage(self. cordia_service, self.discord_id).render(interaction)
