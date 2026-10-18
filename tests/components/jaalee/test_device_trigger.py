"""Tests for Jaalee BLE device triggers."""

from __future__ import annotations

import pytest
from homeassistant.components.device_automation import (
    InvalidDeviceAutomationConfig,
)
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)

from custom_components.jaalee.const import (
    CONF_DISCOVERED_EVENT_CLASSES,
    CONF_SUBTYPE,
    DOMAIN,
    EVENT_CLASS,
    EVENT_CLASS_BUTTON,
    EVENT_CLASS_DIMMER,
    EVENT_TYPE,
    JAALEE_BLE_EVENT,
)
from custom_components.jaalee.device_trigger import (
    async_attach_trigger,
    async_get_triggers,
    async_validate_trigger_config,
    get_event_types_by_event_class,
)

from .conftest import ADDRESS


@pytest.fixture
async def entry_with_device(
    hass: HomeAssistant,
) -> tuple[MockConfigEntry, dr.DeviceEntry]:
    """Mock config entry with discovered event classes and a device registered."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=ADDRESS,
        title="JHT EEFF",
        data={
            CONF_DISCOVERED_EVENT_CLASSES: [EVENT_CLASS_BUTTON, EVENT_CLASS_DIMMER],
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    dev_reg = dr.async_get(hass)
    device = dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, ADDRESS)},
    )
    return entry, device


async def test_get_event_types_by_event_class() -> None:
    """Test getting event types for button and dimmer classes."""
    button_types = get_event_types_by_event_class(EVENT_CLASS_BUTTON)
    assert "press" in button_types
    assert "double_press" in button_types
    assert "hold_press" in button_types

    dimmer_types = get_event_types_by_event_class(EVENT_CLASS_DIMMER)
    assert "rotate_left" in dimmer_types
    assert "rotate_right" in dimmer_types

    # Unknown class
    assert get_event_types_by_event_class("unknown") == set()


async def test_get_triggers(
    hass: HomeAssistant,
    entry_with_device: tuple[MockConfigEntry, dr.DeviceEntry],
) -> None:
    """Test retrieving triggers for a device."""
    _, device = entry_with_device

    triggers = await async_get_triggers(hass, device.id)
    assert len(triggers) > 0

    types = {t[CONF_TYPE] for t in triggers}
    assert EVENT_CLASS_BUTTON in types
    assert EVENT_CLASS_DIMMER in types

    subtypes = {t[CONF_SUBTYPE] for t in triggers if t[CONF_TYPE] == EVENT_CLASS_BUTTON}
    assert "press" in subtypes
    assert "double_press" in subtypes


async def test_validate_trigger_config(
    hass: HomeAssistant,
    entry_with_device: tuple[MockConfigEntry, dr.DeviceEntry],
) -> None:
    """Test trigger configuration validation."""
    _, device = entry_with_device

    # Valid trigger config
    valid_config = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: device.id,
        CONF_DOMAIN: DOMAIN,
        CONF_TYPE: EVENT_CLASS_BUTTON,
        CONF_SUBTYPE: "press",
    }
    validated = await async_validate_trigger_config(hass, valid_config)
    assert validated == valid_config

    # Invalid event class
    invalid_class_config = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: device.id,
        CONF_DOMAIN: DOMAIN,
        CONF_TYPE: "non_existent_class",
        CONF_SUBTYPE: "press",
    }
    with pytest.raises(
        InvalidDeviceAutomationConfig, match="is not valid for device_id"
    ):
        await async_validate_trigger_config(hass, invalid_class_config)

    # Invalid event subtype
    invalid_subtype_config = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: device.id,
        CONF_DOMAIN: DOMAIN,
        CONF_TYPE: EVENT_CLASS_BUTTON,
        CONF_SUBTYPE: "not_a_button_action",
    }
    with pytest.raises(
        InvalidDeviceAutomationConfig, match="is not valid for device_id"
    ):
        await async_validate_trigger_config(hass, invalid_subtype_config)


async def test_attach_trigger_and_fire(
    hass: HomeAssistant,
    entry_with_device: tuple[MockConfigEntry, dr.DeviceEntry],
) -> None:
    """Test attaching and firing a device trigger via JAALEE_BLE_EVENT."""
    _, device = entry_with_device
    action_calls = []

    async def mock_action(run_variables, context=None):
        action_calls.append(run_variables)

    config = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: device.id,
        CONF_DOMAIN: DOMAIN,
        CONF_TYPE: EVENT_CLASS_BUTTON,
        CONF_SUBTYPE: "press",
    }

    remove = await async_attach_trigger(
        hass,
        config,
        mock_action,
        {
            "domain": DOMAIN,
            "name": "device",
            "variables": {},
            "trigger_data": {},
        },
    )

    # Fire JAALEE_BLE_EVENT
    hass.bus.async_fire(
        JAALEE_BLE_EVENT,
        {
            CONF_DEVICE_ID: device.id,
            EVENT_CLASS: EVENT_CLASS_BUTTON,
            EVENT_TYPE: "press",
        },
    )
    await hass.async_block_till_done()

    assert len(action_calls) == 1

    # Remove trigger callback and fire again
    remove()
    hass.bus.async_fire(
        JAALEE_BLE_EVENT,
        {
            CONF_DEVICE_ID: device.id,
            EVENT_CLASS: EVENT_CLASS_BUTTON,
            EVENT_TYPE: "press",
        },
    )
    await hass.async_block_till_done()

    assert len(action_calls) == 1
