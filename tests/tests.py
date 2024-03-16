import pytest

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
            pytest.lazy_fixtures("one"),
            pytest.lazy_fixtures("two"),
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
            {"a": [pytest.lazy_fixtures("one"), pytest.lazy_fixtures("two")]},
            {"a": [1, 2]},
        ),
        (
            {"a": {pytest.lazy_fixtures("one"), pytest.lazy_fixtures("two")}},
            {"a": {1, 2}},
        ),
        (
            {
                pytest.lazy_fixtures("three"),
                pytest.lazy_fixtures("two"),
                pytest.lazy_fixtures("three"),
            },
            {3, 2},
        ),
        ([pytest.lazy_fixtures("three"), pytest.lazy_fixtures("two")], [3, 2]),
        (
            {
                "first_level": {
                    "second_level": (
                        pytest.lazy_fixtures("one"),
                        pytest.lazy_fixtures("one"),
                        pytest.lazy_fixtures("two"),
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


@pytest.mark.parametrize("item", [pytest.lazy_fixtures("four")])
def test_lazy_fixture_with_fixtures(item):
    assert item == 4


@pytest.mark.parametrize(
    "only_entity,entity_value",
    [
        (
            pytest.lazy_fixtures("entity"),
            pytest.lazy_fixtures("entity.value"),
        ),
    ],
)
def test_lazy_fixture_with_attrs(only_entity, entity_value):
    assert isinstance(only_entity, Entity)
    assert entity_value == 1


@pytest.mark.parametrize(
    "message",
    [
        pytest.lazy_fixtures_callable(
            "There is two lazy fixture args, {} and {}! And one kwarg {field}! And also simple value {simple}".format,
            pytest.lazy_fixtures("one"),
            pytest.lazy_fixtures("two"),
            field=pytest.lazy_fixtures("three"),
            simple="value",
        ),
    ],
)
def test_lazy_fixture_callable_with_func(message):
    assert message == "There is two lazy fixture args, 1 and 2! And one kwarg 3! And also simple value value"


@pytest.mark.parametrize(
    "formatted",
    [
        pytest.lazy_fixtures_callable(
            "entity_format",
            pytest.lazy_fixtures("entity"),
        ),
    ],
)
def test_lazy_fixture_callable_with_lf(formatted, entity):
    assert formatted == {"value": entity.value}


@pytest.mark.parametrize(
    "result",
    [
        pytest.lazy_fixtures_callable(
            "entity.sum",
            pytest.lazy_fixtures("two"),
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
