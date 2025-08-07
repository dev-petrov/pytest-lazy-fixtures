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
    # we need to check exact type
    if type(value) is dict:
        new_value = {load_lazy_fixtures(key, request): load_lazy_fixtures(val, request) for key, val in value.items()}
        if new_value != value:
            return new_value
    # we need to check exact type
    if type(value) in {list, tuple, set}:
        new_value = type(value)(load_lazy_fixtures(val, request) for val in value)
        if new_value != value:
            return new_value
    return value
