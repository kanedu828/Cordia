import discord

async def edit_message_with_done(interaction: discord.Interaction, embed, view):
    # Check if the interaction has already been responded to
    if interaction.response.is_done():
        # If the interaction has been responded to, use followup to edit the message
        message = await interaction.original_response()
        await interaction.followup.edit_message(
            message_id=message.id, embed=embed, view=view
        )
    else:
        # Otherwise, respond to the interaction by editing the message
        await interaction.response.edit_message(embed=embed, view=view)
