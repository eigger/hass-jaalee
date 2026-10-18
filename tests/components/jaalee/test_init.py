"""Test component setup, unload, and reload lifecycles for Jaalee."""

from __future__ import annotations

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.jaalee import get_entry_id_from_device
from custom_components.jaalee.coordinator import (
    JaaleePassiveBluetoothProcessorCoordinator,
)


async def test_setup_and_unload(
    hass: HomeAssistant, loaded_entry: MockConfigEntry
) -> None:
    """Test full setup and clean unload."""
    assert loaded_entry.state is ConfigEntryState.LOADED
    assert isinstance(
        loaded_entry.runtime_data, JaaleePassiveBluetoothProcessorCoordinator
    )

    # Unload entry
    assert await hass.config_entries.async_unload(loaded_entry.entry_id)
    await hass.async_block_till_done()

    assert loaded_entry.state is ConfigEntryState.NOT_LOADED


async def test_reload_entry(hass: HomeAssistant, loaded_entry: MockConfigEntry) -> None:
    """Test reloading the config entry."""
    assert loaded_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_reload(loaded_entry.entry_id)
    await hass.async_block_till_done()

    assert loaded_entry.state is ConfigEntryState.LOADED


async def test_get_entry_id_from_device(
    hass: HomeAssistant, loaded_entry: MockConfigEntry
) -> None:
    """Test retrieving entry ID from device registry."""
    dev_reg = dr.async_get(hass)
    device_entries = dr.async_entries_for_config_entry(dev_reg, loaded_entry.entry_id)
    assert len(device_entries) > 0
    device = device_entries[0]

    entry_id = await get_entry_id_from_device(hass, device.id)
    assert entry_id == loaded_entry.entry_id

    # Unknown device raises ValueError
    with pytest.raises(ValueError, match="Unknown device_id"):
        await get_entry_id_from_device(hass, "non_existent_device")

    # Device without config entries raises ValueError
    from unittest.mock import MagicMock, patch

    mock_empty_device = MagicMock(config_entries=set())
    with patch.object(dev_reg, "async_get", return_value=mock_empty_device):
        with pytest.raises(ValueError, match="No config entries for device"):
            await get_entry_id_from_device(hass, "empty_device_id")
