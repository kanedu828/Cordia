from cordia.model.location import Location
from cordia.util.exp_util import exp_to_level
from cordia.util.text_format_util import exp_bar
from cordia.view.pages.page import Page
from cordia.data.locations import location_data
from discord.ui import View, Button, Select
import discord

class FightPage(Page):
    async def render(self, interaction: discord.Interaction):
        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)

        location: Location = location_data[player.location]
        embed = discord.Embed(
            title=f"Fighting Monsters in {location.name}",
        )
        exp_bar_text = f"{exp_bar(player.exp)}\n\n"
        embed.add_field(name="", value=exp_bar_text, inline=False)
        embed.set_image(url=location.get_image_path())
        await interaction.response.edit_message(embed=embed, view=await self._create_view())

    async def attack(self, interaction: discord.Interaction):
        attack_results = await self.cordia_service.attack(self.discord_id)

        current_exp = attack_results['player_exp']
        current_level = exp_to_level(current_exp)

        location: Location = attack_results['location']
        embed = discord.Embed(
            title=f"Fighting Monsters in {location.name}",
        )

        exp_bar_text = f"{exp_bar(current_exp)}\n\n"
        embed.add_field(name="", value=exp_bar_text, inline=False)

        embed.set_image(url=location.get_image_path())

        if attack_results['on_cooldown']:
            cooldown_text = f"You are on cooldown. You can attack again {discord.utils.format_dt(attack_results['cooldown_expiration'], style='R')}"
            embed.add_field(name="🕒You're on cooldown!🕒", value=cooldown_text, inline=False)
            await interaction.response.edit_message(embed=embed, view=await self._create_view())
            return
        
        battle_text = f"You deal **{attack_results['damage']}** damage.\n"
        if attack_results['is_crit']:
            battle_text = '🎯Critical strike! ' + battle_text

        if attack_results['is_combo']:
            battle_text = '🥊Combo! ' + battle_text
        
        if attack_results["kills"] == 0:
            battle_text += f"You tried to fight a **{attack_results['monster']}**, but you could not defeat it. Try again!"
        elif attack_results["kills"] == 1:
            battle_text += f"Using all your might, you defeat a **{attack_results['monster']}**"
        else:
            battle_text += f"In a show of grandeur, you defeat **{attack_results['kills']} {attack_results['monster']}s**"
        
        embed.add_field(name="⚔️Battle⚔️", value=battle_text, inline=False)

        rewards_text = f"**{attack_results['exp']}** Exp\n**{attack_results['gold']}** Gold"
        embed.add_field(name="💰Rewards💰", value=rewards_text, inline=False)

        
        # Set the cooldown for the attack button
        cd_embed_index = 3
        embed.insert_field_at(cd_embed_index, name='', value=f"You can attack again {discord.utils.format_dt(attack_results['cooldown_expiration'], style='R')}", inline=False)

        await interaction.response.edit_message(embed=embed, view=await self._create_view())

        if attack_results['leveled_up']:
            level_up_embed = discord.Embed(
                title=f"✨You leveled up to level {current_level}!✨",
                color=discord.Color.blue()
            )  
            await interaction.followup.send(embed=level_up_embed, ephemeral=True)

    async def _create_view(self):
        view = View()

        attack_button = Button(label="Attack", style=discord.ButtonStyle.blurple, custom_id="attack_button")
        attack_button.callback = self.attack

        cast_spell_button = Button(label="Cast Spell", style=discord.ButtonStyle.blurple, custom_id="cast_spell_button")

        back_button = Button(label="Back", style=discord.ButtonStyle.blurple, custom_id="back_button")
        back_button.callback = self.back_button_callback

        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
        current_level = exp_to_level(player.exp)

        locations = [location for location in list(location_data.keys()) if current_level >= location_data[location].level_unlock][::-1]
        options = [discord.SelectOption(label=location_data[location].name, description=f'Unlocks at level {location_data[location].level_unlock}', value=location) for location in locations]
        
        location_select = Select(placeholder='Select a location',
            min_values=1,
            max_values=1,
            options=options
        )
        location_select.callback = self.location_select_callback
        
        view.add_item(attack_button)
        view.add_item(cast_spell_button)
        view.add_item(back_button)
        view.add_item(location_select)

        return view
    
    async def attack_button_callback(self, interaction: discord.Interaction):
        await self.attack(interaction)

    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage
        await HomePage(self. cordia_service, self.discord_id).render(interaction)
    
    async def location_select_callback(self, interaction: discord.Interaction):
        await self.cordia_service.update_location(interaction.user.id, interaction.data["values"][0])
        from cordia.view.pages.fight_page import FightPage # Lazy import, avoid circular dep
        await FightPage(self.cordia_service, self.discord_id).render(interaction)