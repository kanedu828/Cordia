from cordia.model.item import Item


item_data = {
    "basic_core": Item(
        name="Basic Core", description="Grants a small amount of bonus stats to gear"
    ),
    "quality_core": Item(
        name="Quality Core",
        description="Grants a moderate amount of bonus stats to gear",
    ),
    "supreme_core": Item(
        name="Supreme Core",
        description="Grants a signifigant amount of bonus stats to gear",
    ),
    "chaos_core": Item(
        name="Chaos Core", description="Grants a great amount of bonus stats to gear"
    ),
    "basic_shard": Item(name="Basic Shard", description="Used to upgrade gear"),
    "quality_shard": Item(name="Quality Shard", description="Used to upgrade gear"),
    "supreme_shard": Item(name="Supreme Shard", description="Used to upgrade gear"),
    "chaos_shard": Item(name="Chaos Shard", description="Used to upgrade gear"),
}
