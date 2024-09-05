from cordia.model.location import Location

location_data = {
    'the_plains_i': Location(name='The Plains I', level_unlock=0, monsters=[('rat', 1.0)]),
    'the_plains_ii': Location(name='The Plains II', level_unlock=5, monsters=[('goblin', 0.25), ('rat', 0.75)]),
    'the_plains_iii': Location(name='The Plains III', level_unlock=10, monsters=[('goblin', 0.75), ('rat', 0.25)]),
    'the_forest_i': Location(name='The Forest I', level_unlock=15, monsters=[('wolf', 0.70), ('bear', 0.30)]),
    'the_forest_ii': Location(name='The Forest II', level_unlock=20, monsters=[('bear', 0.60), ('giant_spider', 0.40)]),
    'the_forest_iii': Location(name='The Forest III', level_unlock=25, monsters=[('giant_spider', 0.95), ('dryad', 0.05)])
}