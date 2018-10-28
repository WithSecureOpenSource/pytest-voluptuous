import six

from pytest_voluptuous import S, Partial, Exact, Unordered
from voluptuous.validators import All, Length

from pytest_voluptuous.plugin import pytest_assertrepr_compare

TEST_DATA = {
    'info': {
        'package_url': 'http://pypi.python.org/pypi/pytest',
        'platform': 'unix',
        'description': 'lorem ipsum lorem ipsum',
        'downloads': {
            'last_month': 0
        },
        'classifiers': [
            'Development Status :: 6 - Mature',
            'Intended Audience :: Developers'
        ]
    },
    'releases': {
        '3.1.3': [],
        '3.0.7': []
    },
    'urls': [{}, {}]
}


def test_validation_ok():
    assert S({
        'info': Partial({
            'package_url': 'http://pypi.python.org/pypi/pytest',
            'platform': 'unix',
            'description': Length(min=10),
            'downloads': dict,
            'classifiers': list,
        }),
        'releases': {
            any: list
        },
        'urls': list
    }) == TEST_DATA


def test_error_reporting():
    expected = S({
        'info': Partial({
            'package_url': 'http://pypi.python.org/pypi/pytest',
            'platform': 'INVALID VALUE',
            'description': Length(max=10),
            'downloads': list,
            'classifiers': dict,
        }),
        'urls': int
    })
    _ = expected == TEST_DATA
    msgs = pytest_assertrepr_compare('==', expected, TEST_DATA)
    assert S(Unordered([
        "failed to validation error(s):",
        "- info.platform: not a valid value",
        "- info.description: length of value must be at most 10",
        "- info.downloads: expected list",
        "- info.classifiers: expected dict",
        "- urls: expected int",
        "- releases: extra keys not allowed"
    ])) == msgs

    # TODO: How to assert the actual output?
    # assert expected == resp.json()
    # from _pytest.capture import capfd
    # out, err = capfd.readouterr()
    # assert out == \
    #     "assert failed to validation error(s):\n"
    #     "- info.platform: not a valid value\n"
    #     "- info.description: length of value must be at most 10\n"
    #     "- info.downloads: expected list\n"
    #     "- info.classifiers: expected dict\n"
    #     "- urls: expected int\n"
    #     "- releases: extra keys not allowed"
    # ]


def test_unordered():
    actual = ["foobar", "barbaz", "baz"]
    expected = S(Unordered(["foo", "bar", "baz"]))
    _ = expected == actual
    msgs = pytest_assertrepr_compare('==', expected, actual)
    assert S(Unordered([
        "failed to validation error(s):",
        "- Element #0 (foobar) is not valid against any validator",
        "- Element #1 (barbaz) is not valid against any validator",
    ])) == msgs


def test_list_error_reporting():

    # OK: List of objects
    sch = S({'foo': [int]})
    data = {'foo': ['a', 'b']}
    assert (sch == data) is False
    assert len(sch.error.errors) == 2
    assert sch.error.errors[0].path == ['foo', 0]
    assert sch.error.errors[1].path == ['foo', 1]
    msgs = pytest_assertrepr_compare('==', sch, data)
    assert msgs == [
        "failed to validation error(s):",
        "- foo.0: expected int",
        "- foo.1: expected int"
    ]

    sch = S({'foo': [{'id': int}]})
    data = {'foo': [{'id': 'bar'}, {'id': 'bar2'}]}
    assert (sch == data) is False
    assert len(sch.error.errors) == 1  # XXX: Until https://github.com/alecthomas/voluptuous/pull/330 gets merged
    assert sch.error.errors[0].path == ['foo', 0, 'id']
    msgs = pytest_assertrepr_compare('==', sch, data)
    assert msgs == [
        "failed to validation error(s):",
        "- foo.0.id: expected int"
    ]
