from cordia.service.cordia_service import CordiaService
from cordia.util.errors import InvalidItemError
from cordia.util.text_format_util import display_gold, get_stat_emoji
from discord.ui import Modal, TextInput
import discord
from cordia.data.items import item_data


class SellMarketItemModal(Modal):
    def __init__(self, cordia_service: CordiaService, discord_id: int):
        super().__init__(title="Sell Item")

        # Create a text input for the item to sell
        self.item_name_input = TextInput(label=f"Item name to sell")
        self.add_item(self.item_name_input)
        self.item_count_input = TextInput(label=f"Item count")
        self.add_item(self.item_count_input)
        self.item_price_input = TextInput(label=f"Price to sell (There will be a 5% tax)")
        self.add_item(self.item_price_input)

        self.discord_id = discord_id
        self.cordia_service = cordia_service

    async def on_submit(self, interaction: discord.Interaction):

        try:        
            # Handle the form submission
            item_name: str = self.item_name_input.value
            item_count = int(self.item_count_input.value)
            item_price = int(self.item_price_input.value)

            item_name_key = item_name.lower().replace(" ", "_")
            if item_name_key not in item_data:
                fail_embed = discord.Embed(
                    title=f"❌{item_name} is not a valid item", color=discord.Color.red(),
                    description="Make sure you use the singular name. e.g Ice Queen Soul instead of Ice Queen Souls"
                )
                await interaction.response.send_message(embed=fail_embed, ephemeral=True)
                return
            market_item = await self.cordia_service.market_service.list_market_item(self.discord_id, item_name_key, item_price, item_count)
            
            succeed_embed = discord.Embed(
                title=f"Successfully listed {market_item.display_item()} onto the market for {display_gold(item_price)}",
                color=discord.Color.green(),
            )

            from cordia.view.pages.market_page import MarketPage

            await MarketPage(self.cordia_service, self.discord_id).render(interaction)
            await interaction.followup.send(embed=succeed_embed, ephemeral=True)
        except InvalidItemError as e:
            fail_embed = discord.Embed(
            title=f"❌You do not have {item_count} {item_name.title()}.", color=discord.Color.red()
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
            return
        except Exception as e:
            print(e)
            fail_embed = discord.Embed(
                title=f"❌Please enter a valid price or count.", color=discord.Color.red()
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
            return
