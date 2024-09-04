from cordia.model.gear import GearInstance, GearType
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

        await self.cordia_service.get_or_insert_player(self.discord_id)
        player_gear = await self.cordia_service.get_player_gear(self.discord_id)
        weapon = await self.cordia_service.get_weapon(player_gear)
        if not weapon:
            welcome_text = "**Sword**: A slow, but hard hitting weapon"
            welcome_text += "\n**Dagger**: A quick weapon that allows you to hit fast"
            welcome_text += "\n**Bow**: A weapon that is more efficient when fighting idle"
            welcome_text += "\n**Wand**: A weapon with access to powerful spells to deal damage"
            embed.add_field(name="Welcome adventurer. Select a weapon to begin your journey...", value=welcome_text, inline=False)
            await interaction.response.send_message(embed=embed, view=self._create_new_player_view(interaction))
        else:
            await interaction.response.send_message(embed=embed, view=self._create_view())

    def _create_new_player_view(self, interaction: discord.Interaction):
        view = View(timeout=None)

        def gen_weapon_callback(weapon):
            async def equip_weapon(interaction: discord.Interaction):
                gear_instance: GearInstance = await self.cordia_service.insert_gear(self.discord_id, weapon)
                await self.cordia_service.equip_gear(self.discord_id, gear_instance.id, GearType.WEAPON.value)
                await self.render(interaction)
            return equip_weapon
        
        sword = Button(label="Sword", style=discord.ButtonStyle.blurple)
        sword.callback = gen_weapon_callback('basic_sword')

        dagger = Button(label="Dagger", style=discord.ButtonStyle.blurple, custom_id="basic_dagger")
        dagger.callback = gen_weapon_callback('basic_dagger')

        bow = Button(label="Bow", style=discord.ButtonStyle.blurple, custom_id="basic_bow")
        bow.callback = gen_weapon_callback('basic_bow')

        wand = Button(label="Wand", style=discord.ButtonStyle.blurple, custom_id="basic_wand")
        wand.callback = gen_weapon_callback('basic_wand')

        view.add_item(sword)
        view.add_item(dagger)
        view.add_item(bow)
        view.add_item(wand)
        
        return view

    def _create_view(self):
        view = View(timeout=None)

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
