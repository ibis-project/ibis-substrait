from __future__ import annotations

import pytest

from ibis_substrait.compiler.core import SubstraitCompiler


@pytest.fixture
def compiler():
    return SubstraitCompiler()
