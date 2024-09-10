import unittest
from cordia.data.locations import location_data
from cordia.data.monsters import monster_data

class TestLocationData(unittest.TestCase):
    
    def test_valid_monsters(self):
        """Test that all monsters in locations exist in monster_data."""
        for location, data in location_data.items():
            with self.subTest(location=location):
                for monster, _ in data.monsters:
                    self.assertIn(monster, monster_data, f"{monster} is missing from monster_data for location {location}")

    def test_monster_spawn_rate_add_to_100(self):
        """Test that monster spawn rates add up to 1.0 (100%) for each location."""
        for location, data in location_data.items():
            with self.subTest(location=location):
                total_rate = sum(spawn_rate for _, spawn_rate in data.monsters)
                self.assertAlmostEqual(total_rate, 1, places=5, msg=f"{location} monster spawn rate does not add up to 1.")

    def test_locations_ordered_by_level(self):
        """Test that the locations are ordered by level_unlock."""
        levels = [data.level_unlock for data in location_data.values()]
        self.assertEqual(levels, sorted(levels), "Locations are not ordered by level_unlock")

    def test_location_key_is_snake_case_and_name_is_capitalized(self):
        """Test that location keys are in snake_case and names have capitalized words with no underscores."""
        snake_case_pattern = r'^[a-z]+(_[a-z]+)*$'
        
        for location, data in location_data.items():
            with self.subTest(location=location):
                # Check if location key is in snake_case
                self.assertRegex(location, snake_case_pattern, f"{location} is not in snake_case")

                # Check if location name is capitalized correctly and has no underscores
                self.assertNotIn('_', data.name, f"{data.name} contains underscores, which is not allowed in names")
                
                # Check if each word in the name is capitalized
                words = data.name.split()
                for word in words:
                    self.assertTrue(word[0].isupper(), f"'{word}' in '{data.name}' is not capitalized properly")

if __name__ == "__main__":
    unittest.main()
