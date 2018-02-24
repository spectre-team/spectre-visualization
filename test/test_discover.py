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


@patch.object(os, 'listdir', autospec=True)
class TestDatasetDiscovery(unittest.TestCase):
    def test_checks_default_store(self, mock):
        discover.datasets()
        self.assertIn(discover.DATA_ROOT, mock.call_args[0][0])


class TestDatasetPathBuilding(unittest.TestCase):
    def test_path_is_unique_for_dataset_name(self):
        paths = {discover.data_path(name) for name in some_names}
        self.assertEqual(len(paths), len(some_names))

    def test_path_is_constant_for_the_same_dataset_name(self):
        some_name = "wololo"
        self.assertEqual(discover.data_path(some_name),
                         discover.data_path(some_name))

    def test_path_is_rooted_at_default_store(self):
        some_path = discover.data_path("wololo")
        self.assertTrue(some_path.startswith(discover.DATA_ROOT))
