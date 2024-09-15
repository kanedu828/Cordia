from dataclasses import dataclass


@dataclass()
class PlayerStats:
    """Stats used in combat"""

    strength: int = 0
    persistence: int = 0
    intelligence: int = 0
    efficiency: int = 0
    luck: int = 0
    damage: int = 0
    boss_damage: int = 0
    crit_chance: int = 0
    penetration: int = 0
    combo_chance: int = 0
    strike_radius: int = 0
    attack_cooldown: int = 0
    spell_damage: int = 0

    def __add__(self, other: "PlayerStats") -> "PlayerStats":
        if not isinstance(other, PlayerStats):
            return NotImplemented

        return PlayerStats(
            strength=self.strength + other.strength,
            persistence=self.persistence + other.persistence,
            intelligence=self.intelligence + other.intelligence,
            efficiency=self.efficiency + other.efficiency,
            luck=self.luck + other.luck,
            damage=self.damage + other.damage,
            boss_damage=self.boss_damage + other.boss_damage,
            crit_chance=self.crit_chance + other.crit_chance,
            penetration=self.penetration + other.penetration,
            combo_chance=self.combo_chance + other.combo_chance,
            strike_radius=self.strike_radius + other.strike_radius,
            attack_cooldown=self.attack_cooldown + other.attack_cooldown,
            spell_damage=self.spell_damage + other.spell_damage,
        )
