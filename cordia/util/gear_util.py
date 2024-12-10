from collections import Counter
from typing import List
from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.model.player_gear import PlayerGear
from cordia.data.gear_sets import gear_set_data
from cordia.util.stat_mapping import get_stat_emoji


# Duplicate of the one from cordia service. Should use this one
def get_weapon_from_player_gear(player_gear: List[GearInstance]) -> GearInstance:
    return next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)


def get_gear_set_count(player_gear: list[PlayerGear]) -> dict[str, int]:
    gear_set_count = Counter()
    for pg in player_gear:
        gd = pg.get_gear_data()
        if gd.gear_set:
            gear_set_count[gd.gear_set] += 1
    return gear_set_count


def display_gear_set_stats_for_set(gear_set_name: str, gear_equipped: int) -> str:
    """
    Displays the stats gained for each number of gear equipped for a specific gear set,
    highlighting the active effects based on the number of gear equipped.

    Args:
        gear_set_name (str): The name of the gear set to display.
        gear_equipped (int): The number of gear pieces currently equipped.

    Returns:
        str: A formatted string showing the stats for the specified gear set.
    """
    if gear_set_name not in gear_set_data:
        return f"Gear set '{gear_set_name}' not found."

    output = []
    levels = gear_set_data[gear_set_name]

    for pieces_equipped, stats in sorted(levels.items()):
        is_active = gear_equipped >= pieces_equipped
        status = "✅" if is_active else "❌"
        output.append(f"- {status} **{pieces_equipped} Piece(s) Equipped**")
        if all(value == 0 for value in stats.__dict__.values()):
            output.append("  - No bonus stats")
        else:
            output.extend(
                [
                    f"  - +{value} {get_stat_emoji(name)}{name.replace('_', ' ').title()}"
                    for name, value in stats.__dict__.items()
                    if value != 0
                ]
            )

    return "\n".join(output)
