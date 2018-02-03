from typing import NamedTuple, List

import numpy as np


class CoordinatesRange(object):
    def __init__(self, vector: np.ndarray):
        """
        :param vector: vector with locations across single coordinate
        """
        self.Min = int(vector.ravel().min())
        self.Max = int(vector.ravel().max())

