from operator import attrgetter

import pytest

from pytest_lazy_fixtures import lf, lfc
from pytest_lazy_fixtures.lazy_fixture import LazyFixtureWrapper
from pytest_lazy_fixtures.lazy_fixture_callable import LazyFixtureCallableWrapper
from tests.entity import DataNamedTuple, Entity


def test_lazy_fixture_repr():
    assert str(LazyFixtureWrapper("fixture")) == "fixture"


def test_lazy_fixture_callable_repr():
    assert str(LazyFixtureCallableWrapper("fixture")) == "fixture"


@pytest.mark.parametrize(
    ("first", "second", "other"),
    [
        (
            lf("one"),
            lf("two"),
            4,
        ),
    ],
)
def test_lazy_fixture(first, second, other):
    assert first == 1
    assert second == 2
    assert other == 4


@pytest.mark.parametrize(
    ("actual", "expected"),
    [
        (
            {"a": [lf("one"), lf("two")]},
            {"a": [1, 2]},
        ),
        (
            {"a": {lf("one"), lf("two")}},
            {"a": {1, 2}},
        ),
        (
            {
                lf("three"),
                lf("two"),
                lf("three"),
            },
            {3, 2},
        ),
        ([lf("three"), lf("two")], [3, 2]),
        (
            {
                "first_level": {
                    "second_level": (
                        lf("one"),
                        lf("one"),
                        lf("two"),
                    ),
                    "not_lazy_fixture": 1,
                },
            },
            {"first_level": {"second_level": (1, 1, 2), "not_lazy_fixture": 1}},
        ),
    ],
)
def test_lazy_fixture_data_types(actual, expected):
    assert actual == expected


@pytest.mark.parametrize("item", [lf("four")])
def test_lazy_fixture_with_fixtures(item):
    assert item == 4


@pytest.mark.parametrize(
    ("only_entity", "entity_value"),
    [
        (
            lf("entity"),
            lf("entity.value"),
        ),
    ],
)
def test_lazy_fixture_with_attrs(only_entity, entity_value):
    assert isinstance(only_entity, Entity)
    assert entity_value == 1


@pytest.mark.parametrize(
    "message",
    [
        lfc(
            "There is two lazy fixture args, {} and {}! And one kwarg {field}! And also simple value {simple}".format,
            lf("one"),
            lf("two"),
            field=lf("three"),
            simple="value",
        ),
    ],
)
def test_lazy_fixture_callable_with_func(message):
    assert message == "There is two lazy fixture args, 1 and 2! And one kwarg 3! And also simple value value"


@pytest.mark.parametrize(
    "value",
    [
        lfc(
            attrgetter("value"),
            lf("entity"),
        ),
    ],
)
def test_lazy_fixture_callable_with_class(value, entity):
    assert value == entity.value


@pytest.mark.parametrize(
    "formatted",
    [
        lfc(
            "entity_format",
            lf("entity"),
        ),
    ],
)
def test_lazy_fixture_callable_with_lf(formatted, entity):
    assert formatted == {"value": entity.value}


@pytest.mark.parametrize(
    "result",
    [
        lfc(
            "entity.sum",
            lf("two"),
        ),
    ],
)
def test_lazy_fixture_callable_with_attr_lf(result):
    assert result == 3


@pytest.mark.parametrize("data", [DataNamedTuple(a=1, b=2)])
def test(data):
    assert data.a == 1
    assert data.b == 2


@pytest.fixture(params=["a", "b"])
def fixture1(request):
    return request.param


def test_foo(fixture2):
    pass


@pytest.mark.parametrize(
    "test_dict",
    [
        {lf("fixture_a"): lf("fixture_b")},
    ],
)
def test_dict_a_b(test_dict):
    assert test_dict == {"a": "b"}


@pytest.mark.parametrize(
    "filters",
    [
        {
            "users": [
                lfc(lambda v: v.upper(), lf("username")),
                lfc(lambda v: v.lower(), lf("username")),
            ]
        },
    ],
)
def test_indirect_fixture(filters):
    assert filters == {"users": ["ALESSIO", "alessio"]}


def test_fixture_not_callable(request):
    fixture = lfc("entity")

    with pytest.raises(TypeError, match="Passed fixture is not callable"):
        fixture.get_func(request)
