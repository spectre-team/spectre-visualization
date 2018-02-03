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

