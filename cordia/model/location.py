from dataclasses import dataclass
import random
import re
from typing import List, Tuple

@dataclass(frozen=True, kw_only=True)
class Location:
    name: str
    level_unlock: int
    # Expecting a list of tuples with (monster_name, probability)
    monsters: List[Tuple[str, float]]

    def get_image_path(self):
        # Convert to lowercase
        formatted_string = self.name.lower()
        # Replace spaces and any non-alphanumeric characters with underscores
        formatted_string = re.sub(r'[\s\W]+', '_', formatted_string)
        # Add the .png extension
        formatted_string += '.png'
        return formatted_string

    def get_random_monster(self) -> str:
        total = sum(weight for _, weight in self.monsters)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in self.monsters:
            if upto + weight >= r:
                return choice
            upto += weight
    