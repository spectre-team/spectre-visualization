from typing import NamedTuple, List

import numpy as np


class CoordinatesRange(object):
    def __init__(self, vector: np.ndarray):
        """
        :param vector: vector with locations across single coordinate
        """
        self.Min = int(vector.ravel().min())
        self.Max = int(vector.ravel().max())


class DatasetMetadata(object):
    def __init__(self, dataset_id: int, name: str, spectra_number: int,
                 x_range: CoordinatesRange, y_range: CoordinatesRange):
        """
        :param name: name of dataset to extract metadata from
        """
        self.Id = dataset_id
        self.Name = name
        self.SpectraNumber = spectra_number
        self.XRange = vars(x_range)
        self.YRange = vars(y_range)


DivikResult = NamedTuple('DivikResult', [
    ('X', List[int]), ('Y', List[int]),
    ('Data', List[int])
])
