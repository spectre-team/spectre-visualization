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
