from discord.ui import Select
import discord
from cordia.data.locations import location_data

class LocationSelect(Select):
    def __init__(self, level):

        # Reversed locations and filtered based on level
        locations = [location for location in list(location_data.keys()) if level >= location_data[location].level_unlock][::-1]
        options = [discord.SelectOption(label=location_data[location].name, description=f'Unlocks at level {location_data[location].level_unlock}', value=location) for location in locations]
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