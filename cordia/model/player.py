from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
    discord_id: int
    strength: int
    persistence: int
    intelligence: int
    efficiency: int
    luck: int
    exp: int
    gold: int
    location: str