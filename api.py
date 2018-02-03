from typing import NamedTuple
from functools import wraps

import flask

import discover
import load
from request_arguments import optional, require

app = flask.Flask(__name__)


def as_response(model: NamedTuple):
    """Convert NamedTuple to Flask JSON response

    :param model: returned data model
    :return: JSON representation of data
    """
    # noinspection PyProtectedMember
    return flask.jsonify(model._asdict())
