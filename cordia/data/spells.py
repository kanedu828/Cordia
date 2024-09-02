from enum import Enum


class SpellType(Enum):
    DAMAGE = "damage"
    BUFF = "buff"

class Spell:
    def __init__(self, spell_type: SpellType, name: str, description: str, damage: int, buff=''):
        self.spell_type = spell_type
        self.name = name
        self.description = description
        self.damage = damage
        self.buff = buff

    def __repr__(self):
        return f"<Spell(type={self.spell_type}, name={self.name}, damage={self.damage})>"