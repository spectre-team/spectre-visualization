import unittest

import numpy as np

import models


class TestCoordinatesRange(unittest.TestCase):
    def test_finds_bounds(self):
        coordinates = np.array([1, 2, 6, 3, 4, 76, 2, -3])
        _range = models.CoordinatesRange(coordinates)
        self.assertEqual(_range.Min, -3)
        self.assertEqual(_range.Max, 76)

    def test_does_not_fail_for_strange_shape(self):
        coordinates = np.array([[[1, 2, 6, 3, 4, 76, 2, -3]]])
        _range = models.CoordinatesRange(coordinates)
        self.assertEqual(_range.Min, -3)
        self.assertEqual(_range.Max, 76)


class TestDatasetMetadata(unittest.TestCase):
    def test_converts_coordinate_ranges_to_dicts(self):
        metadata = models.DatasetMetadata(
            dataset_id=1, name="whatever", spectra_number=3,
            x_range=models.CoordinatesRange(np.array([1, 2, 3])),
            y_range=models.CoordinatesRange(np.array([5, 6, 7])))
        self.assertIsInstance(metadata.XRange, dict)
        self.assertIsInstance(metadata.YRange, dict)
        self.assertIn('Min', metadata.XRange)
        self.assertIn('Max', metadata.XRange)
        self.assertIn('Min', metadata.YRange)
        self.assertIn('Max', metadata.YRange)
        self.assertEqual(metadata.XRange["Min"], 1)
        self.assertEqual(metadata.XRange["Max"], 3)
        self.assertEqual(metadata.YRange["Min"], 5)
        self.assertEqual(metadata.YRange["Max"], 7)
