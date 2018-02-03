import unittest
from unittest.mock import MagicMock, mock_open, patch
import builtins
from io import StringIO

import spdata.reader
import spdata.types

import discover
import load


simplified_dataset_file = """global metadata
1 2 3 4 5
0 0 0 0
11 12 13 14 15
1 0 0 0
21 22 23 24 25
0 1 0 0
31 32 33 34 35
1 1 0 1
41 42 43 44 45
2 1 0 1
51 52 53 54 55
"""
simplified_dataset = spdata.reader.load_txt(StringIO(simplified_dataset_file))
simplified_result = '{"partition": [2,0,0,1,1]}'
some_config = '{"maxK": 20, "metric": "euclidean"}'
datasets = ["fist_dataset", "second_dataset"]
