from cordia.model.monster import Monster, MonsterType

monster_data = {
    'rat': Monster(name='Rat', level=1, hp=10, gold=2, exp=5),
    'goblin': Monster(name='Goblin', level=5, hp=15, gold=5, exp=8),
    'wolf': Monster(name='wolf', level=13, hp=20, gold=9, exp=15),
    'bear': Monster(name='bear', level=18, hp=33, gold=10, exp=25),
    'goblin_king': Monster(name='Goblin King', level=20, hp=1000, gold=100, exp=100, type=MonsterType.BOSS),
    'giant_spider': Monster(name='Giant Spider', level=25, hp=50, gold=20, exp=35),
    'dryad': Monster(name='Dryad', level=45, hp=120, gold=50, exp=60)

}
