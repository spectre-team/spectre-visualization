from typing import NamedTuple
from functools import wraps

import flask

import discover
import load
from request_arguments import optional, require

app = flask.Flask(__name__)
