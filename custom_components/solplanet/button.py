"""Solplanet button platform."""

from __future__ import annotations

import logging
from collections import abc
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import SolplanetConfigEntry
from .const import DISCOVERY_SIGNAL, DONGLE_IDENTIFIER
from .coordinator import SolplanetDataUpdateCoordinator
from .entity import SolplanetEntity, SolplanetEntityDescription

_LOGGER = logging.getLogger(__name__)
PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class SolplanetButtonEntityDescription(SolplanetEntityDescription, ButtonEntityDescription):
    """Describe Solplanet button entity."""

    callback: abc.Callable[[], Any]


class SolplanetButton(SolplanetEntity, ButtonEntity):
    """Representation of a Solplanet button."""

    entity_description: SolplanetButtonEntityDescription

    def _set_native_value(self) -> None:
        """Buttons do not have state."""
        return

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.callback()


def create_dongle_entities_description(
    coordinator: SolplanetDataUpdateCoordinator, dongle_id: str
) -> list[SolplanetButtonEntityDescription]:
    """Create button entities for dongle actions."""
    return [
        SolplanetButtonEntityDescription(
            key=f"{dongle_id}_sync_time",
            translation_key="sync_time",
            entity_category=EntityCategory.CONFIG,
            data_field_device_type=DONGLE_IDENTIFIER,
            data_field_data_type="data",
            data_field_path=[],
            unique_id_suffix="sync_time",
            callback=lambda: coordinator.dongle_sync_time(),
        ),
        SolplanetButtonEntityDescription(
            key=f"{dongle_id}_reboot",
            translation_key="reboot",
            entity_category=EntityCategory.CONFIG,
            data_field_device_type=DONGLE_IDENTIFIER,
            data_field_data_type="data",
            data_field_path=[],
            unique_id_suffix="reboot",
            callback=lambda: coordinator.dongle_reboot(),
        ),
    ]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolplanetConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities for Solplanet from a config entry."""
    coordinator = entry.runtime_data.coordinator

    known_device_ids = set(coordinator.data[DONGLE_IDENTIFIER])

    def _create_buttons(device_ids: set[str]) -> list[SolplanetButton]:
        return [
            SolplanetButton(description=description, isn=device_id, coordinator=coordinator)
            for device_id in device_ids
            for description in create_dongle_entities_description(coordinator, device_id)
        ]

    @callback
    def _async_add_discovered_buttons(
        config_entry_id: str,
        device_type: str,
        device_ids: set[str],
    ) -> None:
        """Add buttons for dongles found after setup."""
        if config_entry_id != entry.entry_id or device_type != DONGLE_IDENTIFIER:
            return
        new_device_ids = device_ids - known_device_ids
        if not new_device_ids:
            return
        known_device_ids.update(new_device_ids)
        async_add_entities(_create_buttons(new_device_ids))

    entry.async_on_unload(async_dispatcher_connect(hass, DISCOVERY_SIGNAL, _async_add_discovered_buttons))
    async_add_entities(_create_buttons(known_device_ids))
