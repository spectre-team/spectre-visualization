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
