from cordia.util.stats_util import get_stats_embed, get_upgrade_points
from cordia.util.text_format_util import get_stat_emoji_mapping
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
            stat_emoji_mapping = get_stat_emoji_mapping()
            for s in stat_emoji_mapping.keys():
                upgrade_stat_button = Button(label=f"⬆️{stat_emoji_mapping[s]}", style=discord.ButtonStyle.blurple)
                view.add_item(upgrade_stat_button)

                def create_callback(stat):
                    async def upgrade_stats_button_callback(interaction: discord.Interaction):
                        modal = UpgradeStatsModal(self.cordia_service, self.discord_id, stat)
                        await interaction.response.send_modal(modal)
                    return upgrade_stats_button_callback

                upgrade_stat_button.callback = create_callback(s)
        
        stats_embed = get_stats_embed(player, player_gear)
        await interaction.response.edit_message(embed=stats_embed, view=view)

    def _create_view(self):
        view = View(timeout=None)

        back_button = Button(label="Back", style=discord.ButtonStyle.blurple, custom_id="back_button")
        back_button.callback = self.back_button_callback
        view.add_item(back_button)

        return view
    
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage
        await HomePage(self. cordia_service, self.discord_id).render(interaction)
        