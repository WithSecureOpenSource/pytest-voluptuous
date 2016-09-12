=================
pytest-voluptuous
=================

.. image:: https://img.shields.io/pypi/v/pytest-voluptuous.svg?style=flat
   :alt: PyPI Package latest release
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/dm/pytest-voluptuous.svg?style=flat
   :alt: PyPI Package monthly downloads
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://travis-ci.org/f-secure/pytest-voluptuous.png
   :target: https://travis-ci.org/f-secure/pytest-voluptuous
   :alt: Travis-CI

.. image:: https://coveralls.io/repos/github/f-secure/pytest-voluptuous/badge.svg?branch=master
   :target: https://coveralls.io/github/f-secure/pytest-voluptuous?branch=master
   :alt: Coveralls

.. image:: https://readthedocs.org/projects/pytest-voluptuous/badge/
   :target: http://pytest-voluptuous.readthedocs.io/
   :alt: Documentation

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat
   :target: https://gitter.im/f-secure/pytest-voluptuous?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://img.shields.io/pypi/pyversions/pytest-voluptuous.svg?style=flat
   :alt: Supported versions
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/implementation/pytest-voluptuous.svg?style=flat
   :alt: Supported implementations
   :target: https://pypi.python.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/scrutinizer/g/ionelmc/pytest-voluptuous/master.svg?style=flat
   :alt: Code quality
   :target: https://scrutinizer-ci.com/g/ionelmc/pytest-voluptuous

.. image:: https://img.shields.io/pypi/l/pytest-voluptuous.svg?style=flat
   :alt: License
   :target: https://pypi.python.org/pypi/pytest-voluptuous

Pytest plugin for asserting data against `voluptuous <https://github.com/alecthomas/voluptuous>`_ schema.

Common use case is to validate HTTP API responses (in your functional tests):

    >>> import requests
    >>> from pytest_voluptuous import S, Partial, Exact
    >>> from voluptuous.validators import All, Length
    >>> resp = requests.get('https://pypi.python.org/pypi/pytest/json')
    >>> assert S({
    ...     'info': Partial({
    ...         'package_url': 'http://pypi.python.org/pypi/pytest',
    ...         'author': str,
    ...         'platform': None,
    ...         'description': All(str, Length(min=100)),
    ...         'downloads': dict,
    ...         'classifiers': list,
    ...     }),
    ...     'releases': {
    ...         str: list
    ...      },
    ...      'urls': list
    ... }) == resp.json()

If validation fails, comparison returns ``False`` and assert fails:

    >>> assert S({'does_not_exist': 1}) == resp.json()
    Traceback (most recent call last):
        ...
    AssertionError

Validation errors are printed::

    E       assert failed to validation error(s):
    E              - expected str for dictionary value @ data['prop']
    E              - extra keys not allowed @ data['urls']
    E              - extra keys not allowed @ data['releases']
    E              - extra keys not allowed @ data['info']
    E              - required key not provided @ data['does_not_exist']

Install
=======

::

    pip install pytest-voluptuous

Changelog
=========

See ``CHANGELOG.rst``.

Features
========

- Provides utility schemas (``S``, ``Exact`` and ``Partial``) to cut boilerplate.
- Implement a pytest hook to provide validation error details on ``assert`` failure.
- ``Equal`` and ``Unordered`` validators (contributed to voluptuous project but not released yet).

Usage
=====

Use ``==`` operator to do exact validation:

    >>> data = {'foo': 1, 'bar': True}
    >>> S({'foo': 1, 'bar': True}) == data
    True

We omit ``assert`` in these examples (for easier doctesting).

Use ``<=`` to do *partial* validation (to allow extra keys, that is):

    >>> S({'foo': 1}) == data
    False
    >>> S({'foo': 1}) <= data
    True

The operator you choose gets inherited, so:

    >>> data = {
    ...     'outer': {
    ...         'inner': {
    ...             'prop': 1
    ...         }
    ...     }
    ... }

With ``==`` you must provide exact value in nested schemas:

    >>> S({
    ...     'outer': {
    ...         'inner': {}
    ...     }
    ... }) == data
    False
    >>> S({
    ...     'outer': {
    ...         'inner': {
    ...             'prop': int
    ...         }
    ...     }
    ... }) == data
    True

``<=`` implies partial matching also in nested schemas:

    >>> S({
    ...     'outer': {
    ...         'inner': {}
    ...     }
    ... }) <= data
    True

You can loosen matching with ``Partial``:

    >>> S({
    ...     'outer': {
    ...         'inner': Partial({})
    ...     }
    ... }) == data
    True

And stricten with ``Exact``:

    >>> data['extra'] = 'yes'
    >>> S({
    ...     'outer': {
    ...         'inner': Exact({
    ...             'prop': int
    ...         })
    ...     }
    ... }) <= data
    True

Remember, matching mode is inherited, so you may end up doing this:

    >>> del data['extra']
    >>> data['outer']['extra'] = 2
    >>> S({
    ...     'outer': Partial({
    ...         'inner': Exact({
    ...             'prop': 1
    ...         })
    ...     })
    ... }) == data
    True

There is no ``>=``. If you want to accept a sub-set of schema, use ``Optional``:

    >>> from voluptuous.schema_builder import Optional
    >>> S({Optional('foo'): str}) == {'extra': 1}
    False
    >>> S({Optional('foo'): str}) == {}
    True
    >>> S({Optional('foo'): str}) <= {'extra': 1}
    True

Or, you can override ``required`` field as usual:

    >>> S({'foo': str}, required=False) == {}
    True

Gotchas
=======

In voluptuous, ``[]`` matches any list, not an empty list. ``[str, int]`` matches any list that contains
both strings and ints (in any order and 1-n times). To validate a list of fixed length with those types in it,
use ``ExactSequence([str, int])`` and ``Unordered([str, int])`` when the order has no meaning.
You can also use values inside these as in ``ExactSequence([2, 3])``.

Similarly, ``{}`` doesn't *always* match an empty dict. If you're inside a ``Schema({...}, extra=PREVENT_EXTRA)``
(or ``Exact``), ``{}`` does indeed match exactly ``{}``. However, inside
``Schema({...}, extra=Allow_EXTRA) (or ``Partial``), it matches any dict (because any extra keys are allowed).
Because of these differences, it's wisest to use ``Equal({})`` to make sure it is matched as is.

Furthermore, when you want to validate against any list or dict, use ``list`` and ``dict`` types, instead of ``[]``
or ``Schema({}, extra=PREVENT_EXTRA)``. It's simpler and more fool-proof.

License
=======

Apache 2.0 licensed. See
`LICENSE.rst <https://github.com/f-secure/pytest-voluptuous/blob/master/LICENSE.rst>`_ for more details.
