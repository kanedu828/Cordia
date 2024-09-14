from discord.ui import Modal, TextInput
import discord


class ConfirmationModal(Modal):
    def __init__(self, confirmation_message: str, callback):
        super().__init__(title="Confirm Action")

        # Create a text input for the value to update
        self.confirm_input = TextInput(label=f'Type "confirm" to confirm')
        self.add_item(self.confirm_input)
        self.callback = callback
        self.confirmation_message = confirmation_message

    async def on_submit(self, interaction: discord.Interaction):
        # Handle the form submission, e.g., update the player's stats
        confirm_value: str = self.confirm_input.value

        if confirm_value.lower() == "confirm":
            await self.callback()
            embed = discord.Embed(
                title=f"{self.confirmation_message}", color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            fail_embed = discord.Embed(
                title=f'❌You did not correctly type "confirm".',
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
