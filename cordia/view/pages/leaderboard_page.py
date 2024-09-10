from cordia.util.decorators import only_command_invoker
from cordia.view.pages.page import Page
import discord
from discord.ui import View, Button


class LeaderboardPage(Page):
    def __init__(self, cordia_service, discord_id, page_number=0):
        super().__init__(cordia_service, discord_id)
        self.page_number = page_number
        self.players_per_page = 10  # Define how many players per page
        self.top_100_players = []  # This will be populated when render is called

    async def render(self, interaction: discord.Interaction):
        # Fetch top 100 players and player rank
        self.top_100_players = await self.cordia_service.get_top_100_players_by_exp()
        player_rank = await self.cordia_service.get_player_rank_by_exp(self.discord_id)

        # Create embed to show players on the current page
        embed = await self._create_leaderboard_embed(player_rank)

        # Create view with navigation buttons
        view = self._create_view()

        await interaction.response.edit_message(embed=embed, view=view)

    def _create_view(self):
        view = View(timeout=None)

        # Add Back button to go back to the home page
        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=2)
        back_button.callback = self.back_button_callback
        view.add_item(back_button)

        prev_button = Button(label="⇦", style=discord.ButtonStyle.primary, row=1)
        prev_button.callback = self.previous_page_callback
        view.add_item(prev_button)
        # disabled if first page
        if self.page_number <= 0:
            prev_button.disabled = True

        next_button = Button(label="⇨", style=discord.ButtonStyle.primary, row=1)
        next_button.callback = self.next_page_callback
        view.add_item(next_button)
        # disable if last page
        if (self.page_number + 1) * self.players_per_page >= len(self.top_100_players):
            next_button.disabled = True

        return view

    async def _create_leaderboard_embed(self, player_rank):
        embed = discord.Embed(title="Leaderboard", description="Top 100 Players by EXP")

        # Get the players for the current page
        start_index = self.page_number * self.players_per_page
        end_index = min(start_index + self.players_per_page, len(self.top_100_players))
        players_on_page = self.top_100_players[start_index:end_index]

        # Add each player to the embed, with special emojis for the top 3
        for idx, player in enumerate(players_on_page, start=start_index + 1):
            user = await self.cordia_service.get_leaderboard_user(player.discord_id)

            # Determine the rank to display
            if idx == 1:
                rank_display = "🥇"
            elif idx == 2:
                rank_display = "🥈"
            elif idx == 3:
                rank_display = "🥉"
            else:
                rank_display = f"{idx}. "

            embed.add_field(
                name=f"{rank_display} {user}",
                value=f"**{player.exp} exp**",
                inline=False,
            )

        # Show the player's rank at the bottom
        embed.set_footer(text=f"Your rank: {player_rank}")

        return embed

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def previous_page_callback(self, interaction: discord.Interaction):
        # Decrease the page number and re-render the page
        self.page_number -= 1
        await self.render(interaction)

    @only_command_invoker()
    async def next_page_callback(self, interaction: discord.Interaction):
        # Increase the page number and re-render the page
        self.page_number += 1
        await self.render(interaction)
