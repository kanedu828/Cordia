from typing import List
from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance


# Duplicate of the one from cordia service. Should use this one
def get_weapon_from_player_gear(player_gear: List[GearInstance]) -> GearInstance:
    return next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)
