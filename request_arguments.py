import flask


def optional(variable_name, required_type):
    """Reads optional variable from request arguments

    If the argument has been provided with wrong type, aborts with 404.

    :param variable_name: name of the argument
    :param required_type: expected argument type
    :return: variable of expected type
    """
    variable = flask.request.args.get(variable_name, None)
    if variable is None:
        return None
    try:
        variable = required_type(variable)
    except TypeError:
        flask.abort(404)
    return variable


def require(variable_name, required_type):
    """Reads required variable from request arguments

    If the argument has been provided with wrong type or has not been
    provided at all, aborts with 404.

    :param variable_name: name of the argument
    :param required_type: expected argument type
    :return: variable of expected type
    """
    variable = optional(variable_name, required_type)
    if variable is None:
        flask.abort(404)
    return variable
