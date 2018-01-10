.. image:: https://img.shields.io/pypi/v/pytest-voluptuous.svg?style=flat
   :alt: PyPI Package latest release
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/pyversions/pytest-voluptuous.svg?style=flat
   :alt: Supported versions
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/implementation/pytest-voluptuous.svg?style=flat
   :alt: Supported implementations
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/l/pytest-voluptuous.svg?style=flat
   :alt: License
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://travis-ci.org/F-Secure/pytest-voluptuous.svg?branch=master
   :target: https://travis-ci.org/f-secure/pytest-voluptuous
   :alt: Travis-CI

.. image:: https://coveralls.io/repos/github/f-secure/pytest-voluptuous/badge.svg?branch=master
   :target: https://coveralls.io/github/f-secure/pytest-voluptuous?branch=master
   :alt: Coveralls

=================
pytest-voluptuous
=================

A `pytest <https://pytest.org>`_ plugin for asserting data against
`voluptuous <https://github.com/alecthomas/voluptuous>`_ schema.

Common use case is to validate HTTP API responses (in your functional tests):

.. code-block:: python

    import requests
    from pytest_voluptuous import S, Partial, Exact
    from voluptuous.validators import All, Length

    def test_pypi():
       resp = requests.get('https://pypi.python.org/pypi/pytest/json')
       assert S({
          'info': Partial({
              'package_url': 'http://pypi.python.org/pypi/pytest',
              'platform': 'INVALID VALUE',
              'description': Length(max=10),
              'downloads': list,
              'classifiers': dict,
          }),
          'releases': {
             any: dict
          },
          'urls': int
       }) == resp.json()

If validation fails, comparison returns ``False`` and assert fails, printing error details::

    E       AssertionError: assert failed to validation error(s):
    E         - info.platform: not a valid value for dictionary value @ data[u'info'][u'platform']
    E         - info.description: length of value must be at most 10 for dictionary value @ data[u'info'][u'description']
    E         - info.downloads: expected list for dictionary value @ data[u'info'][u'downloads']
    E         - info.classifiers: expected dict for dictionary value @ data[u'info'][u'classifiers']
    E         - urls: expected int for dictionary value @ data[u'urls']
    E         - releases.3.1.3: expected dict for dictionary value @ data[u'releases'][u'3.1.3']

Install
=======

Works on python 2.7 and 3.4+::

    pip install pytest-voluptuous

Changelog
=========

See `CHANGELOG <CHANGELOG.rst>`_.

Features
========

- Provides **utility schemas** (``S``, ``Exact`` and ``Partial``) to cut down boilerplate.
- Implement a **pytest hook** to provide error details on ``assert`` failure.
- Print descriptive validation **failure messages**.
- ``Equal`` and ``Unordered`` validators (contributed to voluptuous project, available in 0.10+).

Why?
====

Because writing:

    >>> r = {'info': {'package_url': 'http://pypi.python.org/pypi/pytest'}}
    >>> assert 'info' in r
    >>> assert 'package_url' in r['info']
    >>> assert r['info']['package_url'] == 'http://pypi.python.org/pypi/pytest'

...is just *way* too annoying.

Why not `JSON schema <http://json-schema.org/>`_? It's **too verbose**, too inconvenient. JSON schema will never
match the convenience of a validation library that can utilize the goodies of the platform.

Why voluptuous and not some other library? No special reason - but it's pretty easy to use and understand. Also, the
syntax is quite compact.

Usage
=====

In ``pytest``:

    >>> import requests
    >>> from pytest_voluptuous import S, Partial, Exact
    >>> from voluptuous.validators import All, Length
    >>> resp = requests.get('https://pypi.python.org/pypi/pytest/json')
    >>> assert S({
    ...     'info': Partial({
    ...         'package_url': 'http://pypi.python.org/pypi/pytest',
    ...         'platform': 'unix',
    ...         'description': Length(min=100),
    ...         'downloads': dict,
    ...         'classifiers': list,
    ...     }),
    ...     'releases': {
    ...         any: list
    ...     },
    ...     'urls': list
    ... }) == resp.json()

Note: if you run this in shell, there's no pytest magic in play and in case of failure, you'll just get
``AssertionError`` as in:

    >>> assert S({'does_not_exist': 1}) == resp.json()
    Traceback (most recent call last):
        ...
    AssertionError

Don't worry - the promised magic comes into play when you run the validation in a pytest test.

Use ``==`` operator to do exact validation:

    >>> data = {'foo': 1, 'bar': True}
    >>> S({'foo': 1, 'bar': True}) == data
    True

