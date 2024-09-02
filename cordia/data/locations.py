import random


class Location:
    def __init__(self, name, level_unlock, monsters):
        self.name = name
        self.level_unlock = level_unlock
        # Expecting a list of tuples with (monster_name, probability)
        self.monsters = monsters
    
    def get_random_monster(self):
        total = sum(weight for choice, weight in self.monsters)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in self.monsters:
            if upto + weight >= r:
                return choice
            upto += weight

    def __repr__(self):
        return (f"<Location(name={self.name}, level_unlock={self.level_unlock}, "
                f"monsters={self.monsters})>")
    
location_data = {
    'the_plains_i': Location(name='The Plains I', level_unlock=0, monsters=[('rat', 1.0)]),
    'the_plains_ii': Location(name='The Plains II', level_unlock=5, monsters=[('goblin', 0.25), ('rat', 0.75)]),
    'the_plains_iii': Location(name='The Plains III', level_unlock=10, monsters=[('goblin', 0.75), ('rat', 0.25)]),
}