from dataclasses import dataclass
from typing import Literal

from cordia.model.player_stats import PlayerStats


@dataclass
class Achievement:
    monster: str = None
    stat_bonus: PlayerStats = None
    stat_modifier: Literal["+", "%"] = "+"
    monster_killed_increment: int = 100
