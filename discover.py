import hashlib
import os
from functools import lru_cache
from typing import List

_FILESYSTEM_ROOT = os.path.abspath(os.sep)
DATA_ROOT = os.path.join(_FILESYSTEM_ROOT, 'data')
Name = str
Path = str


@lru_cache(maxsize=1024)
def name_to_id(entity_name: str) -> int:
    """Get ID for a name

    Computes SHA256 hash of name and converts it to int value.

    :param entity_name: name of an object
    :return: unique identifier
    """
    return int(hashlib.sha256(entity_name.encode()).hexdigest(), 16)


class UnknownIdError(KeyError):
    """Thrown when id of element could not be resolved"""
    pass


def name(element_id: int, names: List[Name]) -> Name:
    """Resolve element name by its id

    :param element_id: id of the element in names list
    :param names: names list
    :return: name of the element under given id
    """
    matching = [_name for _name in names
                if name_to_id(_name) == element_id]
    if len(matching) == 0:
        raise UnknownIdError(element_id)
    return matching[0]


def divik(dataset_name: Name) -> List[Name]:
    """Discover available divik analyses for a dataset

    :param dataset_name: name of the dataset under analysis
    :return: list of available divik analyses
    """
    return os.listdir(os.path.join(DATA_ROOT, dataset_name, 'divik'))


def datasets() -> List[str]:
    """Discover available datasets in default store

    :return: list of available datasets
    """
    return os.listdir(DATA_ROOT)


def data_path(dataset_name: Name) -> Path:
    """Discover path to dataset

    :param dataset_name: name of the dataset
    :return: path to the dataset file
    """
    return os.path.join(DATA_ROOT, dataset_name, 'text_data', 'data.txt')
