"""Tests for the Solplanet config and options flows."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.solplanet as integration
from custom_components.solplanet.config_flow import (
    CannotConnect,
    STEP_USER_DATA_SCHEMA,
    SolplanetConfigFlow,
    SolplanetOptionsFlow,
    validate_input,
)
from custom_components.solplanet.const import CONF_INTERVAL, DOMAIN

from tests.helpers import FakeCoordinator, integration_data


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations):
    """Enable loading this repository's custom integration."""
    yield


@pytest.fixture
def user_input() -> dict:
    """Return representative form input."""
    return {CONF_HOST: "inverter.local", CONF_INTERVAL: 60}


def _entry(*, interval: int = 60, unique_id: str = "dongle-serial") -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "old.local", CONF_INTERVAL: interval},
        title="old.local",
        unique_id=unique_id,
    )


def test_interval_schema_accepts_defaults_and_supported_bounds() -> None:
    """The polling interval is coerced and constrained."""
    assert STEP_USER_DATA_SCHEMA({CONF_HOST: "inverter.local"})[CONF_INTERVAL] == 60
    assert (
        STEP_USER_DATA_SCHEMA({CONF_HOST: "inverter.local", CONF_INTERVAL: "10"})[
            CONF_INTERVAL
        ]
        == 10
    )
    assert (
        STEP_USER_DATA_SCHEMA({CONF_HOST: "inverter.local", CONF_INTERVAL: 3600})[
            CONF_INTERVAL
        ]
        == 3600
    )


@pytest.mark.parametrize("interval", [9, 3601, "not-a-number"])
def test_interval_schema_rejects_unsupported_values(interval) -> None:
    """Values outside the supported polling range are rejected."""
    with pytest.raises(vol.Invalid):
        STEP_USER_DATA_SCHEMA({CONF_HOST: "inverter.local", CONF_INTERVAL: interval})


async def test_validate_input_v2_prefers_dongle_identity(hass, user_input) -> None:
    """V2 configuration uses a stable dongle identity and the entered host as title."""
    api = SimpleNamespace(
        version="v2",
        client=SimpleNamespace(get=AsyncMock(return_value={"psn": "PSN-1"})),
        get_inverter_info=AsyncMock(
            return_value=SimpleNamespace(inv=[SimpleNamespace(isn="INV-1")])
        ),
    )
    with (
        patch("custom_components.solplanet.config_flow.SolplanetClient"),
        patch(
            "custom_components.solplanet.config_flow.SolplanetApiAdapter.create",
            AsyncMock(return_value=api),
        ),
    ):
        assert await validate_input(hass, user_input) == {
            "title": "inverter.local",
            "unique_id": "PSN-1",
        }


@pytest.mark.parametrize(
    ("identity", "expected"),
    [
        ({"ethmac": "AA:BB"}, "AA:BB"),
        ({"wlanmac": "CC:DD"}, "CC:DD"),
    ],
)
async def test_validate_input_v2_identity_fallbacks(
    hass, user_input, identity, expected
) -> None:
    """V2 uses either wired or wireless MAC when PSN is absent."""
    api = SimpleNamespace(
        version="v2",
        client=SimpleNamespace(get=AsyncMock(return_value=identity)),
        get_inverter_info=AsyncMock(return_value=SimpleNamespace(inv=[])),
    )
    with (
        patch("custom_components.solplanet.config_flow.SolplanetClient"),
        patch(
            "custom_components.solplanet.config_flow.SolplanetApiAdapter.create",
            AsyncMock(return_value=api),
        ),
    ):
        result = await validate_input(hass, user_input)
    assert result["unique_id"] == expected


async def test_validate_input_falls_back_to_inverter_or_host(hass, user_input) -> None:
    """An unavailable dongle lookup falls back through inverter serial to host."""
    api = SimpleNamespace(
        version="v2",
        client=SimpleNamespace(get=AsyncMock(side_effect=RuntimeError("offline"))),
        get_inverter_info=AsyncMock(
            return_value=SimpleNamespace(inv=[SimpleNamespace(isn="INV-1")])
        ),
    )
    with (
        patch("custom_components.solplanet.config_flow.SolplanetClient"),
        patch(
            "custom_components.solplanet.config_flow.SolplanetApiAdapter.create",
            AsyncMock(return_value=api),
        ),
    ):
        result = await validate_input(hass, user_input)
    assert result == {"title": "INV-1", "unique_id": "INV-1"}

    api.version = "v1"
    api.get_inverter_info.return_value = SimpleNamespace(inv=[])
    with (
        patch("custom_components.solplanet.config_flow.SolplanetClient"),
        patch(
            "custom_components.solplanet.config_flow.SolplanetApiAdapter.create",
            AsyncMock(return_value=api),
        ),
    ):
        result = await validate_input(hass, user_input)
    assert result == {"title": "inverter.local", "unique_id": "inverter.local"}


async def test_validate_input_wraps_connection_errors(hass, user_input) -> None:
    """Probe errors are exposed to the flow as CannotConnect."""
    with (
        patch("custom_components.solplanet.config_flow.SolplanetClient"),
        patch(
            "custom_components.solplanet.config_flow.SolplanetApiAdapter.create",
            AsyncMock(side_effect=RuntimeError("offline")),
        ),
        pytest.raises(CannotConnect),
    ):
        await validate_input(hass, user_input)


