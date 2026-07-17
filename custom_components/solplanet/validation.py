"""Validation helpers for Solplanet device payloads."""

from __future__ import annotations


_BATTERY_ZERO_STUB_FIELDS = (
    "cst",
    "bst",
    "vb",
    "tb",
    "soc",
    "soh",
    "cli",
    "clo",
)


def is_zero_filled_battery_payload(data: object) -> bool:
    """Return whether battery data matches the dongle's transient zero stub.

    A real battery may legitimately report zero for individual values such as
    power, current, or even SOC. The transient dongle response is distinct: all
    core status, health, and electrical values are zero at once.
    """
    return all(getattr(data, field, None) == 0 for field in _BATTERY_ZERO_STUB_FIELDS)
