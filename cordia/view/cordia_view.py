import datetime
from typing import List
from cordia.util.stats_util import get_stats_embed, get_upgrade_points
from cordia.view.upgrade_stats_modal import UpgradeStatsModal
import discord
from discord.ui import Button, View
import asyncio
from cordia.view.location_select import LocationSelect
from cordia.service.cordia_service import CordiaService
from cordia.model.location import Location
from cordia.util.exp_util import exp_to_level
from cordia.util.text_format_util import exp_bar, get_player_stats_string, get_stat_emoji_mapping

class CordiaView(View):
    def __init__(self, cordia_service: CordiaService, discord_id: int):
        super().__init__(timeout=None)
        self.page = 'home'

        self.cordia_service = cordia_service

        self.discord_id = discord_id

        self.history_stack = []

        self.pages = {
            "home": {
                "function": self.home_page,
                "items": [
                    Button(label="Fight", style=discord.ButtonStyle.blurple, custom_id="attack_button"),
                    Button(label="Stats", style=discord.ButtonStyle.blurple, custom_id="stats_button")
                ]
            },
            "fight": {
                "function": self.attack,
                "items": [
                    Button(label="Attack", style=discord.ButtonStyle.blurple, custom_id="attack_button"),
                    Button(label="Spell", style=discord.ButtonStyle.blurple, custom_id="spell_button"),
                ]
            },
            "stats": {
                "function": self.stats_page,
                "items": []
            }
        }
    
    def add_page_items(self, page: str, additional_items: List = []):
        self.clear_items()
        for i in additional_items:
            self.add_item(i)
        for i in self.pages[page]["items"]:
            self.add_item(i)
        if page != "home":
            self.add_item(Button(label="Back",  style=discord.ButtonStyle.blurple, custom_id="back_button"))
            self.add_item(Button(label="Home",  style=discord.ButtonStyle.blurple, custom_id="home_button"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Check which button or select triggered the interaction
        if interaction.data.get("custom_id") == "attack_button":
            await self.attack(interaction)
        if interaction.data.get("custom_id") == "stats_button":
            await self.stats_page(interaction)
        if interaction.data.get("custom_id") == "back_button":
            await self.back(interaction)
        if interaction.data.get("custom_id") == "home_button":
            await self.home(interaction)
        return True
    
    async def back(self, interaction):
        self.history_stack.pop()
        page = self.history_stack[-1]
        page_function = self.pages[page]["function"]
        await page_function(interaction)
    
    async def home(self, interaction):
        self.history_stack = ["home"]
        await self.home_page(interaction)

    def push_to_history(self, page_name: str):
        if len(self.history_stack) > 0 and self.history_stack[-1] == page_name:
            return
        else:
            self.history_stack.append(page_name)

    async def get_embed(self):
        # Place holder image. Replace per location later
        player = await self.cordia_service.get_or_insert_player(self.discord_id)
        embed = discord.Embed(
            title=f"Home",
        )
        return embed
    
    async def home_page(self, interaction: discord.Interaction):
        self.add_page_items("home")
        embed = discord.Embed(
            title=f"Welcome to Cordia",
        )
        if len(self.history_stack) == 0:
            await interaction.response.send_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)
        self.push_to_history("home")

    async def stats_page(self, interaction: discord.Interaction):
        self.push_to_history("stats")
        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
        player_gear = await self.cordia_service.get_player_gear(self.discord_id)

        if get_upgrade_points(player):
            stat_emoji_mapping = get_stat_emoji_mapping()
            for s in stat_emoji_mapping.keys():
                upgrade_stat_button = Button(label=f"⬆️{stat_emoji_mapping[s]}", style=discord.ButtonStyle.blurple)
                self.add_item(upgrade_stat_button)

                def create_callback(stat):
                    async def upgrade_stats_button_callback(interaction: discord.Interaction):
                        modal = UpgradeStatsModal(self.cordia_service, self.discord_id, stat)
                        await interaction.response.send_modal(modal)
                    return upgrade_stats_button_callback

                upgrade_stat_button.callback = create_callback(s)
        
        # Add page items after upgrade buttons
        self.add_page_items("stats")

        stats_embed = get_stats_embed(player, player_gear)
        await interaction.response.edit_message(embed=stats_embed, view=self)
    
    async def attack(self, interaction: discord.Interaction):
        self.push_to_history("fight")
        attack_results = await self.cordia_service.attack(self.discord_id)

        current_exp = attack_results['player_exp']
        current_level = exp_to_level(current_exp)

        # Buttons for attack
        self.add_page_items("fight", [LocationSelect(current_level)])
        
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
            await interaction.response.edit_message(embed=embed, view=self)
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

        # Update the message with initial embed and disabled button
        await interaction.response.edit_message(embed=embed, view=self)

        if attack_results['leveled_up']:
            level_up_embed = discord.Embed(
                title=f"✨You leveled up to level {current_level}!✨",
                color=discord.Color.blue()
            )  
            await interaction.followup.send(embed=level_up_embed, ephemeral=True)
        
