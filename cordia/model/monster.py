from dataclasses import dataclass, field
from enum import Enum
from typing import List


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
    loot: List[str] = field(default_factory=list)

    def display_monster(self) -> str:
        return f"[lv. {self.level}] {self.name}"