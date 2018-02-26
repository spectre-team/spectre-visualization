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


heatmap_loading = MagicMock(return_value=models.Heatmap(
    Mz=1., Intensities=[1., 2., 3.], X=[1, 2, 3], Y=[4, 5, 6]))


@patch.object(load, 'heatmap', new=heatmap_loading)
class TestHeatmap(ApiTestCase):
    url = '/heatmap/123?channelId=1'

    def test_has_mz(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Mz": ', response.data)

    def test_has_intensities(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Intensities": ', response.data)

    def test_has_coordinates(self):
        response = self.app.get(self.url)
        self.assertIn(b'"X": ', response.data)
        self.assertIn(b'"Y": ', response.data)


spectrum_loading = MagicMock(side_effect=lambda _, x, y: models.Spectrum(
    Intensities=[1., 2., 3.], Id=1, Mz=[4., 5., 6.], X=x, Y=y))


@patch.object(load, 'spectrum', new=spectrum_loading)
class TestSpectrum(ApiTestCase):
    url = '/spectrum/123?x=8&y=9'

    def test_throws_404_without_coordinates(self):
        response = self.app.get('/spectrum/123?x=8')
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/spectrum/123?y=9')
        self.assertEqual(response.status_code, 404)

    def test_has_id(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Id": 1', response.data)

    def test_has_intensities(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Intensities": ', response.data)

    def test_has_mz(self):
        response = self.app.get(self.url)
        self.assertIn(b'"Mz": ', response.data)

    def test_has_coordinates(self):
        response = self.app.get(self.url)
        self.assertIn(b'"X": 8', response.data)
        self.assertIn(b'"Y": 9', response.data)
