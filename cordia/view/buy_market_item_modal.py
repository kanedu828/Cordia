import math
from cordia.service.cordia_service import CordiaManager
from cordia.util.errors import InvalidItemError, NotEnoughGoldError
from cordia.util.text_format_util import display_gold
from discord.ui import Modal, TextInput
import discord
from cordia.data.items import item_data


class BuyMarketItemModal(Modal):
    def __init__(self, cordia_service: CordiaManager, discord_id: int):
        super().__init__(title="Buy Item")

        # Create a text input for the item to buy
        self.market_item_id_input = TextInput(label=f"Market Item ID To Buy")
        self.add_item(self.market_item_id_input)

        self.discord_id = discord_id
        self.cordia_service = cordia_service

    async def on_submit(self, interaction: discord.Interaction):
        # Handle the form submission
        market_item_id: str = self.market_item_id_input.value

        try:
            market_item = await self.cordia_service.market_service.buy_market_item(
                int(market_item_id), self.discord_id
            )
            succeed_embed = discord.Embed(
                title="Success",
                description=f"Successfully bought {market_item.display_item()} from the market for {display_gold(market_item.price)}",
                color=discord.Color.green(),
            )

            from cordia.view.pages.market_page import MarketPage

            await MarketPage(self.cordia_service, self.discord_id).render(interaction)

            await interaction.followup.send(embed=succeed_embed, ephemeral=True)

            TAX_RATE = 0.05
            succeed_sell_embed = discord.Embed(
                title=f"Successfully sold {market_item.display_item()} from the market",
                description=f"Sale Price: {display_gold(market_item.price)}\n Tax: -{display_gold(market_item.price * TAX_RATE)}\n Your Gain: {display_gold(math.ceil(market_item.price - market_item.price * TAX_RATE))}",
                color=discord.Color.green(),
            )
            try:
                seller = await self.cordia_service.bot.fetch_user(market_item.discord_id)
                await seller.send(embed=succeed_sell_embed)
            except discord.NotFound:
                # Seller account no longer exists or bot can't access it
                pass
            except discord.Forbidden:
                # Seller has DMs disabled
                pass
            except Exception as e:
                # Other errors - log but don't fail the transaction
                print(f"Failed to notify seller {market_item.discord_id}: {e}")
        except NotEnoughGoldError as e:
            fail_embed = discord.Embed(
                title="Error",
                description=f"❌You do not have enough gold to purchase this item",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
            return
        except InvalidItemError as e:
            fail_embed = discord.Embed(
                title="Error",
                description=f"❌Please enter a valid market item",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=fail_embed, ephemeral=True)
            return
