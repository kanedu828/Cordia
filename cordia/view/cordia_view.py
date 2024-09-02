import discord
from discord.ui import Button, View
import asyncio
from cordia.view.location_select import LocationSelect
from cordia.service.cordia_service import CordiaService

class CordiaView(View):
    def __init__(self, cordia_service: CordiaService, discord_id: int):
        super().__init__(timeout=None)
        self.page = 'home'

        self.cordia_service = cordia_service

        self.discord_id = discord_id

        # Home page buttons
        attack_button = Button(label="Attack!", style=discord.ButtonStyle.green, custom_id="attack_button")
        self.add_item(attack_button)
            
    def exp_bar(self, exp, bar_length=10, filled_char="🟩", empty_char="⬜"):
        """
        Generate an experience bar using emojis or characters.

        :param exp: Current experience points of the user.
        :param bar_length: The total length of the bar (in characters or emojis).
        :param filled_char: Character or emoji to represent filled portions.
        :param empty_char: Character or emoji to represent empty portions.
        :return: A string representing the experience bar.
        """
        # Calculate the current level
        current_level = self.cordia_service.exp_to_level(exp)
        
        # Get the total experience for the current and next levels
        current_level_exp = self.cordia_service.level_to_exp(current_level)
        next_level_exp = self.cordia_service.level_to_exp(current_level + 1)
        
        # Calculate progress towards the next level
        exp_in_current_level = exp - current_level_exp
        exp_needed_for_next_level = next_level_exp - current_level_exp
        
        # Calculate the number of filled segments in the bar
        filled_length = int((exp_in_current_level / exp_needed_for_next_level) * bar_length)
        
        # Create the bar string
        bar = filled_char * filled_length + empty_char * (bar_length - filled_length)
        
        return f"**LV {current_level}** ({exp} exp)\n{bar}"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Check which button or select triggered the interaction
        if interaction.data.get("custom_id") == "attack_button":
            await self.attack(interaction)
        return True

    async def get_embed(self):
        # Place holder image. Replace per location later
        file = discord.File("assets/locations/the_plains.png", filename="the_plains.png")
        player = await self.cordia_service.get_or_insert_player(self.discord_id)
        embed = discord.Embed(
            title=f"Fighting Monsters in {player['location']}!",
        )
        embed.add_field(name="⚔️Battle⚔️", value="You defeat one goblin")
        embed.set_image(url="attachment://the_plains.png")
        return embed, file
    
    async def attack(self, interaction: discord.Interaction):
        attack_results = await self.cordia_service.attack(self.discord_id)

        current_exp = attack_results['player_exp']
        current_level = self.cordia_service.exp_to_level(current_exp)

        # Buttons for attack
        self.clear_items()
        attack_button = Button(label="Attack!", style=discord.ButtonStyle.green, custom_id="attack_button")
        self.add_item(LocationSelect(current_level))
        self.add_item(attack_button)
        
        embed = discord.Embed(
            title=f"Fighting Monsters in {attack_results['location']}",
        )


        stats_text = f"{self.exp_bar(current_exp)}\n"
        if attack_results['leveled_up']:
            stats_text += "✨You leveled up!✨\n"
        stats_text += "\n".join(f"{key.capitalize()}: {value}" for key, value in attack_results['player_stats'].items())

        embed.add_field(name="💪Player Stats💪", value=stats_text, inline=False)

        embed.set_image(url="attachment://the_plains.png")

        if attack_results['remaining_cooldown'] > 0:
            cooldown_text = "You are on cooldown. Please wait {:.2f} seconds.".format(attack_results['remaining_cooldown'])
            embed.add_field(name="🕒You're on cooldown!🕒", value=cooldown_text, inline=False)
            await interaction.response.edit_message(embed=embed, view=self)
            return
        
        if attack_results["kills"] == 0:
            battle_text = f"You tried to fight a **{attack_results['monster']}**, but you could not defeat it. Try again!"
        elif attack_results["kills"] == 1:
            battle_text = f"Using all your might, you defeat a **{attack_results['monster']}**"
        else:
            battle_text = f"In a show of grandeur, you defeat **{attack_results['kills']} {attack_results['monster']}s**"
        embed.add_field(name="⚔️Battle⚔️", value=battle_text, inline=False)

        rewards_text = f"{attack_results['exp']} Exp\n{attack_results['gold']} Gold"
        embed.add_field(name="💰Rewards💰", value=rewards_text, inline=False)

        
        
        # Set the cooldown for the attack button
        cooldown_seconds = attack_results['attack_cooldown']
        embed.set_footer(text=f"{cooldown_seconds} seconds until you can attack again")
        attack_button.disabled = True  # Disable the button

        # Update the message with initial embed and disabled button
        await interaction.response.edit_message(embed=embed, view=self)

        # Wait for the cooldown period to expire
        await asyncio.sleep(cooldown_seconds)

        # Re-enable the attack button and reset the label
        attack_button.disabled = False
        attack_button.label = "Attack!"

        
        await interaction.message.edit(view=self)

