from datetime import datetime, timedelta
from typing import Literal
from cordia.model.attack_result import AttackResult
from cordia.model.boos_fight_result import BossFightResult
from cordia.model.location import Location
from cordia.util.decorators import only_command_invoker
from cordia.util.exp_util import exp_to_level
from cordia.util.text_format_util import exp_bar, hp_bar
from cordia.view.embeds.level_up_embed import get_level_up_embed
from cordia.view.pages.page import Page
from cordia.data.locations import location_data
from cordia.data.bosses import boss_data
from cordia.data.gear import gear_data
from discord.ui import View, Button, Select
import discord


class FightBossPage(Page):
    async def render(self, interaction: discord.Interaction):
        bi = await self.cordia_service.get_boss_by_discord_id(self.discord_id)
        if not bi:
            await self.render_select_boss_page(interaction)
        else:
            bd = boss_data[bi.name]
            embed = discord.Embed(
                title=f"Fighting Boss: {bd.display_monster()}",
            )

            hp_bar_text = f"{hp_bar(bi.current_hp, bd.hp)}"
            embed.add_field(name="", value=hp_bar_text, inline=False)

            embed.set_image(url=bd.get_image_path())

            await interaction.response.edit_message(
                embed=embed, view=await self._create_view()
            )

    async def render_select_boss_page(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Select a Boss to Fight",
        )
        embed.set_image(
            url="https://kanedu828.github.io/cordia-assets/assets/boss_fight_page.png"
        )
        embed.add_field(
            name="Boss Fight Info",
            value=(
                "You will have 1 hour to defeat a boss. "
                "You will not be able to fight monsters while a boss fight is active. "
                "If you leave the fight early, you will forfeit any rewards. "
                "You may only fight a boss every 8 hours. "
                "Select a boss to get started!"
            ),
        )

        await interaction.response.edit_message(
            embed=embed, view=await self._create_boss_select_view()
        )

    @only_command_invoker()
    async def cast_spell(self, interaction: discord.Interaction):
        attack_results = await self.cordia_service.boss_fight(
            self.discord_id, "cast_spell"
        )
        await self.fight_boss(interaction, attack_results, "cast_spell")

    @only_command_invoker()
    async def attack(self, interaction: discord.Interaction):
        boss_fight_results = await self.cordia_service.boss_fight(self.discord_id)
        await self.fight_boss(interaction, boss_fight_results, "attack")

    async def fight_boss(
        self,
        interaction: discord.Interaction,
        boss_fight_results: BossFightResult,
        action: Literal["attack", "cast_spell"],
    ):
        bi = boss_fight_results.boss_instance
        bd = boss_data[bi.name]
        embed = discord.Embed(
            title=f"Fighting Boss: {bd.display_monster()}",
        )

        hp_bar_text = f"{hp_bar(bi.current_hp, bd.hp)}"
        embed.add_field(name="", value=hp_bar_text, inline=False)

        embed.set_image(url=bd.get_image_path())

        # Cooldown message
        if boss_fight_results.on_cooldown:
            cd_type_text = "attack"
            if action == "cast_spell":
                cd_type_text = "cast your spell"
            cooldown_text = f"You are on cooldown. You can {cd_type_text} again {discord.utils.format_dt(boss_fight_results.cooldown_expiration, style='R')}"
            embed.add_field(
                name="🕒You're on cooldown!🕒", value=cooldown_text, inline=False
            )
            await interaction.response.edit_message(
                embed=embed, view=await self._create_view()
            )
            return
        
        # Fight monster
        battle_text = f"You deal **{boss_fight_results.damage}** damage.\n"
        if action == "cast_spell":
            battle_text = f"You cast **{boss_fight_results.spell_name}**! {boss_fight_results.spell_text}. You deal **{boss_fight_results.damage}** damage.\n"
        if boss_fight_results.is_crit:
            battle_text = "🎯Critical strike! " + battle_text

        if boss_fight_results.is_combo:
            battle_text = "🥊Combo! " + battle_text

        embed.add_field(name="⚔️Battle⚔️", value=battle_text, inline=False)

        if boss_fight_results.killed:
            # Get loot
            rewards_text = (
                f"**{boss_fight_results.exp}** Exp\n**{boss_fight_results.gold}** Gold"
            )
            for g in boss_fight_results.gear_loot:
                new_gear_text = f"**{g.name}. Navigate to your gear to equip it.**"
                rewards_text += "\n" + new_gear_text
                new_gear_embed = discord.Embed(
                    title="You found new gear!", color=discord.Color.green()
                )
                new_gear_embed.add_field(name="", value=new_gear_text)
                await interaction.response.send_message(
                    embed=new_gear_embed,
                    ephemeral=True,
                )
            if boss_fight_results.sold_gear_amount:
                rewards_text += f"\nYou found gear you already own. You gained **{boss_fight_results.sold_gear_amount}** gold instead."
            embed.add_field(
                name=f"💰VICTORY! You have defeated {bd.display_monster()}. Here are you rewards💰",
                value=rewards_text,
                inline=False,
            )

        # Set the cooldown for the attack button
        cd_embed_index = 3
        # Extract this to be reusable
        cd_type_text = "attack"
        if action == "cast_spell":
            cd_type_text = "cast your spell"
        embed.insert_field_at(
            cd_embed_index,
            name="",
            value=f"You can {cd_type_text} again {discord.utils.format_dt(boss_fight_results.cooldown_expiration, style='R')}",
            inline=False,
        )

        await interaction.response.edit_message(
            embed=embed, view=await self._create_view()
        )

        if boss_fight_results.leveled_up:
            level_up_embed = get_level_up_embed(
                exp_to_level(boss_fight_results.player_exp)
            )
            await interaction.followup.send(embed=level_up_embed, ephemeral=True)

    async def _create_boss_select_view(self):
        view = View(timeout=None)
        player = await self.cordia_service.get_player_by_discord_id(self.discord_id)
        current_level = exp_to_level(player.exp)

        bosses = [
            boss
            for boss in list(boss_data.keys())
            if current_level >= boss_data[boss].level - 10
        ][::-1]

        options = [
            discord.SelectOption(
                label=boss_data[boss].name,
                description=f"Unlocks at level {boss_data[boss].level - 10}",
                value=boss,
            )
            for boss in bosses
        ]

        boss_select = Select(
            placeholder="Select a boss", min_values=1, max_values=1, options=options
        )
        boss_select.callback = self.boss_select_callback

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=2)
        back_button.callback = self.back_button_callback
        view.add_item(boss_select)
        view.add_item(back_button)
        return view

    async def _create_view(self):
        view = View(timeout=None)

        attack_button = Button(label="Attack", style=discord.ButtonStyle.blurple, row=1)
        attack_button.callback = self.attack

        cast_spell_button = Button(
            label="Cast Spell", style=discord.ButtonStyle.blurple, row=1
        )
        cast_spell_button.callback = self.cast_spell
        player_gear = await self.cordia_service.get_player_gear(self.discord_id)
        weapon = self.cordia_service.get_weapon(player_gear)
        spell = gear_data[weapon.name].spell
        if not spell:
            cast_spell_button.disabled = True

        forfeit_boss_fight_button = Button(
            label="Forfeit Boss Fight", style=discord.ButtonStyle.red, row=1
        )
        forfeit_boss_fight_button.callback = self.forfeit_boss_fight_callback

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=2)
        back_button.callback = self.back_button_callback

        view.add_item(attack_button)
        view.add_item(cast_spell_button)
        view.add_item(forfeit_boss_fight_button)
        view.add_item(back_button)

        return view

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

    @only_command_invoker()
    async def boss_select_callback(self, interaction: discord.Interaction):
        await self.cordia_service.insert_boss(
            self.discord_id, interaction.data["values"][0]
        )
        await self.render(interaction)

    @only_command_invoker()
    async def forfeit_boss_fight_callback(self, interaction: discord.Interaction):
        await self.cordia_service.delete_boss(self.discord_id)
        await self.render(interaction)