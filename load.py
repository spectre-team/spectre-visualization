import json
from functools import lru_cache

import numpy as np

import spdata.reader
import spdata.types

import models
import discover
from discover import name_to_id

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


def heatmap(dataset_id: int, channel_id: int) -> models.Heatmap:
    """Load heatmap from dataset by mass channel id

    :param dataset_id: id of dataset
    :param channel_id: id of mass channel
    :return: heatmap for given channel
    """
    dataset_name = discover.name(dataset_id, discover.datasets())
    data = dataset(dataset_name)
    return models.Heatmap(data.mz[channel_id],
                          list(data.spectra[:, channel_id]),
                          list(map(int, data.coordinates.x)),
                          list(map(int, data.coordinates.y)))


def _find_spectrum(coordinates: spdata.types.Coordinates,
                   x: int, y: int) -> int:
    """Find index of spectrum by its coordinates

    :param coordinates: coordinates of spectra in the dataset
    :param x: x-coordinate of spot
    :param y: y-coordinate of spot
    :return: index of spectrum
    """
    matching_x = coordinates.x == x
    matching_y = coordinates.y == y
    matching_coordinates = np.logical_and(matching_x, matching_y)
    matching_indexes = list(np.where(matching_coordinates.ravel())[0])
    if len(matching_indexes) < 1:
        raise KeyError((x, y))
    return int(matching_indexes[0])


def spectrum(dataset_id: int, x: int, y: int) -> models.Spectrum:
    """Load spectrum from dataset by its coordinates

    :param dataset_id: id of dataset
    :param x: x-coordinate of spot
    :param y: y-coordinate of spot
    :return: spectrum at given coordinates
    """
    dataset_name = discover.name(dataset_id, discover.datasets())
    data = dataset(dataset_name)
    spectrum_id = _find_spectrum(data.coordinates, x, y)
    intensities = list(data.spectra[spectrum_id].astype(float))
    return models.Spectrum(Id=spectrum_id, Mz=list(data.mz.astype(float)),
                           X=x, Y=y, Intensities=intensities)
