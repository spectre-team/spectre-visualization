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


def missing_key_returns_404(fun):
    """Handle missing identifiers by 404

    :param fun: view that requires handling
    :return: view with handling capabilities
    """
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except discover.UnknownIdError:
            flask.abort(404)
    return wrapper


@app.route('/preparations/')
@app.route('/preparations/<int:dataset_id>')
@missing_key_returns_404
def preparations(dataset_id: int=None):
    if dataset_id is None:
        return flask.jsonify([
            vars(load.metadata(name)) for name in discover.datasets()
        ])
    dataset_name = discover.name(dataset_id, discover.datasets())
    return flask.jsonify(vars(load.metadata(dataset_name)))


@app.route('/divikResult/<int:dataset_id>')
@missing_key_returns_404
def divik(dataset_id: int):
    divik_id = require('divikId', int)
    level = optional('level', int)
    if level is None:
        # configuration was requested
        return load.divik_config(dataset_id, divik_id)
    # unused for a while, informs that result was requested
    return as_response(load.divik_result(dataset_id, divik_id))


@app.route('/heatmap/<int:dataset_id>')
@missing_key_returns_404
def heatmap(dataset_id: int):
    channel_id = require('channelId', int)
    return as_response(load.heatmap(dataset_id, channel_id))
