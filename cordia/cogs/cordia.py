from cordia.view.embeds.seach_gear_embed import get_search_gear_embed
from cordia.view.pages.home_page import HomePage
import discord
from discord import app_commands
from discord.ext import commands


class Cordia(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="play")
    async def play(self, interaction: discord.Interaction) -> None:
        page = HomePage(self.bot.cordia_service, interaction.user.id)
        await page.init_render(interaction)
    
    @app_commands.command(name="search_gear", description="Search for gear by name.")
    async def search_gear(self,  interaction: discord.Interaction, gear_name: str) -> None:
        embed = get_search_gear_embed(gear_name)
        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cordia(bot))