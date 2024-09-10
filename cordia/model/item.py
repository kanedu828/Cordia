from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Item:
    name: str
    description: str = ""
