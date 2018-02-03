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
