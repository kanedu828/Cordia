from dataclasses import dataclass
from datetime import datetime

from cordia.data.achievements import achievement_data


@dataclass()
class AchievementInstance:
    id: int
    discord_id: int
    monster: str
    count: int
    created_at: datetime
    updated_at: datetime

    def get_achievement_data(self):
        return achievement_data[self.monster]
