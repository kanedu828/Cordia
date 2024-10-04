from cordia.util.decorators import only_command_invoker
from cordia.view.pages.page import Page
import discord
from discord.ui import View, Button


class GuidePage(Page):
    async def render(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Guide", color=discord.Color.dark_orange())
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        guide_text = (
            "Naviage the different pages to learn more about the game. If you need more help, feel free to reach out on Discord! "
            "\nView our wiki for further information: https://github.com/kanedu828/Cordia-Wiki"
        )
        embed.add_field(
            name="Guide Menu",
            value=guide_text,
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
        leaderboard_text = (
            "Daily leaderboards reset every 11:55 PM EST. Players who are top 3 in any of the categories will recieve a trophy."
            "Only rewards gained from manual attacking are counted towards the daily leaderboard."
        )
        embed.add_field(
            name="About leaderboards",
            value=leaderboard_text,
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self._create_view())

    async def render_upgrade(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Upgrading Gear Guide", color=discord.Color.dark_orange()
        )
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        cores_text = (
            "Stars increase that stats of your gear. For every star, the cost the upgrade your gear increases. "
            "Every 5 stars, the stats gained from each star also increases. After you reach 10 stars, you will need fragments"
            " to continue upgrading your gear. Fragments can be found from monsters and bosses."
        )
        embed.add_field(
            name="Stars",
            value=cores_text,
            inline=False,
        )

        cores_text = (
            "Cores given random bonus stats to your gear. The better the core (basic, quality, supreme, chaos), "
            "the better that bonus stats are. You can get anywhere from one to three bonus stats when using cores. "
            "Basic, quality, and supreme cores can be found from monsters and bosses. Chaos cores can be found from powerful monsters, "
            "and bosses."
        )
        embed.add_field(
            name="Cores",
            value=cores_text,
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self._create_view())

    async def render_rebirth(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Rebirth Guide", color=discord.Color.dark_orange())
        image_path = "https://kanedu828.github.io/cordia-assets/assets/guide_page.png"
        embed.set_image(url=image_path)
        rebirth_text = (
            "If you would like to reset your stats, you can rebirth. When you rebirth, your exp is set back to 0. "
            "However, you will keep all your gear and items. Once you reach level 50, you will gain extra upgrade points for "
            "rebirthing. You can use rebirthing to become more powerful."
        )
        embed.add_field(
            name="Rebirth",
            value=rebirth_text,
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self._create_view())

    def _create_view(self):
        view = View(timeout=None)

        stats_button = Button(label="Stats", style=discord.ButtonStyle.blurple)
        stats_button.callback = self.stats_button_callback

        rebirth_button = Button(label="Rebirth", style=discord.ButtonStyle.blurple)
        rebirth_button.callback = self.rebirth_button_callback

        leaderboard_button = Button(
            label="Leaderboard", style=discord.ButtonStyle.blurple
        )
        leaderboard_button.callback = self.leaderboard_button_callback

        upgrade_button = Button(
            label="Upgrading Gear", style=discord.ButtonStyle.blurple
        )
        upgrade_button.callback = self.upgrade_button_callback

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=4)
        back_button.callback = self.back_button_callback

        view.add_item(stats_button)
        view.add_item(rebirth_button)
        view.add_item(upgrade_button)
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

    @only_command_invoker()
    async def rebirth_button_callback(self, interaction: discord.Interaction):
        await self.render_rebirth(interaction)

    @only_command_invoker()
    async def upgrade_button_callback(self, interaction: discord.Interaction):
        await self.render_upgrade(interaction)
