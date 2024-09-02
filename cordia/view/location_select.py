from discord.ui import Select
import discord
from cordia.data.locations import locations

class LocationSelect(Select):
    def __init__(self):

        options = [discord.SelectOption(label=location, description=f'Unlocked at level {locations[location]["level_unlock"]}', value=location) for location in list(locations.keys())]

        super().__init__(
            placeholder='Select a location',
            min_values=1,
            max_values=1,
            options=options,
        )    

    async def callback(self, interaction: discord.Interaction):
        if self.view is not None:
            await self.view.cordia_service.update_location(interaction.user.id, self.values[0])
            embed, _ = await self.view.get_embed()
            await interaction.response.edit_message(embed=embed, view=self.view)