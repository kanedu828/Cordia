import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional

class Cordia(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="battle")
  async def battle(self, interaction: discord.Interaction) -> None:
    message: str = 'Pong! {0}'.format(round(self.latency * 1000, 1))
    await interaction.response.send_message(message, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Cordia(bot))