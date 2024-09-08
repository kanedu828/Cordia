import discord
from cordia.data.locations import location_data
from cordia.data.bosses import boss_data


def get_level_up_embed(
    self,
    current_level: int,
):
    unlocked_locations = {
        key: location
        for key, location in location_data.items()
        if (lambda loc: loc.level_unlock == current_level)(location)
    }
    unlocked_bosses = {
        key: boss
        for key, boss in boss_data.items()
        if (lambda b: b.level - 10 == current_level)(boss)
    }
    if unlocked_locations:
        new_locations_text = "\n".join(
            f"**{location.name}**" for location in unlocked_locations.values()
        )
    else:
        new_locations_text = "No new locations unlocked."
    if unlocked_bosses:
        new_bosses_text = "\n".join(
            f"**{location.name}**" for location in unlocked_locations.values()
        )
    else:
        new_bosses_text = "No new bosses unlocked."

    level_up_embed = discord.Embed(
        title=f"✨You leveled up to level {current_level}!✨",
        color=discord.Color.blue(),
    )
    level_up_embed.add_field(
        name="Go to your stats page to use your upgrade points!",
        value="",
        inline=False,
    )
    level_up_embed.add_field(
        name="You unlocked the following new locations:",
        value=new_locations_text,
        inline=False,
    )
    level_up_embed.add_field(
        name="You unlocked the following new bosses:",
        value=new_bosses_text,
        inline=False,
    )
    return level_up_embed
