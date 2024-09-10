from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Item:
    name: str
    description: str = ""
    emoji: str = ""

    def display_item(self):
        return f"{self.emoji} **{self.name}**"
