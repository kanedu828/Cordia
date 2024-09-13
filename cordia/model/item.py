from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Item:
    name: str
    description: str = ""
    emoji: str = "<:cordia_generic_item:1284032229999378473>"

    def display_item(self):
        return f"{self.emoji} **{self.name}**"
