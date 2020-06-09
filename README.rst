.. image:: https://img.shields.io/pypi/v/pytest-voluptuous.svg?style=flat
   :alt: PyPI Package latest release
   :target: https://pypi.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/pyversions/pytest-voluptuous.svg?style=flat
   :alt: Supported versions
   :target: https://pypi.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/implementation/pytest-voluptuous.svg?style=flat
   :alt: Supported implementations
   :target: https://pypi.org/pypi/pytest-voluptuous

.. image:: https://img.shields.io/pypi/l/pytest-voluptuous.svg?style=flat
   :alt: License
   :target: https://pypi.org/pypi/pytest-voluptuous

.. image:: https://travis-ci.org/F-Secure/pytest-voluptuous.svg?branch=master
   :target: https://travis-ci.org/f-secure/pytest-voluptuous
   :alt: Travis-CI

.. image:: https://coveralls.io/repos/github/F-Secure/pytest-voluptuous/badge.svg?branch=master
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
       resp = requests.get('https://pypi.org/pypi/pytest/json')
       assert S({
          'info': Partial({
              'package_url': 'https://pypi.org/project/pytest/',
              'platform': 'INVALID VALUE',
              'description': Length(max=10),
              'downloads': list,
              'classifiers': dict,
          }),
          'releases': dict,
          'urls': int
       }) == resp.json()

If validation fails, comparison returns ``False`` and assert fails, printing error details like::

    E       AssertionError: assert failed due to validation error(s):
    E         - info.platform: not a valid value for dictionary value (actual: 'unix')
    E         - info.description: length of value must be at most 10 for dictionary value (actual: ".. image:: https://...")
    E         - info.downloads: expected list for dictionary value (actual: {'last_month': -1, 'last_week': -1, 'last_day': -1})
    E         - info.classifiers: expected dict for dictionary value (actual: [u'Development Status :: 6 - Mature', ...])
    E         - last_serial: extra keys not allowed (actual: 4422291)
    E         - urls: expected int (actual: [{u'has_sig': False, u'upload_time': u'2018-10-27T16:31:24', ...}])

Install
=======

Works on python 2.7 and 3.4+::

    pip install pytest-voluptuous

Changelog
=========

See `CHANGELOG <https://github.com/F-Secure/pytest-voluptuous/blob/master/CHANGELOG.rst>`_.

Features
========

- Provides **utility schemas** (``S``, ``Exact`` and ``Partial``) to cut down boilerplate.
- Implement a **pytest hook** to provide error details on ``assert`` failure.
- Print descriptive validation **failure messages**.
- ``Equal`` and ``Unordered`` validators (contributed to voluptuous project, available in 0.10+).

Why?
====

Because writing:

>>> r = {'info': {'package_url': 'https://pypi.org/pypi/pytest'}}
>>> assert 'info' in r
>>> assert 'package_url' in r['info']
>>> assert r['info']['package_url'] == 'https://pypi.org/pypi/pytest'

...is just *way* too annoying.

Why not `JSON schema <http://json-schema.org/>`_? It's **too verbose**, too inconvenient. JSON schema will never
match the convenience of a validation library that can utilize the goodies of the platform.

Why voluptuous and not some other library? No special reason - but it's pretty easy to use and understand. Also, the
syntax is quite compact.

Usage
=====

Intro
-----

Start by specifying a schema:

>>> from pytest_voluptuous import S, Partial, Exact
>>> from voluptuous.validators import All, Length
>>> schema = S({
...     'info': Partial({
...         'package_url': 'https://pypi.org/project/pytest/',
...         'platform': 'unix',
...         'description': Length(min=100),
...         'downloads': dict,
...         'classifiers': list,
...     }),
...     'urls': list
... })

Then load up the data to validate:

>>> import requests
>>> data = requests.get('https://pypi.org/pypi/pytest/json').json()

Now if you assert this, the data will be validated against the schema, but instead of raising an error, the comparison
will just evaluate to ``False`` which fails the assert:

>>> assert data == schema
Traceback (most recent call last):
    ...
AssertionError

