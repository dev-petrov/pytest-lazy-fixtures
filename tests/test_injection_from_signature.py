import pytest

from pytest_lazy_fixtures import lf, lfc


@pytest.mark.parametrize("foo", [lfc(lambda one: str(one))])
def test_inject_from_signature_simple(foo):
    assert foo == "1"


@pytest.mark.parametrize(
    "foo",
    [
        lfc(lambda one: str(one), lf("two")),
        lfc(lambda one: str(one), one=lf("two")),
    ],
)
def test_inject_from_signature_override(foo):
    assert foo == "2"


@pytest.mark.parametrize(
    "foo",
    [
        lfc(lambda one, two: [str(one), str(two)], two=lf("three")),
    ],
)
def test_inject_first_param_implicit_second_explicit(foo):
    assert foo == ["1", "3"]


@pytest.mark.parametrize(
    "foo",
    [
        lfc(lambda one, two: [str(one), str(two)], lf("three")),
        lfc(lambda one, two: [str(one), str(two)], one=lf("three")),
    ],
)
def test_inject_first_param_explicit_second_implicit(foo):
    assert foo == ["3", "2"]


@pytest.mark.parametrize("foo", [lfc(lambda one=42: str(one))])
def test_defaults_prevent_implicit_injection(foo):
    assert foo == "42"
