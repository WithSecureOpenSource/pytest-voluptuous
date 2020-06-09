Changelog
=========

1.2.0 (2020-06-09)
------------------

**New**:

- `#7 <https://github.com/F-Secure/pytest-voluptuous/pull/7>`_:
  Officially support python 3.7 and 3.8. Add ``python_requires`` identifier to package.

**Fix**:

- `#3 <https://github.com/F-Secure/pytest-voluptuous/pull/6>`_:
  Improve the slightly confusing assertion error message.
  Thanks `@bjoluc <https://github.com/bjoluc>`_!

1.1.0 (2018-10-31)
------------------

**New**:

- `#3 <https://github.com/F-Secure/pytest-voluptuous/issues/3>`_:
  Include actual value in error messages for easier debugging (and remove duplication of error path in error message).
  Thanks `@Turbo87 <https://github.com/Turbo87>`_!

**Fix**:

- `Commit <https://github.com/F-Secure/pytest-voluptuous/pull/4/commits/885dc5bf0ec30ff345738312e842b6bb79a5bd86>`_:
  Skip path prefix in error output, if path is empty (when error is on "main level").
  Thanks `@Turbo87 <https://github.com/Turbo87>`_!

1.0.2 (2018-02-16)
------------------

**Fix**:

- `#1 <https://github.com/F-Secure/pytest-voluptuous/issues/1>`_:
  Error reporting failed on lists.
  Thanks `@rytilahti <https://github.com/rytilahti>`_!

1.0.1 (2017-01-10)
------------------

First public version.

1.0.0 (2016-12-07)
------------------

First version.
