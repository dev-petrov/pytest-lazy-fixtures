import pytest

from .lazy_fixture import LazyFixtureWrapper
from .loader import load_lazy_fixtures


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    val = getattr(request, "param", None)
    if val is not None:
        request.param = load_lazy_fixtures(val, request)


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, LazyFixtureWrapper):
        return val.name
