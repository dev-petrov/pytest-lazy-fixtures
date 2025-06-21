import pytest

from pytest_lazy_fixtures import lf
from tests.entity import Entity

pytest_plugins = ("pytest_lazy_fixtures.plugin",)


@pytest.fixture
def one():
    return 1


@pytest.fixture
def two():
    return 2


@pytest.fixture
def three():
    return 3


@pytest.fixture
def four(one, three):
    return one + three


@pytest.fixture
def entity(one):
    return Entity(one)


@pytest.fixture
def entity_format():
    def _entity_format(entity: Entity):
        return {"value": entity.value}

    return _entity_format


@pytest.fixture
def service1(fixture1):
    return 1


@pytest.fixture
def service2(fixture1):
    return 1


@pytest.fixture
def service3(fixture1):
    return 1


@pytest.fixture
def service4(fixture1):
    return 1


@pytest.fixture
def service5(fixture1):
    return 1


@pytest.fixture(
    params=[
        lf("service1"),
        {"test": lf("service2")},
        [lf("service3")],
        (lf("service4"),),
        {lf("service5")},
    ],
)
def fixture2(request):
    return None


@pytest.fixture
def fixture_a() -> str:
    return "a"


@pytest.fixture
def fixture_b() -> str:
    return "b"


@pytest.fixture(params=["Alessio"])
def username(request):
    return request.param
