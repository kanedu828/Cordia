from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.util.decorators import only_command_invoker
from cordia.util.gear_util import get_weapon_from_player_gear
from cordia.view.pages.fight_boss_page import FightBossPage
from cordia.view.pages.page import Page
import discord
from discord.ui import Button, View


class HomePage(Page):
    def _get_embed(self):
        embed = discord.Embed(
            title=f"Welcome to Cordia",
        )
        image_path = "https://kanedu828.github.io/cordia-assets/assets/home_page.png"
        embed.set_image(url=image_path)
        embed.add_field(
            name="📜Quests📜", value="You currently have no quests", inline=False
        )
        navigation_text = "**Fight**: Fight monsters\n**Fight Boss**: Fight a powerful boss to obtain rewards\n**Stats**: View and upgrade your stats\n**Gear**: View and upgrade your gear"
        embed.add_field(name="🧭Navigation🧭", value=navigation_text, inline=False)
        return embed

    async def render(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=self._get_embed(), view=self._create_view()
        )

    async def init_render(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Welcome to Cordia",
        )
        image_path = "https://kanedu828.github.io/cordia-assets/assets/home_page.png"
        embed.set_image(url=image_path)
        await self.cordia_service.get_or_insert_player(self.discord_id)
        player_gear = await self.cordia_service.get_player_gear(self.discord_id)
        weapon = get_weapon_from_player_gear(player_gear)
        if not weapon:
            welcome_text = (
                "**Sword**: A slow, but hard hitting weapon that hits many monsters"
            )
            welcome_text += "\n**Dagger**: A quick weapon that allows you to deal a lot of damage quickly"
            welcome_text += (
                "\n**Bow**: A weapon that is more efficient when fighting idle"
            )
            welcome_text += (
                "\n**Wand**: A weapon with access to powerful spells to deal damage"
            )
            embed.add_field(
                name="Welcome adventurer. Select a weapon to begin your journey...",
                value=welcome_text,
                inline=False,
            )
            await interaction.response.send_message(
                embed=embed, view=self._create_new_player_view(interaction)
            )
        else:
            await interaction.response.send_message(
                embed=self._get_embed(), view=self._create_view()
            )

    def _create_new_player_view(self, interaction: discord.Interaction):
        view = View(timeout=None)

        def gen_weapon_callback(weapon):
            async def equip_weapon(interaction: discord.Interaction):
                gear_instance: GearInstance = await self.cordia_service.insert_gear(
                    self.discord_id, weapon
                )
                await self.cordia_service.equip_gear(
                    self.discord_id, gear_instance.id, GearType.WEAPON.value
                )
                await self.render(interaction)

            return equip_weapon

        sword = Button(label="Sword", style=discord.ButtonStyle.blurple)
        sword.callback = gen_weapon_callback("basic_sword")

        dagger = Button(label="Dagger", style=discord.ButtonStyle.blurple)
        dagger.callback = gen_weapon_callback("basic_dagger")

        bow = Button(label="Bow", style=discord.ButtonStyle.blurple)
        bow.callback = gen_weapon_callback("basic_bow")

        wand = Button(label="Wand", style=discord.ButtonStyle.blurple)
        wand.callback = gen_weapon_callback("basic_wand")

        view.add_item(sword)
        view.add_item(dagger)
        view.add_item(bow)
        view.add_item(wand)

        return view

    def _create_view(self):
        view = View(timeout=None)

        # Fight button with callback attached
        fight_button = Button(label="Fight", style=discord.ButtonStyle.blurple)
        fight_button.callback = (
            self.fight_button_callback
        )  # Attach the callback function here

        # Fight button with callback attached
        fight_boss_button = Button(
            label="Fight Boss", style=discord.ButtonStyle.blurple
        )
        fight_boss_button.callback = (
            self.fight_boss_button_callback
        )  # Attach the callback function here

        # Stats button with callback attached
        stats_button = Button(label="Stats", style=discord.ButtonStyle.blurple)
        stats_button.callback = (
            self.stats_button_callback
        )  # Attach the callback function here

        gear_button = Button(label="Gear", style=discord.ButtonStyle.blurple)
        gear_button.callback = self.gear_button_callback

        # Add buttons to the view
        view.add_item(fight_button)
        view.add_item(fight_boss_button)
        view.add_item(stats_button)
        view.add_item(gear_button)

        return view

    @only_command_invoker()
    async def fight_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.fight_page import FightPage

        bi = await self.cordia_service.get_boss_by_discord_id(self.discord_id)
        if bi:
            in_boss_embed = discord.Embed(
                title=f"You cannot fight right now",
                color=discord.Color.red(),
            )
            in_boss_embed.add_field(
                name="You must finish or forfeit your current boss fight.",
                value="",
                inline=False,
            )
            await interaction.response.send_message(embed=in_boss_embed, ephemeral=True)
        await FightPage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def fight_boss_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.fight_page import FightPage

        await FightBossPage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def stats_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.stats_page import StatsPage

        await StatsPage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def gear_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.gear_page import GearPage

        gear_page = await GearPage.create(self.cordia_service, self.discord_id)
        await gear_page.render(interaction)
