import unittest
from unittest.mock import MagicMock, patch

from flask import url_for
import numpy as np

import discover
import load
import models

import api


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()


def build_metadata(name: str) -> models.DatasetMetadata:
    return models.DatasetMetadata(
        dataset_id=load.name_to_id(name), name=name, spectra_number=1234,
        x_range=models.CoordinatesRange(np.array([1, 2, 3])),
        y_range=models.CoordinatesRange(np.array([4, 5, 6])))


dataset_discovery = MagicMock(return_value=['first_dataset', 'second_dataset'])
metadata_loading = MagicMock(side_effect=build_metadata)
some_id = 1234


def get_name_for_matching_id(identifier: int, _) -> str:
    if identifier == some_id:
        return 'first_dataset'
    raise KeyError(identifier)


name_discovery = MagicMock(side_effect=get_name_for_matching_id)


@patch.object(discover, 'datasets', new=dataset_discovery)
@patch.object(load, 'metadata', new=metadata_loading)
class TestPreparationsList(ApiTestCase):
    def test_gets_list_of_preparations_if_default_store(self):
        response = self.app.get('/preparations/')
        self.assertIn(b'first_dataset', response.data)
        self.assertIn(b'second_dataset', response.data)

    @patch.object(discover, 'name', new=name_discovery)
    def test_gets_single_preparation_when_passed_id(self):
        response = self.app.get('/preparations/%i' % some_id)
        self.assertIn(b'first_dataset', response.data)
        self.assertNotIn(b'second_dataset', response.data)

    @patch.object(discover, 'name', new=name_discovery)
    def test_has_backward_compatible_response(self):
        response = self.app.get('/preparations/%i' % some_id)
        self.assertIn(b'"Id": ', response.data)
        self.assertIn(b'"Name": ', response.data)
        self.assertIn(b'"SpectraNumber": ', response.data)
        self.assertIn(b'"XRange": ', response.data)
        self.assertIn(b'"YRange": ', response.data)
        self.assertIn(b'"Min": ', response.data)
        self.assertIn(b'"Max": ', response.data)


divik_result_loading = MagicMock(return_value=models.DivikResult([1], [2], [0]))


@patch.object(load, 'divik_result', new=divik_result_loading)
class TestDivikResult(ApiTestCase):
    url = '/divikResult/123?divikId=2&level=3'
    possible_urls = ['/divikResult/123?divikId=2&level=3',
                     '/divikResult/123?level=3&divikId=2']

    def test_routing_is_backward_compatible(self):
        with api.app.test_request_context():
            url = url_for('divik', dataset_id=123, divikId=2, level=3)
        self.assertIn(url, self.possible_urls)

    def test_has_coordinates(self):
        response = self.app.get(self.url)
        self.assertIn(b'"X": ', response.data)
        self.assertIn(b'"Y": ', response.data)

    def test_has_partition(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Data": ', response.data)


some_config = '{"maxK": 10, "metric": "euclidean"}'
divik_config_loading = MagicMock(return_value=some_config)


@patch.object(load, 'divik_config', new=divik_config_loading)
class TestDivikConfig(ApiTestCase):
    url = '/divikResult/123?divikId=2'

    def test_routing_is_backward_compatible(self):
        with api.app.test_request_context():
            url = url_for('divik', dataset_id=123, divikId=2)
        self.assertEqual(url, self.url)

    def test_passes_config_file_unchanged(self):
        response = self.app.get(self.url)
        self.assertEqual(response.data, some_config.encode())

    def test_returns_404_when_divik_id_is_missing(self):
        response = self.app.get('/divikResult/123')
        self.assertEqual(response.status_code, 404)
