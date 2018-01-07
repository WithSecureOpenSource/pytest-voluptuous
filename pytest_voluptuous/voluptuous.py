from __future__ import absolute_import

import functools

from voluptuous import Schema, ALLOW_EXTRA, Invalid
from voluptuous.schema_builder import PREVENT_EXTRA


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
