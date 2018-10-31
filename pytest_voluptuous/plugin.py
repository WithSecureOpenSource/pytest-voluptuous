from __future__ import absolute_import

from voluptuous import MultipleInvalid

from pytest_voluptuous.voluptuous import S


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, S) and (op == '<=' or op == '==') or isinstance(right, S) and op == '==':
        if isinstance(left, S):
            source = left
            data = right
        else:
            source = right
            data = left

        if isinstance(source.error, MultipleInvalid):
            errors = [format_error(error, data) for error in source.error.errors]
        else:
            errors = [format_error(source.error, data)]

        return [
            'failed to validation error(s):'
        ] + errors
    return None


def format_error(error, data):
    if error.path:
        prefix = '.'.join(map(str, error.path)) + ': '
        try:
            value = get_value(data, error.path)
            suffix = (' (actual: ' + repr(value) + ')')
        except:
            suffix = ''

    else:
        prefix = ''
        suffix = ''

    return '- {}{}{}'.format(prefix, error.msg, suffix)


def get_value(data, path):
    value = data
    for key in path:
        value = value[key]

    return value
