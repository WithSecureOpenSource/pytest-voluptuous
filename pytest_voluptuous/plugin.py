import functools

from voluptuous import Schema, ALLOW_EXTRA, Invalid, MultipleInvalid
from voluptuous.schema_builder import PREVENT_EXTRA


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, S) and (op == '<=' or op == '==') or isinstance(right, S) and op == '==':
        if isinstance(left, S):
            source = left
        else:
            source = right
        if isinstance(source, MultipleInvalid):
            errors = [('   - ' + str(error)) for error in source.errors]
        else:
            errors = ['   - ' + str(source)]
        return [
            'failed due to invalid data against schema:',
            '   Errors: '
        ] + errors


class S(Schema):

    def __init__(self, *args, **kwargs):
        super(S, self).__init__(*args, required=kwargs.pop('required', True), **kwargs)
        self.error = None

    def _validate(self, other):
        try:
            self(other)
        except Invalid as e:
            self.error = e  # cache error
            return False
        else:
            return True

    def __eq__(self, other):
        self.extra = PREVENT_EXTRA
        return self._validate(other)

    def __le__(self, other):
        self.extra = ALLOW_EXTRA
        return self._validate(other)


Exact = functools.partial(S, extra=PREVENT_EXTRA)
Partial = functools.partial(S, extra=ALLOW_EXTRA)
