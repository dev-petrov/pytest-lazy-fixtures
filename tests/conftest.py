import pytest

from tests.entity import Entity

pytest_plugins = "pytest_lazy_fixtures.plugin"


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
