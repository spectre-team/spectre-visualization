import hashlib
import os
from functools import lru_cache
from typing import List

_FILESYSTEM_ROOT = os.path.abspath(os.sep)
DATA_ROOT = os.path.join(_FILESYSTEM_ROOT, 'data')
Name = str
Path = str
