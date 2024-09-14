from dataclasses import dataclass
from datetime import date


@dataclass()
class DailyLeaderboard:
    discord_id: int
    exp: int
    gold: int
    monsters_killed: int
    date: date
