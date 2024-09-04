import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional

from cordia.view.cordia_view import CordiaView

class Cordia(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="battle")
  async def battle(self, interaction: discord.Interaction) -> None:
    view = CordiaView(self.bot.cordia_service, interaction.user.id)
    embed = await view.get_embed()
    await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Cordia(bot))