import unittest
import re
from cordia.data.items import (
    item_data,
)  # Assuming item_data is imported from the correct module


class TestItemData(unittest.TestCase):

    def test_key_matches_name_in_title_case(self):
        """Test that the snake case key is equivalent to the name in title case."""
        for key, item in item_data.items():
            with self.subTest(item=key):
                # Convert snake_case key to title case
                expected_name = re.sub(r"_+", " ", key).title()
                self.assertEqual(
                    item.name,
                    expected_name,
                    f"Key '{key}' does not match item name '{item.name}' in title case",
                )

    def test_item_has_description(self):
        """Test that each item has a non-empty description."""
        for key, item in item_data.items():
            with self.subTest(item=key):
                self.assertTrue(
                    item.description,
                    f"Item '{item.name}' has an empty or missing description",
                )


if __name__ == "__main__":
    unittest.main()
