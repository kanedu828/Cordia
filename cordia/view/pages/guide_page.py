from cordia.util.decorators import only_command_invoker
from cordia.view.pages.page import Page
import discord
from discord.ui import View, Button


class GuidePage(Page):
    async def render(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Guide", color=discord.Color.dark_orange())
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        embed.add_field(
            name="Guide Menu",
            value="Naviage the different pages to learn more about the game. If you need more help, feel free to reach out on Discord!",
            inline=False,
        )

        await interaction.response.edit_message(embed=embed, view=self._create_view())

    async def render_stats(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Stats Guide", color=discord.Color.dark_orange())
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        embed.add_field(
            name="Strength",
            value='Scales your "attack" button. The more strength you have, the more damage you do!',
            inline=False,
        )
        embed.add_field(
            name="Persistence",
            value="Scales how much damage you do in your idle fights. If you want more rewards while idling, you should increase this.",
            inline=False,
        )

        embed.add_field(
            name="Intelligence",
            value="Scales how much damage you do on magic-based spells. Most wand and staff-like weapons will have spells that scale off of intelligence.",
            inline=False,
        )

        embed.add_field(
            name="Efficiency",
            value="Scales how much exp you get when fighting monsters. This is capped at 2x the base exp given by the monster.",
            inline=False,
        )

        embed.add_field(
            name="Luck",
            value="Scales how much gold you get when fighting monsters. This is capped at 2x the base gold given by the monster.",
            inline=False,
        )

        embed.add_field(
            name="Damage",
            value="Typically comes from your weapon. This is your base damage for attacking.",
            inline=False,
        )

        embed.add_field(
            name="Spell Damage",
            value="Typically comes from your weapon's spell. This is your base damage for casting spells.",
            inline=False,
        )

        embed.add_field(
            name="Boss Damage",
            value="Percent multiplier on how much damage you deal to bosses.",
            inline=False,
        )

        embed.add_field(
            name="Crit Chance",
            value="Percent chance to critically strike on your attacks and spells. Critical strikes are 1.5x damage multipliers.",
            inline=False,
        )

        embed.add_field(
            name="Penetration",
            value="Percent of defense you ignore from the monster.",
            inline=False,
        )

        embed.add_field(
            name="Combo Chance",
            value="Percent chance to reset your cooldowns for your attack or spell.",
            inline=False,
        )

        embed.add_field(
            name="Strike Radius",
            value="Max amount of monsters you can kill in one attack.",
            inline=False,
        )

        await interaction.response.edit_message(embed=embed, view=self._create_view())

    async def render_leaderboard(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Stats Guide", color=discord.Color.dark_orange())
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        leaderboard_text = "Daily leaderboards reset every 11:55 PM EST. Players who are top 3 in any of the categories will recieve a trophy."
        embed.add_field(
            name="About leaderboards",
            value=leaderboard_text,
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self._create_view())

    def _create_view(self):
        view = View(timeout=None)

        stats_button = Button(label="Stats", style=discord.ButtonStyle.blurple)
        stats_button.callback = self.stats_button_callback

        leaderboard_button = Button(
            label="Leaderboard", style=discord.ButtonStyle.blurple
        )
        leaderboard_button.callback = self.leaderboard_button_callback

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=4)
        back_button.callback = self.back_button_callback

        view.add_item(stats_button)
        view.add_item(leaderboard_button)
        view.add_item(back_button)

        return view

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def stats_button_callback(self, interaction: discord.Interaction):
        await self.render_stats(interaction)

    @only_command_invoker()
    async def leaderboard_button_callback(self, interaction: discord.Interaction):
        await self.render_leaderboard(interaction)
