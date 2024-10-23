import re
import unittest
from cordia.data.achievements import achievement_data
from cordia.data.shop_items import shop_item_data
from cordia.data.items import item_data
from cordia.data.monsters import monster_data


class TestAchievementData(unittest.TestCase):

    def test_achievement_is_valid(self):
        for k in achievement_data.keys():
            with self.subTest(achievement=k):
                self.assertIn(k, monster_data)

    def test_has_only_one_stat(self):
        for k, i in achievement_data.items():
            with self.subTest(monster=k):
                i.stat_bonus.get_one_non_zero_stat()

    def test_key_matches_achievement_monster(self):
        for k, i in achievement_data.items():
            with self.subTest(achievement=k):
                expected_name = re.sub(r"_+", " ", k).title()
                self.assertEqual(expected_name, i.monster.title())


if __name__ == "__main__":
    unittest.main()
