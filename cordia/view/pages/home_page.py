from cordia.view.pages.page import Page
import discord
from discord.ui import Button, View

class HomePage(Page):
    async def render(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Welcome to Cordia",
        )
        await interaction.response.edit_message(embed=embed, view=self._create_view())

    async def init_render(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Welcome to Cordia",
        )
        await interaction.response.send_message(embed=embed, view=self._create_view())
    
    def _create_view(self):
        view = View()

        # Fight button with callback attached
        fight_button = Button(label="Fight", style=discord.ButtonStyle.blurple, custom_id="fight_button")
        fight_button.callback = self.fight_button_callback  # Attach the callback function here

        # Stats button with callback attached
        stats_button = Button(label="Stats", style=discord.ButtonStyle.blurple, custom_id="stats_button")
        stats_button.callback = self.stats_button_callback  # Attach the callback function here

        # Add buttons to the view
        view.add_item(fight_button)
        view.add_item(stats_button)
        
        return view
    
    async def fight_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.fight_page import FightPage
        await FightPage(self.cordia_service, self.discord_id).render(interaction)

    async def stats_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.stats_page import StatsPage
        await StatsPage(self.cordia_service, self.discord_id).render(interaction)
