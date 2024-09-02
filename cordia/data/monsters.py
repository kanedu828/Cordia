class Monster:
    def __init__(self, name, level, hp, gold, exp, loot=None):
        self.name = name
        self.level = level
        self.hp = hp
        self.gold = gold
        self.exp = exp
        self.loot = loot if loot is not None else []

    def display_monster(self):
        return f"[lv. {self.level}] {self.name}"

    def __repr__(self):
        return f"<Monster(name={self.name}, level={self.level}, hp={self.hp}, gold={self.gold}, exp={self.exp}, loot={self.loot})>"


monster_data = {
    'rat': Monster(name='Rat', level=1, hp=10, gold=2, exp=5),
    'goblin': Monster(name='Goblin', level=5, hp=15, gold=5, exp=8)
}
