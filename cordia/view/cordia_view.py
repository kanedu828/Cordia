import discord
from discord.ui import Button, View
from cordia.view.location_select import LocationSelect
from cordia.service.cordia_service import CordiaService

class CordiaView(View):
    def __init__(self, cordia_service: CordiaService, discord_id: int):
        super().__init__(timeout=None)
        self.page = 'home'

        self.cordia_service = cordia_service

        self.discord_id = discord_id

        self.add_item(LocationSelect())
        self.add_item(Button(label="Fight!", style=discord.ButtonStyle.green, custom_id="fight_button"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Check which button or select triggered the interaction
        if interaction.data.get("custom_id") == "fight_button":
            await self.fight(interaction)
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
    
    async def fight(self, interaction: discord.Interaction):
        player = await self.cordia_service.get_or_insert_player(self.discord_id)
        embed = discord.Embed(
            title=f"Fighting Monsters in {player['location']}!",
        )
        embed.add_field(name="⚔️Battle⚔️", value="You defeat one goblin")
        embed.set_image(url="attachment://the_plains.png")
        await interaction.response.edit_message(embed=embed, view=self)