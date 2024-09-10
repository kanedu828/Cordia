import unittest
import re
from cordia.model.gear import Gear, GearType
from cordia.data.gear_types.weapons import weapon_data
from cordia.data.gear_types.cape import cape_data
from cordia.data.gear_types.hats import hat_data
from cordia.data.gear_types.pants import pants_data
from cordia.data.gear_types.pendant import pendant_data
from cordia.data.gear_types.rings import ring_data
from cordia.data.gear_types.shoes import shoes_data
from cordia.data.gear_types.tops import top_data
from cordia.data.gear_types.gloves import glove_data
from cordia.data.gear import gear_data

class TestGearData(unittest.TestCase):

    def test_key_matches_name_in_title_case(self):
        """Test that the snake case key is equivalent to the name in title case."""
        for key, gear in gear_data.items():
            with self.subTest(gear=key):
                # Convert snake_case key to title case
                expected_name = re.sub(r'_+', ' ', key).title()
                self.assertEqual(gear.name, expected_name, f"Key '{key}' does not match gear name '{gear.name}' in title case")

    def test_gear_in_cape_data(self):
        """Test that all gear in cape_data is of type GearType.CAPE."""
        for key, gear in cape_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.CAPE, f"{gear.name} in cape_data should have GearType.CAPE but has {gear.type}")
    
    def test_gear_in_weapon_data(self):
        """Test that all gear in weapon_data is of type GearType.WEAPON."""
        for key, gear in weapon_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.WEAPON, f"{gear.name} in weapon_data should have GearType.WEAPON but has {gear.type}")

    def test_gear_in_hat_data(self):
        """Test that all gear in hat_data is of type GearType.HAT."""
        for key, gear in hat_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.HAT, f"{gear.name} in hat_data should have GearType.HAT but has {gear.type}")

    def test_gear_in_pants_data(self):
        """Test that all gear in pants_data is of type GearType.PANTS."""
        for key, gear in pants_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.PANTS, f"{gear.name} in pants_data should have GearType.PANTS but has {gear.type}")
    
    def test_gear_in_pendant_data(self):
        """Test that all gear in pendant_data is of type GearType.PENDANT."""
        for key, gear in pendant_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.PENDANT, f"{gear.name} in pendant_data should have GearType.PENDANT but has {gear.type}")
    
    def test_gear_in_ring_data(self):
        """Test that all gear in ring_data is of type GearType.RING."""
        for key, gear in ring_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.RING, f"{gear.name} in ring_data should have GearType.RING but has {gear.type}")
    
    def test_gear_in_shoes_data(self):
        """Test that all gear in shoes_data is of type GearType.SHOES."""
        for key, gear in shoes_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.SHOES, f"{gear.name} in shoes_data should have GearType.SHOES but has {gear.type}")
    
    def test_gear_in_top_data(self):
        """Test that all gear in top_data is of type GearType.TOP."""
        for key, gear in top_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.TOP, f"{gear.name} in top_data should have GearType.TOP but has {gear.type}")
    
    def test_gear_in_glove_data(self):
        """Test that all gear in glove_data is of type GearType.GLOVES."""
        for key, gear in glove_data.items():
            with self.subTest(gear=key):
                self.assertEqual(gear.type, GearType.GLOVES, f"{gear.name} in glove_data should have GearType.GLOVES but has {gear.type}")

if __name__ == "__main__":
    unittest.main()
