from dataclasses import dataclass, field
from enum import Enum
import random
from typing import List, Tuple

from cordia.model.gear import Gear
from cordia.data.gear import gear_data
from cordia.model.item import Item


class MonsterType(Enum):
    NORMAL = "normal"
    BOSS = "boss"


@dataclass(frozen=True, kw_only=True)
class Monster:
    name: str
    level: int
    hp: int
    gold: int
    exp: int
    type: MonsterType = MonsterType.NORMAL
    defense: int = 0
    resistance: int = 0
    item_loot: List[Tuple[str, float]] = field(default_factory=list)
    gear_loot: List[Tuple[str, float]] = field(default_factory=list)

    def display_monster(self) -> str:
        return f"[lv. {self.level}] {self.name}"

    # CHANGE THIS TO GET THE ITEM CLASS
    def get_dropped_items(self) -> List[str]:
        dropped_items = []
        for item, drop_rate in self.item_loot:
            if (
                random.random() <= drop_rate
            ):  # Check if the item drops based on probability
                dropped_items.append(item)
        return dropped_items

    def get_dropped_gear(self) -> List[str]:
        dropped_gear = []
        for g, drop_rate in self.gear_loot:
            if (
                random.random() <= drop_rate
            ):  # Check if the item drops based on probability
                dropped_gear.append(g)
        return dropped_gear
