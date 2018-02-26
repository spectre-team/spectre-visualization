from typing import NamedTuple
from functools import wraps

import flask
import flask_cors

import discover
import load
from request_arguments import optional, require

app = flask.Flask(__name__)
flask_cors.CORS(app)


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


@app.route('/heatmap/<int:dataset_id>')
@missing_key_returns_404
def heatmap(dataset_id: int):
    channel_id = require('channelId', int)
    return as_response(load.heatmap(dataset_id, channel_id))


@app.route('/spectrum/<int:dataset_id>')
@missing_key_returns_404
def spectrum(dataset_id: int):
    x = require('x', int)
    y = require('y', int)
    return as_response(load.spectrum(dataset_id, x, y))
