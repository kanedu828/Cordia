# decorators.py
from functools import wraps
import discord


def only_command_invoker():
    """A decorator to ensure only the user who invoked the command can interact with the button."""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            # Check if the interaction user matches the original command invoker (discord_id)
            if interaction.user.id != self.discord_id:
                await interaction.response.send_message(
                    "You cannot interact with this.", ephemeral=True
                )
                return
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator
