from dataclasses import dataclass, field
from enum import Enum
import random
import re
from typing import List, Tuple


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
    defense: int = 0  # Defense from 0-100
    resistance: int = 0  # Resisteance from 0-100
    item_loot: List[Tuple[str, float]] = field(default_factory=list)
    gear_loot: List[Tuple[str, float]] = field(default_factory=list)

    def display_monster(self) -> str:
        return f"[lv. {self.level}] {self.name}"

    def get_image_path(self):
        image_file_name = self.get_image_file_name()
        image_path = (
            f"https://kanedu828.github.io/cordia-assets/assets/bosses/{image_file_name}"
        )
        return image_path

    def get_image_file_name(self):
        # Convert to lowercase
        image_file_name = self.name.lower()
        # Replace spaces and any non-alphanumeric characters with underscores
        image_file_name = re.sub(r"[\s\W]+", "_", image_file_name)
        # Add the .png extension
        image_file_name += ".png"
        return image_file_name

    def get_dropped_items(self, kills: int = 1) -> List[Tuple[str, int]]:
        """
        Returns a tuple containing (item_key, count)
        """
        dropped_items = []
        item_loot = self.item_loot
        # All monsters drop cores by default
        if self.type == MonsterType.NORMAL:
            item_loot += [
                ("basic_core", 0.02),
                ("quality_core", 0.01),
                ("supreme_core", 0.005),
            ]
        elif self.type == MonsterType.BOSS:
            item_loot += [
                ("basic_core", 0.50),
                ("quality_core", 0.25),
                ("supreme_core", 0.12),
                ("chaos_core", 0.06),
            ]
        for item, drop_rate in item_loot:
            count = 0
            for _ in range(kills):
                if (
                    random.random() <= drop_rate
                ):  # Check if the item drops based on probability
                    count += 1
            if count:
                dropped_items.append((item, count))
        return dropped_items

    def get_dropped_gear(self, kills: int = 1) -> List[str]:
        dropped_gear = []
        for g, drop_rate in self.gear_loot:
            for _ in range(kills):
                if (
                    random.random() <= drop_rate
                ):  # Check if the item drops based on probability
                    dropped_gear.append(g)
                    break
        return dropped_gear
