from dataclasses import dataclass

from cordia.model.gear import Gear
from cordia.data.gear import gear_data


# DEPRECATED. Delete
@dataclass(frozen=True)
class PlayerGear:
    id: int
    discord_id: int
    gear_id: int
    slot: str
    name: str
    stars: int
    bonus: str

    def get_gear_data(self) -> Gear:
        return gear_data[self.name]
