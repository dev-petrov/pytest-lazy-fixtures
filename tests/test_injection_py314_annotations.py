"""Regression test for https://github.com/dev-petrov/pytest-lazy-fixtures/issues/53

lfc must not eagerly evaluate a callable's annotations when inspecting its
signature. On Python 3.14+ (PEP 649) annotations are evaluated lazily, and a
parameter annotated (unquoted) with a name that only exists under
`if TYPE_CHECKING:` must not raise `NameError` when lfc introspects the callable.

IMPORTANT: do NOT add `from __future__ import annotations` to this module. That
future import turns annotations back into strings, which would mask the very
bug this test guards against (the unquoted forward reference must stay a real
PEP 649 lazy annotation for the test to be meaningful).
"""

import sys

import pytest

from pytest_lazy_fixtures import lf, lfc

pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 14),
    reason="PEP 649 lazy annotations (unquoted forward reference) require Python 3.14+",
)


def test_lfc_ignores_type_checking_only_annotation():
    # `Missing` never exists at runtime, mimicking an import guarded behind
    # `if TYPE_CHECKING:` (e.g. to avoid a circular import).
    class Thing:
        def __init__(self, one: Missing) -> None:  # type: ignore [name-defined] # noqa: F821  (`Missing` is TYPE_CHECKING-only)
            self.value = one

    # Building the lfc inspects Thing's signature. Before the fix this raised
    # NameError: name 'Missing' is not defined.
    wrapper = lfc(Thing, lf("one"))

    assert wrapper._func is Thing
