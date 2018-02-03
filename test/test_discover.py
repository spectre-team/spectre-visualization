import unittest
from unittest.mock import patch
import os

import discover

some_names = ["a", "blah", "wololo", "some_name", "other_name"]


class TestNameToId(unittest.TestCase):
    def test_generates_some_unique_ids(self):
        ids = {discover.name_to_id(name) for name in some_names}
        self.assertEqual(len(ids), len(some_names))

    def test_id_is_consistent_for_the_same_name(self):
        self.assertEqual(discover.name_to_id("blah"), discover.name_to_id("blah"))


class TestNameDiscovery(unittest.TestCase):
    def test_finds_name_by_its_id(self):
        some_name = "wololo"
        some_id = discover.name_to_id(some_name)
        self.assertEqual(
            discover.name(some_id, some_names),
            some_name
        )

    def test_throws_for_nonexistent_name(self):
        with self.assertRaises(discover.UnknownIdError):
            discover.name(123, some_names)
