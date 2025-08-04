import logging
import math
from cordia.dao.market_item_dao import MarketItemDao
from cordia.model.market_item import MarketItem
from cordia.service.item_service import ItemService
from cordia.service.player_service import PlayerService
from cordia.util.errors import InvalidItemError, NotEnoughItemsError, InvalidInputError

# Set up logger for this module
logger = logging.getLogger(__name__)


class MarketService:
    def __init__(
        self,
        market_item_dao: MarketItemDao,
        item_service: ItemService,
        player_service: PlayerService,
    ):
        self.market_item_dao = market_item_dao
        self.item_service = item_service
        self.player_service = player_service
        logger.info("MarketService initialized")

    async def get_all_market_items(self) -> list[MarketItem]:
        """Retrieve all items currently in the market."""
        logger.debug("Getting all market items")
        items = await self.market_item_dao.get_all_market_items()
        logger.debug(f"Retrieved {len(items)} market items")
        return items

    async def buy_market_item(self, market_item_id: int, discord_id: int) -> MarketItem:
        """Remove an item from the market by its ID."""
        logger.info(f"User {discord_id} buying market item {market_item_id}")
        market_item = await self.market_item_dao.get_market_item_by_id(market_item_id)
        if not market_item:
            logger.error(f"Market item {market_item_id} not found")
            raise InvalidItemError("Item is not found market")
        
        logger.debug(f"Market item {market_item_id}: {market_item.item_name} x{market_item.count} for {market_item.price} gold")
        
        await self.player_service.increment_gold(discord_id, -market_item.price)
        await self.item_service.insert_item(
            discord_id, market_item.item_name, market_item.count
        )

        TAX_RATE = 0.05
        tax_adjusted_price = math.ceil(market_item.price - market_item.price * TAX_RATE)
        await self.player_service.increment_gold(
            market_item.discord_id, tax_adjusted_price
        )

        await self.market_item_dao.delete_market_item(market_item_id)
        logger.info(f"Completed market purchase: user {discord_id} bought {market_item.item_name} x{market_item.count} for {market_item.price} gold, seller received {tax_adjusted_price} gold")
        return market_item

    async def list_market_item(
        self, discord_id: int, item_name: str, price: int, count: int
    ) -> MarketItem:
        """Add a new item to the market."""
        logger.info(f"User {discord_id} listing market item: {item_name} x{count} for {price} gold")
        
        if count < 1:
            logger.error(f"Invalid count for user {discord_id}: {count}")
            raise InvalidItemError("Input cannot be less than 1.")
        
        item = await self.item_service.get_item(discord_id, item_name)
        if not item:
            logger.error(f"Item not found in inventory for user {discord_id}: {item_name}")
            raise NotEnoughItemsError("Item is not found in player inventory")
        
        if price < 0:
            logger.error(f"Invalid price for user {discord_id}: {price}")
            raise InvalidInputError("Price can not be lower than 0")
        
        await self.item_service.insert_item(
            discord_id, item_name, -count
        )  # Remove item from seller inventory
        market_item = await self.market_item_dao.insert_market_item(
            discord_id, item_name, price, count
        )
        logger.info(f"Listed market item: user {discord_id} listed {item_name} x{count} for {price} gold")
        return market_item

    async def unlist_market_item(self, market_item_id: int) -> None:
        """Add a new item to the market."""
        logger.info(f"Unlisting market item {market_item_id}")
        market_item = await self.market_item_dao.get_market_item_by_id(market_item_id)
        await self.item_service.insert_item(
            market_item.discord_id, market_item.item_name, market_item.count
        )
        await self.market_item_dao.delete_market_item(market_item_id)
        logger.info(f"Unlisted market item {market_item_id}: returned {market_item.item_name} x{market_item.count} to user {market_item.discord_id}")

    async def find_items_by_name(self, item_name: str) -> list[MarketItem]:
        """Search for items in the market by their name."""
        logger.debug(f"Searching market items by name: {item_name}")
        items = await self.market_item_dao.get_market_items_by_name(item_name)
        logger.debug(f"Found {len(items)} market items matching '{item_name}'")
        return items

    def get_market_stats(self) -> dict:
        """Get statistics about market operations for monitoring."""
        stats = {
            "service_name": "MarketService"
        }
        logger.debug(f"Market service stats: {stats}")
        return stats
