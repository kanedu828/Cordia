from cordia.model.monster import Monster, MonsterType

monster_data = {
    'rat': Monster(name='Rat', level=1, hp=10, gold=2, exp=5),
    'goblin': Monster(name='Goblin', level=5, hp=15, gold=5, exp=8),
    'goblin_king': Monster(name='Goblin King', level=20, hp=1000, gold=100, exp=100, type=MonsterType.BOSS),
}
