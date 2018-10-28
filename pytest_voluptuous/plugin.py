from __future__ import absolute_import

from voluptuous import MultipleInvalid

from pytest_voluptuous.voluptuous import S


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, S) and (op == '<=' or op == '==') or isinstance(right, S) and op == '==':
        if isinstance(left, S):
            source = left
        else:
            source = right
        if isinstance(source.error, MultipleInvalid):
            errors = [format_error(error) for error in source.error.errors]
        else:
            errors = [format_error(source.error)]
        return [
            'failed to validation error(s):'
        ] + errors
    return None


def format_error(error):
    return '- {}: {}'.format('.'.join(map(str, error.path)), error)