Now getting ``AssertionError`` in case the data doesn't match the schema is not very nice but don't worry - there's
no pytest magic in play here but once you run through pytest you'll rather get::

    E       AssertionError: assert failed due to validation error(s):
    E         - info.platform: not a valid value for dictionary value (actual: 'unix')
    E         - info.description: length of value must be at most 10 for dictionary value (actual: ".. image:: https://docs.pytest.org/en/latest/_static/pytest1.png\n   :target: https://docs.pytest.org/en/latest/\n   :align: center\n   :alt: pytest\n\n\n------\n\n.. image:: https://img.shields.io/pypi/v/pytest.svg\n    :target: https://pypi.org/project/pytest/\n\n.. image:: https://img.shields.io/conda/vn/conda-forge/pytest.svg\n    :target: https://anaconda.org/conda-forge/pytest\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest.svg\n    :target: https://pypi.org/project/pytest/\n\n.. image:: https://codecov.io/gh/pytest-dev/pytest/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/pytest-dev/pytest\n    :alt: Code coverage Status\n\n.. image:: https://travis-ci.org/pytest-dev/pytest.svg?branch=master\n    :target: https://travis-ci.org/pytest-dev/pytest\n\n.. image:: https://ci.appveyor.com/api/projects/status/mrgbjaua7t33pg6b?svg=true\n    :target: https://ci.appveyor.com/project/pytestbot/pytest\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://www.codetriage.com/pytest-dev/pytest/badges/users.svg\n    :target: https://www.codetriage.com/pytest-dev/pytest\n\nThe ``pytest`` framework makes it easy to write small tests, yet\nscales to support complex functional testing for applications and libraries.\n\nAn example of a simple test:\n\n.. code-block:: python\n\n    # content of test_sample.py\n    def inc(x):\n        return x + 1\n\n\n    def test_answer():\n        assert inc(3) == 5\n\n\nTo execute it::\n\n    $ pytest\n    ============================= test session starts =============================\n    collected 1 items\n\n    test_sample.py F\n\n    ================================== FAILURES ===================================\n    _________________________________ test_answer _________________________________\n\n        def test_answer():\n    >       assert inc(3) == 5\n    E       assert 4 == 5\n    E        +  where 4 = inc(3)\n\n    test_sample.py:5: AssertionError\n    ========================== 1 failed in 0.04 seconds ===========================\n\n\nDue to ``pytest``'s detailed assertion introspection, only plain ``assert`` statements are used. See `getting-started <https://docs.pytest.org/en/latest/getting-started.html#our-first-test-run>`_ for more examples.\n\n\nFeatures\n--------\n\n- Detailed info on failing `assert statements <https://docs.pytest.org/en/latest/assert.html>`_ (no need to remember ``self.assert*`` names);\n\n- `Auto-discovery\n  <https://docs.pytest.org/en/latest/goodpractices.html#python-test-discovery>`_\n  of test modules and functions;\n\n- `Modular fixtures <https://docs.pytest.org/en/latest/fixture.html>`_ for\n  managing small or parametrized long-lived test resources;\n\n- Can run `unittest <https://docs.pytest.org/en/latest/unittest.html>`_ (or trial),\n  `nose <https://docs.pytest.org/en/latest/nose.html>`_ test suites out of the box;\n\n- Python 2.7, Python 3.4+, PyPy 2.3, Jython 2.5 (untested);\n\n- Rich plugin architecture, with over 315+ `external plugins <http://plugincompat.herokuapp.com>`_ and thriving community;\n\n\nDocumentation\n-------------\n\nFor full documentation, including installation, tutorials and PDF documents, please see https://docs.pytest.org/en/latest/.\n\n\nBugs/Requests\n-------------\n\nPlease use the `GitHub issue tracker <https://github.com/pytest-dev/pytest/issues>`_ to submit bugs or request features.\n\n\nChangelog\n---------\n\nConsult the `Changelog <https://docs.pytest.org/en/latest/changelog.html>`__ page for fixes and enhancements of each version.\n\n\nLicense\n-------\n\nCopyright Holger Krekel and others, 2004-2018.\n\nDistributed under the terms of the `MIT`_ license, pytest is free and open source software.\n\n.. _`MIT`: https://github.com/pytest-dev/pytest/blob/master/LICENSE\n\n\n")
    E         - info.downloads: expected list for dictionary value (actual: {'last_month': -1, 'last_week': -1, 'last_day': -1})
    E         - info.classifiers: expected dict for dictionary value (actual: [u'Development Status :: 6 - Mature', u'Intended Audience :: Developers', u'License :: OSI Approved :: MIT License', u'Operating System :: MacOS :: MacOS X', u'Operating System :: Microsoft :: Windows', u'Operating System :: POSIX', u'Programming Language :: Python :: 2', u'Programming Language :: Python :: 2.7', u'Programming Language :: Python :: 3', u'Programming Language :: Python :: 3.4', u'Programming Language :: Python :: 3.5', u'Programming Language :: Python :: 3.6', u'Programming Language :: Python :: 3.7', u'Topic :: Software Development :: Libraries', u'Topic :: Software Development :: Testing', u'Topic :: Utilities'])
    E         - last_serial: extra keys not allowed (actual: 4422291)
    E         - urls: expected int (actual: [{u'has_sig': False, u'upload_time': u'2018-10-27T16:31:24', u'comment_text': u'', u'python_version': u'py2.py3', u'url': u'https://files.pythonhosted.org/packages/02/75/d041ed00994fbac4c5183e6f4bf6c906506bef8da7a57ef3fc825f171020/pytest-3.9.3-py2.py3-none-any.whl', u'md5_digest': u'150289b7b6658b62b3eddb96c4474e9d', u'downloads': -1, u'requires_python': u'>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*', u'filename': u'pytest-3.9.3-py2.py3-none-any.whl', u'packagetype': u'bdist_wheel', u'digests': {u'sha256': u'bf47e8ed20d03764f963f0070ff1c8fda6e2671fc5dd562a4d3b7148ad60f5ca', u'md5': u'150289b7b6658b62b3eddb96c4474e9d'}, u'size': 214163}, {u'has_sig': False, u'upload_time': u'2018-10-27T16:31:26', u'comment_text': u'', u'python_version': u'source', u'url': u'https://files.pythonhosted.org/packages/28/09/f73d49a5b0b714e2d4712f044686cb8fa954aac15f4b7ea557049210179f/pytest-3.9.3.tar.gz', u'md5_digest': u'32ca214ba15bbd8680d9d807a371c385', u'downloads': -1, u'requires_python': u'>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*', u'filename': u'pytest-3.9.3.tar.gz', u'packagetype': u'sdist', u'digests': {u'sha256': u'a9e5e8d7ab9d5b0747f37740276eb362e6a76275d76cebbb52c6049d93b475db', u'md5': u'32ca214ba15bbd8680d9d807a371c385'}, u'size': 882503}])

Details
-------

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

Apache 2.0 licensed. See `LICENSE <https://github.com/F-Secure/pytest-voluptuous/blob/master/LICENSE.rst>`_ for
more details.