async def test_user_flow_success_and_duplicate_update(hass, user_input) -> None:
    """The user flow creates one entry and updates the host on rediscovery."""
    with patch(
        "custom_components.solplanet.config_flow.validate_input",
        AsyncMock(return_value={"title": "inverter.local", "unique_id": "PSN-1"}),
    ):
        form = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert form["type"] is FlowResultType.FORM
        result = await hass.config_entries.flow.async_configure(
            form["flow_id"], user_input
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "inverter.local"
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert entry.unique_id == "PSN-1"

    with patch(
        "custom_components.solplanet.config_flow.validate_input",
        AsyncMock(return_value={"title": "new.local", "unique_id": "PSN-1"}),
    ):
        duplicate = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data={CONF_HOST: "new.local", CONF_INTERVAL: 120},
        )
    assert duplicate["type"] is FlowResultType.ABORT
    assert duplicate["reason"] == "already_configured"
    assert entry.data[CONF_HOST] == "new.local"


@pytest.mark.parametrize(
    ("error", "reason"),
    [(CannotConnect(), "cannot_connect"), (RuntimeError("surprise"), "unknown")],
)
async def test_user_flow_reports_validation_errors(
    hass, user_input, error, reason
) -> None:
    """Expected and unexpected validation errors return the appropriate form error."""
    with patch(
        "custom_components.solplanet.config_flow.validate_input",
        AsyncMock(side_effect=error),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data=user_input,
        )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": reason}


async def test_options_flow_shows_current_value_and_updates_entry(hass) -> None:
    """The options flow persists the selected interval and reloads the entry."""
    entry = _entry(interval=30)
    entry.add_to_hass(hass)
    with patch.object(
        hass.config_entries, "async_reload", AsyncMock(return_value=True)
    ) as reload:
        form = await hass.config_entries.options.async_init(entry.entry_id)
        assert form["type"] is FlowResultType.FORM
        assert form["data_schema"]({})[CONF_INTERVAL] == 30
        result = await hass.config_entries.options.async_configure(
            form["flow_id"], {CONF_INTERVAL: 120}
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert entry.data[CONF_INTERVAL] == 120
    reload.assert_awaited_once_with(entry.entry_id)


async def test_reconfigure_flow_shows_current_value_and_reloads(hass) -> None:
    """Reconfigure updates the interval and aborts successfully."""
    entry = _entry(interval=45)
    entry.add_to_hass(hass)
    with patch.object(
        hass.config_entries, "async_reload", AsyncMock(return_value=True)
    ) as reload:
        form = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={
                "source": config_entries.SOURCE_RECONFIGURE,
                "entry_id": entry.entry_id,
            },
        )
        assert form["type"] is FlowResultType.FORM
        assert form["data_schema"]({})[CONF_INTERVAL] == 45
        result = await hass.config_entries.flow.async_configure(
            form["flow_id"], {CONF_INTERVAL: 90}
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert entry.data[CONF_INTERVAL] == 90
    reload.assert_awaited_once_with(entry.entry_id)


def test_options_flow_factory() -> None:
    """The config flow returns its dedicated options handler."""
    entry = _entry()
    assert isinstance(
        SolplanetConfigFlow.async_get_options_flow(entry), SolplanetOptionsFlow
    )


async def test_config_entry_setup_registers_real_platform_entities(hass) -> None:
    """A real config entry forwards platforms and registers their entities in HA."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="inverter.local",
        data={CONF_HOST: "inverter.local", CONF_INTERVAL: 60},
        unique_id="dongle-1",
    )
    entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})

    def metadata_factory(*_args, **kwargs):
        runtime = kwargs["runtime"]
        runtime.data.update(integration_data())
        coordinator = FakeCoordinator(runtime.data)
        coordinator.runtime = runtime
        coordinator.async_config_entry_first_refresh = AsyncMock()
        return coordinator

    def live_factory(_hass, runtime, _entry, _interval):
        coordinator = FakeCoordinator(runtime.data)
        coordinator.runtime = runtime
        coordinator.async_refresh = AsyncMock()
        return coordinator

    with (
        patch.object(integration, "async_get_clientsession", return_value="session"),
        patch.object(integration, "SolplanetClient"),
        patch.object(
            integration.SolplanetApiAdapter,
            "create",
            AsyncMock(return_value=SimpleNamespace(version="v2")),
        ),
        patch.object(
            integration,
            "SolplanetMetadataUpdateCoordinator",
            side_effect=metadata_factory,
        ),
        patch.object(
            integration,
            "SolplanetInverterUpdateCoordinator",
            side_effect=live_factory,
        ),
        patch.object(
            integration,
            "SolplanetBatteryUpdateCoordinator",
            side_effect=live_factory,
        ),
        patch.object(
            integration,
            "SolplanetMeterUpdateCoordinator",
            side_effect=live_factory,
        ),
        patch.object(
            integration,
            "SolplanetDongleUpdateCoordinator",
            side_effect=live_factory,
        ),
        patch.object(integration, "_register_devices"),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is config_entries.ConfigEntryState.LOADED

    entities = [
        registry_entry
        for registry_entry in er.async_get(hass).entities.values()
        if registry_entry.config_entry_id == entry.entry_id
    ]
    assert len(entities) > 80
    assert {registry_entry.domain for registry_entry in entities} == {
        "binary_sensor",
        "button",
        "number",
        "select",
        "sensor",
        "switch",
    }
    assert all(
        hass.states.get(registry_entry.entity_id) is not None
        for registry_entry in entities
    )
