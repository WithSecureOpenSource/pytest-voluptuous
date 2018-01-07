from pytest_voluptuous.voluptuous import S
from voluptuous import MultipleInvalid


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, S) and (op == '<=' or op == '==') or isinstance(right, S) and op == '==':
        if isinstance(left, S):
            source = left
        else:
            source = right
        if isinstance(source.error, MultipleInvalid):
            errors = ['- {}: {}'.format('.'.join(error.path), error) for error in source.error.errors]
        else:
            errors = ['- {}: {}'.format('.'.join(source.error.path), source.error)]
        return [
            'failed to validation error(s):'
        ] + errors
