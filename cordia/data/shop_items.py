from cordia.model.shop_item import ShopItem, ShopItemType


shop_item_data: dict[str, ShopItem] = {
    "quality_core": ShopItem(
        item_name="quality_core", type=ShopItemType.ITEM, item_cost=("basic_core", 5)
    ),
    "quality_core_x10": ShopItem(
        item_name="quality_core",
        type=ShopItemType.ITEM,
        item_cost=("basic_core", 50),
        item_quantity=10,
    ),
    "supreme_core": ShopItem(
        item_name="supreme_core", type=ShopItemType.ITEM, item_cost=("quality_core", 5)
    ),
    "supreme_core_x10": ShopItem(
        item_name="supreme_core",
        type=ShopItemType.ITEM,
        item_cost=("quality_core", 50),
        item_quantity=10,
    ),
    "chaos_shard": ShopItem(
        item_name="chaos_shard",
        type=ShopItemType.ITEM,
        item_cost=("shard", 100),
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
    "volcanic_top": ShopItem(
        item_name="volcanic_top",
        type=ShopItemType.GEAR,
        item_cost=("volcanic_salamander_tail", 5),
        gold_cost=20000,
    ),
    "volcanic_pants": ShopItem(
        item_name="volcanic_pants",
        type=ShopItemType.GEAR,
        item_cost=("volcanic_salamander_tail", 5),
        gold_cost=20000,
    ),
    "soul_stealer_katana": ShopItem(
        item_name="soul_stealer_katana",
        type=ShopItemType.GEAR,
        item_cost=("soul_stealer_soul", 5),
        gold_cost=50000,
    ),
    "soul_stealer_scepter": ShopItem(
        item_name="soul_stealer_scepter",
        type=ShopItemType.GEAR,
        item_cost=("soul_stealer_soul", 5),
        gold_cost=50000,
    ),
    "soul_stealer_pendant": ShopItem(
        item_name="soul_stealer_pendant",
        type=ShopItemType.GEAR,
        item_cost=("soul_stealer_soul", 5),
        gold_cost=50000,
    ),
    "soul_stealer_ring": ShopItem(
        item_name="soul_stealer_ring",
        type=ShopItemType.GEAR,
        item_cost=("soul_stealer_soul", 5),
        gold_cost=50000,
    ),
    "mystical_guardian_hammer": ShopItem(
        item_name="mystical_guardian_hammer",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_bow": ShopItem(
        item_name="mystical_guardian_bow",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_staff": ShopItem(
        item_name="mystical_guardian_staff",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_mage_hat": ShopItem(
        item_name="mystical_guardian_mage_hat",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_hunter_hat": ShopItem(
        item_name="mystical_guardian_hunter_hat",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_mage_top": ShopItem(
        item_name="mystical_guardian_mage_top",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_hunter_top": ShopItem(
        item_name="mystical_guardian_hunter_top",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_mage_pants": ShopItem(
        item_name="mystical_guardian_mage_pants",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_hunter_pants": ShopItem(
        item_name="mystical_guardian_hunter_pants",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_mage_shoes": ShopItem(
        item_name="mystical_guardian_mage_shoes",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "mystical_guardian_hunter_shoes": ShopItem(
        item_name="mystical_guardian_hunter_shoes",
        type=ShopItemType.GEAR,
        item_cost=("mystical_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_shark_tooth": ShopItem(
        item_name="ancient_ocean_guardian_shark_tooth",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_sword": ShopItem(
        item_name="ancient_ocean_guardian_sword",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_warrior_hat": ShopItem(
        item_name="ancient_ocean_guardian_warrior_hat",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_assassin_hat": ShopItem(
        item_name="ancient_ocean_guardian_assassin_hat",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_warrior_top": ShopItem(
        item_name="ancient_ocean_guardian_warrior_top",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_assassin_top": ShopItem(
        item_name="ancient_ocean_guardian_assassin_top",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_warrior_pants": ShopItem(
        item_name="ancient_ocean_guardian_warrior_pants",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_assassin_pants": ShopItem(
        item_name="ancient_ocean_guardian_assassin_pants",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_warrior_shoes": ShopItem(
        item_name="ancient_ocean_guardian_warrior_shoes",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "ancient_ocean_guardian_assassin_shoes": ShopItem(
        item_name="ancient_ocean_guardian_assassin_shoes",
        type=ShopItemType.GEAR,
        item_cost=("ancient_ocean_guardian_soul", 5),
        gold_cost=100000,
    ),
    "olympian_sword": ShopItem(
        item_name="olympian_sword",
        type=ShopItemType.GEAR,
        item_cost=("olympian_soul", 5),
        gold_cost=100000,
    ),
    "olympian_bow": ShopItem(
        item_name="olympian_bow",
        type=ShopItemType.GEAR,
        item_cost=("olympian_soul", 5),
        gold_cost=1_000_000,
    ),
    "olympian_spellbook": ShopItem(
        item_name="olympian_spellbook",
        type=ShopItemType.GEAR,
        item_cost=("olympian_soul", 5),
        gold_cost=1_000_000,
    ),
    "olympian_dagger": ShopItem(
        item_name="olympian_dagger",
        type=ShopItemType.GEAR,
        item_cost=("olympian_soul", 5),
        gold_cost=1_000_000,
    ),
}