We omit ``assert`` in these examples (for easier doctesting).

Use ``<=`` to do *partial* validation (to allow extra keys, that is):

    >>> S({'foo': 1}) == data  # not valid
    False
    >>> S({'foo': 1}) <= data  # valid
    True

The operator you choose gets inherited, so with test data of:

    >>> data = {
    ...     'outer1': {
    ...         'inner1': 1,
    ...         'inner2': True
    ...     },
    ...     'outer2': 'foo'
    ... }

With ``==`` you must provide exact value *also in nested context*:

    >>> S({
    ...     'outer1': {
    ...         'inner1': 1,  # this would be valid but...
    ...         # missing 'inner2'
    ...     },
    ...     'outer2': 'foo'
    ... }) == data
    False
    >>> S({
    ...     'outer1': {
    ...         'inner1': int,  # exact/partial matching
    ...         'inner2': bool  # is for keys only
    ...     },
    ...     'outer2': 'foo'
    ... }) == data
    True

``<=`` implies partial matching:

    >>> S({
    ...     'outer1': {
    ...         'inner1': int,
    ...         # 'inner2' missing but that's ok
    ...     },
    ...     # 'outer2' is missing too
    ... }) <= data
    True

When you need to mix and match operators, you can loosen matching with ``Partial``:

    >>> S({
    ...     'outer1': Partial({
    ...         'inner1': int
    ...         # 'inner2' ok to omit as scope is partial
    ...     }),
    ...     'outer2': 'foo'  # can't be missing as outer scope is exact
    ... }) == data
    True

And stricten with ``Exact``:

    >>> S({
    ...     'outer1': Exact({
    ...         'inner1': int,
    ...         'inner2': bool
    ...     }),
    ...     # 'outer2' can be missing as outer scope is partial
    ... }) <= data
    True

Remember, matching mode is inherited, so you may end up doing stuff like this:

    >>> data['outer1']['inner1'] = {'prop': 1}
    >>> S({
    ...     'outer1': Partial({
    ...         'inner1': Exact({
    ...             'prop': 1
    ...         })
    ...     }),
    ...     'outer2': 'foo'
    ... }) == data
    True

There is no ``>=``. If you want to declare *schema keys that may be missing*, use ``Optional``:

    >>> from voluptuous.schema_builder import Optional
    >>> S({Optional('foo'): str}) == {'extra': 1}
    False
    >>> S({'foo': str}) == {}
    False
    >>> S({'foo': str}) <= {}
    False
    >>> S({Optional('foo'): str}) == {}
    True
    >>> S({Optional('foo'): str}) <= {'extra': 1}
    True

Or, if you want to make all keys optional, override ``required``:

    >>> from voluptuous.schema_builder import Required
    >>> S({'foo': str}, required=False) == {}
    True

In these cases, if you want to *require* a key:

    >>> S({'foo': str, Required('bar'): 1}, required=False) == {}
    False
    >>> S({'foo': str, Required('bar'): 1}, required=False) == {'bar': 1}
    True

That's it. For available validators, look into `voluptuous docs <https://github.com/alecthomas/voluptuous>`_.

Gotchas
=======

**Voluptuous 0.9.3 and earlier:**

In voluptuous pre-0.10.2 ``[]`` matches *any* list, not an empty list. To declare an empty list, use ``Equal([])``.

Similarly, in voluptuous pre-0.10.2, ``{}`` doesn't *always* match an empty dict. If you're inside a
``Schema({...}, extra=PREVENT_EXTRA)`` (or ``Exact``), ``{}`` does indeed match exactly ``{}``. However, inside
``Schema({...}, extra=ALLOW_EXTRA) (or ``Partial``), it matches *any* dict (because any extra keys are allowed).
To declare an empty dict, use ``Equal({})``.

**Voluptuous 0.10.0+:**

In voluptuous 0.10.0+ ``{}`` and ``[]`` evaluate as *empty* dict and *empty* list, so you don't need above workarounds.

Always use ``dict`` and ``list`` to validate dict or list of any size. It works despite voluptuous version.

**Any version:**

``[str, int]`` matches any list that contains both strings and ints (in any order and 1-n times). To validate
a list of fixed length with those types in it, use ``ExactSequence([str, int])`` and ``Unordered([str, int])``
when the order has no meaning. You can also use values inside these as in ``ExactSequence([2, 3])``.

License
=======

Apache 2.0 licensed. See `LICENSE <LICENSE.rst>`_ for more details.
