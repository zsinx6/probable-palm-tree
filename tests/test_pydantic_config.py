from __future__ import annotations
import pytest
from pydantic import ValidationError
from app.domain.orders import Money


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        Money(currency="BRL", units=100, scale=2, unexpected="nope")
