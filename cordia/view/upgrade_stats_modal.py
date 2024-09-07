from cordia.service.cordia_service import CordiaService
from cordia.util.stats_util import get_stats_embed, get_upgrade_points
from cordia.util.text_format_util import get_stat_emoji
from discord.ui import Modal, TextInput
import discord


class UpgradeStatsModal(Modal):
    def __init__(self, cordia_service: CordiaService, discord_id: int, stat: str):
        super().__init__(title="Upgrade Stats")

        # Create a text input for the value to update
        self.stat_input = TextInput(label=f"Points to allocate")
        self.add_item(self.stat_input)
        self.discord_id = discord_id
        self.stat = stat
        self.cordia_service = cordia_service

    async def on_submit(self, interaction: discord.Interaction):
        # Handle the form submission, e.g., update the player's stats
        stat_value = self.stat_input.value

        try:
            stat_value_int = int(stat_value)
            await self.cordia_service.increment_stat(
                self.discord_id, self.stat, stat_value_int
            )
            succeed_embed = discord.Embed(
                title=f"Allocated {stat_value} points into {get_stat_emoji(self.stat)}{self.stat}",
                color=discord.Color.green(),
            )
            player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
            player_gear = await self.cordia_service.get_player_gear(self.discord_id)
            await interaction.response.edit_message(
                embed=get_stats_embed(player, player_gear)
            )
            await interaction.followup.send(embed=succeed_embed, ephemeral=True)
        except Exception as e:
            fail_embed = discord.Embed(
                title=f"❌Please enter a valid amount.", color=discord.Color.red()
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
