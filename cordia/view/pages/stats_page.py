from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.model.player import Player
from cordia.util.decorators import only_command_invoker
from cordia.util.exp_util import exp_to_level
from cordia.util.gear_util import get_weapon_from_player_gear
from cordia.util.interaction_util import edit_message_with_done
from cordia.util.stats_util import get_rebirth_points, get_upgrade_points
from cordia.util.text_format_util import (
    display_gold,
    exp_bar,
    get_player_stats_string,
    get_stat_emoji,
)
from cordia.view.confirmation_modal import ConfirmationModal
from cordia.view.pages.page import Page
from cordia.view.upgrade_stats_modal import UpgradeStatsModal
from discord.ui import View, Button
import discord


class StatsPage(Page):
    async def render(self, interaction: discord.Interaction):
        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
        player_gear = await self.cordia_service.get_player_gear(self.discord_id)

        view = self._create_view()

        if get_upgrade_points(player):
            main_stats = [
                "strength",
                "persistence",
                "intelligence",
                "efficiency",
                "luck",
            ]
            for s in main_stats:
                upgrade_stat_button = Button(
                    label=f"⬆️{get_stat_emoji(s)}",
                    style=discord.ButtonStyle.blurple,
                    row=1,
                )
                view.add_item(upgrade_stat_button)

                def create_callback(stat):
                    async def upgrade_stats_button_callback(
                        interaction: discord.Interaction,
                    ):
                        modal = UpgradeStatsModal(
                            self.cordia_service, self.discord_id, stat
                        )
                        await interaction.response.send_modal(modal)

                    return upgrade_stats_button_callback

                upgrade_stat_button.callback = create_callback(s)

        stats_embed = self._create_embed(player, player_gear)

        await edit_message_with_done(interaction, stats_embed, view)

    def _create_view(self):
        view = View(timeout=None)

        rebirth_button = Button(
            label="Rebirth", style=discord.ButtonStyle.blurple, row=2
        )
        rebirth_button.callback = self.rebirth_button_callback

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=3)
        back_button.callback = self.back_button_callback

        view.add_item(rebirth_button)
        view.add_item(back_button)

        return view

    def _create_embed(self, player: Player, player_gear: list[GearInstance]):
        embed = discord.Embed(title=f"Your Stats", color=discord.Color.blue())
        stats_text, special_stats_text = get_player_stats_string(player, player_gear)
        upgrade_points = get_upgrade_points(player)

        exp_bar_text = f"{exp_bar(player.exp)}\n\n"
        embed.add_field(name="", value=exp_bar_text, inline=False)
        if upgrade_points > 0:
            embed.add_field(
                name="",
                value=f"✨You have {upgrade_points} upgrade points!✨",
                inline=False,
            )
        else:
            embed.add_field(
                name="",
                value=f"You have {upgrade_points} upgrade points.",
                inline=False,
            )
        embed.add_field(name="", value=stats_text)
        embed.add_field(name="", value=special_stats_text)
        weapon = get_weapon_from_player_gear(player_gear)
        spell = weapon.get_gear_data().spell
        if spell:
            embed.add_field(
                name="Spell Stats",
                value=weapon.get_spell_stats_string(False),
                inline=False,
            )

        embed.add_field(name="Gold", value=display_gold(player.gold), inline=False)
        embed.add_field(
            name="Rebirth",
            value=f"You will be reset to **0** exp and gain **{get_rebirth_points(exp_to_level(player.exp))}** upgrade points if you rebirth.",
        )
        return embed

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def rebirth_button_callback(self, interaction: discord.Interaction):
        async def confirmation_callback():
            player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
            rebirth_points = get_rebirth_points(exp_to_level(player.exp))
            await self.cordia_service.increment_rebirth_points(
                self.discord_id, rebirth_points
            )
            await self.cordia_service.rebirth_player(self.discord_id)
            await self.cordia_service.remove_all_gear(self.discord_id)
            armory = await self.cordia_service.get_armory(self.discord_id)
            level_one_weapon = next(
                (
                    x
                    for x in armory
                    if x.get_gear_data().level == 1
                    and x.get_gear_data().type == GearType.WEAPON
                )
            )
            await self.cordia_service.equip_gear(
                self.discord_id, level_one_weapon.id, "weapon"
            )
            # Render the stats page after the followup
            await self.render(interaction)

        modal = ConfirmationModal(
            f"You have successfully rebirthed! You have been reset to 0 exp.",
            confirmation_callback,
        )
        await interaction.response.send_modal(modal)
