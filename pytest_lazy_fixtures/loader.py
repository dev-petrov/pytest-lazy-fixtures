import pytest

from .lazy_fixture import LazyFixtureWrapper
from .lazy_fixture_callable import LazyFixtureCallableWrapper


def load_lazy_fixtures(value, request: pytest.FixtureRequest):
    if isinstance(value, LazyFixtureCallableWrapper):
        return value.get_func(request)(
            *load_lazy_fixtures(value.args, request),
            **load_lazy_fixtures(value.kwargs, request),
        )
    if isinstance(value, LazyFixtureWrapper):
        return value.load_fixture(request)
    if type(value) is dict:
        for key in list(value):
            value[load_lazy_fixtures(key, request)] = load_lazy_fixtures(value.pop(key), request)
        return value
    if type(value) is list:
        for i, val in enumerate(value):
            value[i] = load_lazy_fixtures(val, request)
        return value
    if type(value) in (set, tuple):
        new_value = type(value)(load_lazy_fixtures(val, request) for val in value)
        return value if value == new_value else new_value
    return value
