import math
from cordia.util.decorators import only_command_invoker
from cordia.util.constants import VIEW_TIMEOUT
from cordia.util.text_format_util import display_exp, display_gold
from cordia.view.pages.page import Page
import discord
from discord.ui import View, Button, Select


class LeaderboardPage(Page):
    def __init__(self, cordia_service, discord_id, page_number=0):
        super().__init__(cordia_service, discord_id)
        self.page_number = page_number
        self.players_per_page = 10  # Define how many players per page
        self.top_100_players = []  # This will be populated when render is called
        self.type = "exp"
        self.daily = False

    async def render_leaderboard(self, interaction: discord.Interaction):
        if self.daily:
            player_rank = await self.cordia_service.leaderboard_service.get_player_daily_rank_by_column(
                self.discord_id, self.type
            )
        else:
            player_rank = await self.cordia_service.leaderboard_service.get_player_rank_by_column(
                self.discord_id, self.type
            )
        # Create embed to show players on the current page
        embed = await self._create_leaderboard_embed(player_rank)

        # Create view with navigation buttons
        view = self._create_view()

        await interaction.response.edit_message(embed=embed, view=view)

    async def render(self, interaction: discord.Interaction):
        # Fetch top 100 players and player rank
        self.top_100_players = await self.cordia_service.leaderboard_service.get_top_100_players_by_column(
            self.type
        )
        self.daily = False
        await self.render_leaderboard(interaction)

    async def render_daily_leaderboard(self, interaction: discord.Interaction):
        # Fetch top 100 players and player rank
        self.top_100_players = (
            await self.cordia_service.leaderboard_service.get_top_100_daily_players_by_column(self.type)
        )
        self.daily = True
        await self.render_leaderboard(interaction)

    def _create_view(self):
        view = View(timeout=VIEW_TIMEOUT)  # 5 minute timeout instead of None

        leaderboard_select_options = [
            discord.SelectOption(label="Exp", value="exp"),
            discord.SelectOption(label="Rebirth Points", value="rebirth_points"),
            discord.SelectOption(label="Gold", value="gold"),
            discord.SelectOption(label="Trophies", value="trophies"),
        ]

        if self.daily:
            leaderboard_select_options = [
                discord.SelectOption(label="Exp", value="exp"),
                discord.SelectOption(label="Monsters Killed", value="monsters_killed"),
                discord.SelectOption(label="Gold", value="gold"),
            ]

        leaderboard_type_select = Select(
            placeholder="Select a leaderboard type",
            min_values=1,
            max_values=1,
            options=leaderboard_select_options,
            row=0,
        )
        leaderboard_type_select.callback = (
            self.daily_leaderboard_type_select_callback
            if self.daily
            else self.leaderboard_type_select_callback
        )
        view.add_item(leaderboard_type_select)

        leaderboard_button = Button(
            label="Leaderboard", style=discord.ButtonStyle.primary, row=1
        )
        leaderboard_button.callback = self.leaderboard_button_callback
        view.add_item(leaderboard_button)

        daily_leaderboard_button = Button(
            label="Daily Leaderboard", style=discord.ButtonStyle.primary, row=1
        )
        daily_leaderboard_button.callback = self.daily_leaderboard_button_callback
        view.add_item(daily_leaderboard_button)

        prev_button = Button(label="⇦", style=discord.ButtonStyle.primary, row=2)
        prev_button.callback = self.previous_page_callback
        view.add_item(prev_button)
        # disabled if first page
        if self.page_number <= 0:
            prev_button.disabled = True

        next_button = Button(label="⇨", style=discord.ButtonStyle.primary, row=2)
        next_button.callback = self.next_page_callback
        view.add_item(next_button)
        # disable if last page
        if (self.page_number + 1) * self.players_per_page >= len(self.top_100_players):
            next_button.disabled = True

        # Add Back button to go back to the home page
        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=3)
        back_button.callback = self.back_button_callback
        view.add_item(back_button)

        return view

    async def _create_leaderboard_embed(self, player_rank):
        embed = discord.Embed(
            title=f"{'Daily ' if self.daily else ''}Leaderboard",
            description=f"Top 100 Players by {self.type.replace('_', ' ').title()}",
            color=discord.Color.blue(),
        )

        # Get the players for the current page
        start_index = self.page_number * self.players_per_page
        end_index = min(start_index + self.players_per_page, len(self.top_100_players))
        players_on_page = self.top_100_players[start_index:end_index]

        # Add each player to the embed, with special emojis for the top 3
        for idx, player in enumerate(players_on_page, start=start_index + 1):
            user = await self.cordia_service.leaderboard_service.get_leaderboard_user(player.discord_id)

            # Determine the rank to display
            if idx == 1:
                rank_display = "🥇"
            elif idx == 2:
                rank_display = "🥈"
            elif idx == 3:
                rank_display = "🥉"
            else:
                rank_display = f"{idx}. "

            if self.type == "exp":
                stat_value = display_exp(player.exp)
            elif self.type == "gold":
                stat_value = display_gold(player.gold)
            elif self.type == "trophies":
                stat_value = f"🏆**{player.__dict__[self.type]:,}**"
            else:
                stat_value = f"**{player.__dict__[self.type]:,}**"

            embed.add_field(
                name=f"{rank_display} {user}",
                value=stat_value,
                inline=False,
            )

        # Show the player's rank at the bottom
        embed.set_footer(
            text=f"Your rank: {player_rank}\nPage: {self.page_number + 1}/{math.ceil(len(self.top_100_players) / self.players_per_page)}"
        )

        return embed

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def previous_page_callback(self, interaction: discord.Interaction):
        # Decrease the page number and re-render the page
        self.page_number -= 1
        await self.render_leaderboard(interaction)

    @only_command_invoker()
    async def next_page_callback(self, interaction: discord.Interaction):
        # Increase the page number and re-render the page
        self.page_number += 1
        await self.render_leaderboard(interaction)

    @only_command_invoker()
    async def leaderboard_type_select_callback(self, interaction: discord.Interaction):
        self.type = interaction.data["values"][0]
        await self.render(interaction)

    @only_command_invoker()
    async def daily_leaderboard_type_select_callback(
        self, interaction: discord.Interaction
    ):
        self.type = interaction.data["values"][0]
        await self.render_daily_leaderboard(interaction)

    @only_command_invoker()
    async def leaderboard_button_callback(self, interaction: discord.Interaction):
        self.type = "exp"
        self.page_number = 0
        await self.render(interaction)

    @only_command_invoker()
    async def daily_leaderboard_button_callback(self, interaction: discord.Interaction):
        self.type = "exp"
        self.page_number = 0
        await self.render_daily_leaderboard(interaction)
