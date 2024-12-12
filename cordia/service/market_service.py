import math
from cordia.dao.market_item_dao import MarketItemDao
from cordia.model.market_item import MarketItem
from cordia.service.item_service import ItemService
from cordia.service.player_service import PlayerService
from cordia.util.errors import InvalidItemError


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

    async def get_all_market_items(self) -> list[MarketItem]:
        """Retrieve all items currently in the market."""
        return await self.market_item_dao.get_all_market_items()

    async def buy_market_item(self, market_item_id: int, discord_id: int) -> MarketItem:
        """Remove an item from the market by its ID."""
        market_item = await self.market_item_dao.get_market_item_by_id(market_item_id)
        if not market_item:
            raise InvalidItemError("Item is not found market")
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
        return market_item

    async def list_market_item(
        self, discord_id: int, item_name: str, price: int, count: int
    ) -> MarketItem:
        """Add a new item to the market."""
        item = await self.item_service.get_item(discord_id, item_name)
        if not item:
            raise InvalidItemError("Item is not found in player inventory")
        await self.item_service.insert_item(
            discord_id, item_name, -count
        )  # Remove item from seller inventory
        return await self.market_item_dao.insert_market_item(
            discord_id, item_name, price, count
        )

    async def unlist_market_item(self, market_item_id: int) -> None:
        """Add a new item to the market."""
        market_item = await self.market_item_dao.get_market_item_by_id(market_item_id)
        await self.item_service.insert_item(
            market_item.discord_id, market_item.item_name, market_item.count
        )
        await self.market_item_dao.delete_market_item(market_item_id)

    async def find_items_by_name(self, item_name: str) -> list[MarketItem]:
        """Search for items in the market by their name."""
        return await self.market_item_dao.get_market_items_by_name(item_name)
