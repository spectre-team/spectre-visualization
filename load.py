import json
from functools import lru_cache

import numpy as np

import spdata.reader
import spdata.types

import models
import discover
from discover import divik_result_path, name_to_id

Name = str
Path = str


@lru_cache(maxsize=10)
def dataset(name: Name) -> spdata.types.Dataset:
    """Load dataset by name

    :param name: name of the dataset
    :return: MSI data
    """
    with open(discover.data_path(name)) as data_file:
        return spdata.reader.load_txt(data_file)


@lru_cache(maxsize=128)
def metadata(name: Name) -> models.DatasetMetadata:
    """Load dataset metadata by dataset name

    :param name: name of the dataset
    :return: metadata of the dataset
    """
    dataset_id = name_to_id(name)
    data = dataset(name)
    spectra_number = data.spectra.shape[0]
    x_range = models.CoordinatesRange(data.coordinates.x)
    y_range = models.CoordinatesRange(data.coordinates.y)
    return models.DatasetMetadata(dataset_id, name, spectra_number, x_range,
                                  y_range)
