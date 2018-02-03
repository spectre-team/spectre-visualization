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
