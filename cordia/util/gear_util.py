from typing import List
from cordia.model.gear import GearType
from cordia.model.player_gear import PlayerGear

# Duplicate of the one from cordia service. Should use this one
def get_weapon_from_player_gear(player_gear: List[PlayerGear]) -> PlayerGear:
    return next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)