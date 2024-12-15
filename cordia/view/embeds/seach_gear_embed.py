import discord
from cordia.data.gear import gear_data
from cordia.model.gear_instance import GearInstance
from cordia.util.gear_util import display_gear_set_stats_for_set
from cordia.util.text_format_util import get_stars_string


def get_search_gear_embed(gear_name: str):
    gear_name = gear_name.lower().replace(" ", "_")
    if gear_name in gear_data:
        gd = gear_data[gear_name]
        embed = discord.Embed(
            title=f"lv.{gd.level} {gd.name}", color=discord.Color.blue()
        )

        embed.add_field(
            name="", value=get_stars_string(0, gd.get_max_stars()), inline=False
        )
        embed.add_field(
            name=f"**Type**: {gd.type.value.title()}", value="", inline=False
        )

        gi = GearInstance(0, 0, gear_name, 0, "", slot="")

        embed.add_field(name="", value=gi.get_main_stats_string(), inline=False)
        embed.add_field(name="", value=gi.get_secondary_stats_string(), inline=False)

        if gd.spell:
            embed.add_field(
                name=f"Spell: {gd.spell.name}",
                value=f"**Description:** {gd.spell.description}",
                inline=False,
            )
            embed.add_field(
                name="Spell Stats",
                value=gi.get_spell_stats_string(True),
                inline=False,
            )
        if gd.gear_set:
            gear_set_str = display_gear_set_stats_for_set(gd.gear_set, 0)
            embed.add_field(name="Gear Set", value=gear_set_str)
        return embed
    else:
        embed = discord.Embed(
            title=f"Cannot find gear",
            description="Incorrect gear name. Is it spelled correctly?",
            color=discord.Color.red(),
        )
        return embed
