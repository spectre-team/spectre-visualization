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


def divik_result(dataset_id: int, divik_id: int) -> models.DivikResult:
    """Load result of divik by id

    :param dataset_id: id of analyzed dataset
    :param divik_id: id of divik analysis
    :return: result of divik algorithm
    """
    dataset_name = discover.name(dataset_id, discover.datasets())
    divik_name = discover.name(divik_id, discover.divik(dataset_name))
    path = divik_result_path(dataset_name, divik_name)
    with open(path) as result_file:
        result_tree = json.load(result_file)
    assignments = list(np.array(result_tree['partition']))

    data = dataset(dataset_name)
    x = list(data.coordinates.x.ravel())
    y = list(data.coordinates.y.ravel())

    return models.DivikResult(x, y, assignments)


def divik_config(dataset_id: int, divik_id: int) -> str:
    """Load config of divik by id

    :param dataset_id: id of analyzed dataset
    :param divik_id: id of divik analysis
    :return: string containing JSON with divik options
    """
    dataset_name = discover.name(dataset_id, discover.datasets())
    divik_name = discover.name(divik_id, discover.divik(dataset_name))
    path = divik_result_path(dataset_name, divik_name)
    with open(path) as result_file:
        result = result_file.read()
    return result
