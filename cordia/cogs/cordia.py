from cordia.view.pages.home_page import HomePage
import discord
from discord import app_commands
from discord.ext import commands

class Cordia(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="battle")
  async def battle(self, interaction: discord.Interaction) -> None:
    page = HomePage(self.bot.cordia_service, interaction.user.id)
    await page.init_render(interaction)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Cordia(bot))