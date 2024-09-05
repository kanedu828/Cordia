from cordia.model.location import Location

location_data = {
    'the_plains_i': Location(name='The Plains I', level_unlock=0, monsters=[('rat', 1.0)]),
    'the_plains_ii': Location(name='The Plains II', level_unlock=5, monsters=[('goblin', 0.25), ('rat', 0.75)]),
    'the_plains_iii': Location(name='The Plains III', level_unlock=10, monsters=[('goblin', 0.75), ('rat', 0.25)]),
    'the_forest_i': Location(name='The Forest I', level_unlock=15, monsters=[('wolf', 0.70), ('bear', 0.30)])
}