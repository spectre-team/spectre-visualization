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
