from collections import defaultdict
import math
from cordia.util.decorators import only_command_invoker
from cordia.util.stat_mapping import get_stat_emoji
from cordia.util.text_format_util import get_stars_string
from cordia.view.pages.page import Page
from cordia.data.achievements import achievement_data
import discord
from discord.ui import View, Button


class AchievementPage(Page):
    def __init__(self, cordia_service, discord_id, page_number=0):
        super().__init__(cordia_service, discord_id)
        self.page_number = page_number
        self.achievements_per_page = 10
        self.achievements = []

    async def render(self, interaction: discord.Interaction):
        ad = achievement_data.copy()
        self.achievements = [
            list(ad.keys())[i : i + self.achievements_per_page]
            for i in range(0, len(ad.keys()), self.achievements_per_page)
        ]

        embed = await self._create_achievement_embed()
        view = self._create_view()

        await interaction.response.edit_message(embed=embed, view=view)

    async def _create_achievement_embed(self):
        embed = discord.Embed(
            title="Achievements", description="", color=discord.Color.gold()
        )

        achievements_on_page: list[str] = self.achievements[self.page_number]

        player_achievements = await self.cordia_service.get_achievements_by_discord_id(
            self.discord_id
        )

        player_achievements = {a.monster: a.count for a in player_achievements}

        player_achievements = defaultdict(int, player_achievements)

        for i in achievements_on_page:
            achievement = achievement_data[i]

            milestones = math.floor(
                player_achievements[i] / achievement.monster_killed_increment
            )
            next_milestone = (
                achievement.monster_killed_increment * milestones
                + achievement.monster_killed_increment
            )
            next_milestone = min(
                next_milestone, achievement.monster_killed_increment * 5
            )
            if i in player_achievements:
                progress = f"{player_achievements[i]}/{next_milestone}"
            else:
                progress = f"0/{next_milestone}"

            stat_bonus = ""
            if milestones > 0:
                bonus_stat, bonus_value = (
                    achievement.stat_bonus * milestones
                ).get_one_non_zero_stat()
                stat_bonus = f"Current Stat Bonus: `+{bonus_value}{'%' if achievement.stat_modifier == '%' else ''} {get_stat_emoji(bonus_stat)}{bonus_stat}`\n"
            if milestones >= 5:
                next_stat_bonus = "Achievement Finished"
            else:
                bonus_stat, bonus_value = achievement.stat_bonus.get_one_non_zero_stat()
                next_stat_bonus = f"`+{bonus_value}{'%' if achievement.stat_modifier == '%' else ''} {get_stat_emoji(bonus_stat)}{bonus_stat}`"
            achievement_text = f"Next Milestone Progress: `{progress}`\n{stat_bonus}Next Milestone Bonus: {next_stat_bonus}"

            embed.add_field(
                name=f"Slay {achievement.monster}s {get_stars_string(milestones, 5)}",
                value=achievement_text,
                inline=False,
            )

        embed.set_footer(text=f"Page: {self.page_number + 1}/{len(self.achievements)}")

        return embed

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
        if self.page_number >= len(self.achievements) - 1:
            next_button.disabled = True

        return view

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
