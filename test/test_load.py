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


@patch.object(load, 'dataset', return_value=simplified_dataset)
class TestMetadataLoading(unittest.TestCase):
    def test_finds_number_of_spectra(self, _):
        metadata = load.metadata("whatever")
        self.assertEqual(metadata.SpectraNumber, 5)

    def test_assigns_some_id(self, _):
        metadata = load.metadata("whatever")
        self.assertIsNotNone(metadata.Id)

    def test_keeps_name(self, _):
        metadata = load.metadata("whatever")
        self.assertEqual(metadata.Name, "whatever")

    def test_finds_ranges(self, _):
        metadata = load.metadata("whatever")
        self.assertEqual(metadata.XRange["Min"], 0)
        self.assertEqual(metadata.XRange["Max"], 2)
        self.assertEqual(metadata.YRange["Min"], 0)
        self.assertEqual(metadata.YRange["Max"], 1)


@patch.object(builtins, 'open', new=mock_open(read_data=simplified_result))
@patch.object(load, 'dataset', new=MagicMock(return_value=simplified_dataset))
@patch.object(discover, 'name', new=MagicMock(return_value="blah"))
@patch.object(discover, 'datasets', new=MagicMock(return_value=datasets))
@patch.object(discover, 'divik', new=MagicMock(return_value=["wololo"]))
class TestDivikResultLoading(unittest.TestCase):
    def test_parses_partition_from_result(self):
        result = load.divik_result(123, 456)
        self.assertEqual(result.Data, [2, 0, 0, 1, 1])

    def test_parses_coordinates_from_dataset(self):
        result = load.divik_result(123, 456)
        self.assertEqual(result.X, [0, 1, 0, 1, 2])
        self.assertEqual(result.Y, [0, 0, 1, 1, 1])


@patch.object(builtins, 'open', new=mock_open(read_data=some_config))
@patch.object(discover, 'name', new=MagicMock(return_value="blah"))
@patch.object(discover, 'datasets', new=MagicMock(return_value=datasets))
@patch.object(discover, 'divik', new=MagicMock(return_value=["wololo"]))
class TestDivikConfigLoading(unittest.TestCase):
    def test_passes_content_without_any_processing(self):
        config = load.divik_config(123, 456)
        self.assertEqual(config, some_config)


@patch.object(load, 'dataset', new=MagicMock(return_value=simplified_dataset))
@patch.object(discover, 'datasets', new=MagicMock(return_value=datasets))
@patch.object(discover, 'name', new=MagicMock(return_value="blah"))
class TestHeatmapLoading(unittest.TestCase):
    def test_throws_when_channel_does_not_exist(self):
        with self.assertRaises(IndexError):
            load.heatmap(123, channel_id=123456789)

    def test_loads_given_channel(self):
        heatmap = load.heatmap(123, channel_id=1)
        self.assertEqual(heatmap.Intensities, [12, 22, 32, 42, 52])


class TestSpectrumLookup(unittest.TestCase):
    def setUp(self):
        self.coordinates = spdata.types.Coordinates([1, 2, 3], [4, 5, 6],
                                                    3 * [0])

    def test_finds_id_of_spectrum_with_given_coordinates(self):
        spectrum_id = load._find_spectrum(self.coordinates, 1, 4)
        self.assertEqual(spectrum_id, 0)

    def test_throws_if_coordinates_do_not_exist(self):
        with self.assertRaises(KeyError):
            load._find_spectrum(self.coordinates, 4, 1)
