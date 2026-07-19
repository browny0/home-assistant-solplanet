"""Tests for Solplanet payload validation."""

from types import SimpleNamespace

import pytest

from custom_components.solplanet.validation import is_zero_filled_battery_payload


_CORE_FIELDS = ("cst", "bst", "vb", "tb", "soc", "soh", "cli", "clo")


def test_zero_filled_battery_stub_is_detected() -> None:
    """All core battery values at zero identify the transient dongle stub."""
    payload = SimpleNamespace(**dict.fromkeys(_CORE_FIELDS, 0), pb=123)
    assert is_zero_filled_battery_payload(payload)


@pytest.mark.parametrize("field", _CORE_FIELDS)
def test_real_battery_value_prevents_stub_detection(field: str) -> None:
    """Any non-zero core value means the payload contains real telemetry."""
    values = dict.fromkeys(_CORE_FIELDS, 0)
    values[field] = 1
    assert not is_zero_filled_battery_payload(SimpleNamespace(**values))


def test_missing_fields_do_not_look_like_zero_values() -> None:
    """Absent fields cannot be mistaken for an all-zero response."""
    assert not is_zero_filled_battery_payload(SimpleNamespace(cst=0))
    assert not is_zero_filled_battery_payload(None)
