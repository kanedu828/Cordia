from cordia.model.item import Item


item_data = {
    "basic_core": Item(
        name="Basic Core", description="Grants a small amount of bonus stats to gear", emoji="<:cordia_basic_core:1284033683040374825>"
    ),
    "quality_core": Item(
        name="Quality Core",
        description="Grants a moderate amount of bonus stats to gear", emoji="<:cordia_quality_core:1284033701465817149>",
    ),
    "supreme_core": Item(
        name="Supreme Core",
        description="Grants a signifigant amount of bonus stats to gear", emoji="<:cordia_supreme_core:1284035452675817494>",
    ),
    "chaos_core": Item(
        name="Chaos Core", description="Grants a great amount of bonus stats to gear", emoji="<:cordia_chaos_core:1284035789138952284>"
    ),
    "basic_shard": Item(name="Basic Shard", description="Used to upgrade gear"),
    "quality_shard": Item(name="Quality Shard", description="Used to upgrade gear"),
    "supreme_shard": Item(name="Supreme Shard", description="Used to upgrade gear"),
    "chaos_shard": Item(name="Chaos Shard", description="Used to upgrade gear"),

    "ice_queen_soul": Item(name="Ice Queen Soul", description="Used to purchase certain gear"),
    "shadow_master_soul": Item(name="Shadow Master Soul", description="Used to purchase certain gear"),
}
