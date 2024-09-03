from dataclasses import dataclass
import random
from typing import List, Tuple

@dataclass(frozen=True, kw_only=True)
class Location:
    name: str
    level_unlock: int
    # Expecting a list of tuples with (monster_name, probability)
    monsters: List[Tuple[str, float]]

    def get_random_monster(self) -> str:
        total = sum(weight for _, weight in self.monsters)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in self.monsters:
            if upto + weight >= r:
                return choice
            upto += weight
    