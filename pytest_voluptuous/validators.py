from __future__ import absolute_import

from voluptuous import Invalid, MultipleInvalid
from voluptuous.schema_builder import Schema


class Equal(object):
    """Ensure that value matches target.

    >>> import pytest
    >>> s = Schema(Equal(1))
    >>> s(1)
    1
    >>> with pytest.raises(Invalid):
    ...    s(2)

    Validators are not supported, match must be exact:

    >>> s = Schema(Equal(str))
    >>> with pytest.raises(Invalid):
    ...     s('foo')
    """

    def __init__(self, target, msg=None):
        self.target = target
        self.msg = msg

    def __call__(self, v):
        if v != self.target:
            raise Invalid(self.msg or 'Values are not equal: value:{} != target:{}'.format(v, self.target))
        return v

    def __repr__(self):
        return 'Equal({})'.format(self.target)


class Unordered(object):
    """Ensures sequence contains values in unspecified order.

    >>> s = Schema(Unordered([2, 1]))
    >>> s([2, 1])
    [2, 1]
    >>> s([1, 2])
    [1, 2]
    >>> s = Schema(Unordered([str, int]))
    >>> s(['foo', 1])
    ['foo', 1]
    >>> s([1, 'foo'])
    [1, 'foo']

    """

    def __init__(self, validators, msg=None, **kwargs):
        self.validators = validators
        self.msg = msg
        self._schemas = [Schema(val, **kwargs) for val in validators]

    def __call__(self, v):
        if not isinstance(v, (list, tuple)):
            raise Invalid(self.msg or 'Value {} is not sequence!'.format(v))

        if len(v) != len(self._schemas):
            raise Invalid(self.msg or 'List lengths differ, value:{} != target:{}'.format(len(v), len(self._schemas)))

        consumed = set()
        missing = []
        for index, value in enumerate(v):
            found = False
            for i, s in enumerate(self._schemas):
                if i in consumed:
                    continue
                try:
                    s(value)
                except Invalid:
                    pass
                else:
                    found = True
                    consumed.add(i)
                    break
            if not found:
                missing.append((index, value))

        if len(missing) == 1:
            el = missing[0]
            raise Invalid(self.msg or 'Element #{} ({}) is not valid against any validator'.format(el[0], el[1]))
        elif missing:
            raise MultipleInvalid([
                Invalid(self.msg or 'Element #{} ({}) is not valid against any validator'.format(el[0], el[1]))
                for el in missing
            ])
        return v

    def __repr__(self):
        return 'Unordered([{}])'.format(", ".join(repr(v) for v in self.validators))
