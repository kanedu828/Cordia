import unittest
import re
from cordia.model.monster import Monster, MonsterType
from cordia.data.monsters import monster_data  # Existing regular monster data
from cordia.data.bosses import boss_data  # Importing the boss data for testing
from cordia.data.gear import gear_data  # For gear_loot validation


class TestMonsterData(unittest.TestCase):

    def test_gear_loot_is_valid(self):
        """Test that all gear_loot items exist in gear_data."""
        for monster_key, monster in {**monster_data, **boss_data}.items():
            with self.subTest(monster=monster_key):
                for gear_item, _ in monster.gear_loot:
                    self.assertIn(
                        gear_item,
                        gear_data,
                        f"{gear_item} from {monster_key} is missing in gear_data",
                    )

    def test_monster_name_is_title_case(self):
        """Test that monster names are the title case version of their keys."""
        for monster_key, monster in {**monster_data, **boss_data}.items():
            with self.subTest(monster=monster_key):
                # Convert the key from snake_case to Title Case for comparison
                expected_name = re.sub(r"_+", " ", monster_key).title()
                self.assertEqual(
                    monster.name,
                    expected_name,
                    f"{monster_key}'s name should be {expected_name}, but got {monster.name}",
                )

    def test_defense_and_resistance(self):
        """Test that defense and resistance attributes are less than or equal to 100."""
        for monster_key, monster in {**monster_data, **boss_data}.items():
            with self.subTest(monster=monster_key):
                # Check if defense exists and is <= 100
                if hasattr(monster, "defense"):
                    self.assertLessEqual(
                        monster.defense,
                        100,
                        f"{monster_key} defense is greater than 100",
                    )

                # Check if resistance exists and is <= 100
                if hasattr(monster, "resistance"):
                    self.assertLessEqual(
                        monster.resistance,
                        100,
                        f"{monster_key} resistance is greater than 100",
                    )

    def test_boss_monsters_are_of_type_boss(self):
        """Test that all monsters in boss_data are of type MonsterType.BOSS."""
        for boss_key, boss in boss_data.items():
            with self.subTest(boss=boss_key):
                self.assertEqual(
                    boss.type,
                    MonsterType.BOSS,
                    f"{boss.name} should be of type BOSS but has {boss.type}",
                )


if __name__ == "__main__":
    unittest.main()
