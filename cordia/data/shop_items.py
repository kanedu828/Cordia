from cordia.model.shop_item import ShopItem, ShopItemType


shop_item_data: dict[str, ShopItem] = {
    "quality_core": ShopItem(
        item_name="quality_core", type=ShopItemType.ITEM, item_cost=("basic_core", 5)
    ),
    "supreme_core": ShopItem(
        item_name="supreme_core", type=ShopItemType.ITEM, item_cost=("quality_core", 5)
    ),
    "shadow_master_dagger": ShopItem(
        item_name="shadow_master_dagger",
        type=ShopItemType.GEAR,
        item_cost=("shadow_master_soul", 5),
    ),
    "shadow_master_bow": ShopItem(
        item_name="shadow_master_bow",
        type=ShopItemType.GEAR,
        item_cost=("shadow_master_soul", 5),
    ),
    "shadow_master_top": ShopItem(
        item_name="shadow_master_top",
        type=ShopItemType.GEAR,
        item_cost=("shadow_master_soul", 5),
    ),
    "shadow_master_pants": ShopItem(
        item_name="shadow_master_pants",
        type=ShopItemType.GEAR,
        item_cost=("shadow_master_soul", 5),
    ),
    "ice_queen_staff": ShopItem(
        item_name="ice_queen_staff",
        type=ShopItemType.GEAR,
        item_cost=("ice_queen_soul", 5),
    ),
    "ice_queen_blade": ShopItem(
        item_name="ice_queen_blade",
        type=ShopItemType.GEAR,
        item_cost=("ice_queen_soul", 5),
    ),
    "ice_queen_pendant": ShopItem(
        item_name="ice_queen_pendant",
        type=ShopItemType.GEAR,
        item_cost=("ice_queen_soul", 5),
    ),
    "ice_queen_ring": ShopItem(
        item_name="ice_queen_ring",
        type=ShopItemType.GEAR,
        item_cost=("ice_queen_soul", 5),
    ),
    "royal_crystal_helmet": ShopItem(
        item_name="royal_crystal_helmet",
        type=ShopItemType.GEAR,
        item_cost=("royal_crystal_guard_soul", 5),
    ),
    "royal_crystal_gloves": ShopItem(
        item_name="royal_crystal_gloves",
        type=ShopItemType.GEAR,
        item_cost=("royal_crystal_guard_soul", 5),
    ),
}
