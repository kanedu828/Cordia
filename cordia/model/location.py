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
        image_file_name = self.get_image_file_name()
        image_path = f'https://kanedu828.github.io/cordia-assets/assets/locations/{image_file_name}'
        return image_path
    
    def get_image_file_name(self):
        # Convert to lowercase
        image_file_name = self.name.lower()
        # Replace spaces and any non-alphanumeric characters with underscores
        image_file_name = re.sub(r'[\s\W]+', '_', image_file_name)
        # Add the .png extension
        image_file_name += '.png'
        return image_file_name

    def get_random_monster(self) -> str:
        total = sum(weight for _, weight in self.monsters)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in self.monsters:
            if upto + weight >= r:
                return choice
            upto += weight
    
    def get_key_name(self) -> str:
        return re.sub(r'[\W_]+', '_', self.name.lower())
