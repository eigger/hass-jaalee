"""Tests for Jaalee BLE event platform."""

from __future__ import annotations

from homeassistant.components.event import EventDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_send
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.jaalee import (
    format_discovered_event_class,
    format_event_dispatcher_name,
)
from custom_components.jaalee.const import (
    DOMAIN,
    EVENT_CLASS,
    EVENT_CLASS_BUTTON,
    EVENT_CLASS_DIMMER,
    EVENT_PROPERTIES,
    EVENT_TYPE,
    JaaleeBleEvent,
)

from .conftest import ADDRESS


async def test_event_discovery_and_trigger(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test dynamically discovering an event class and triggering events."""
    event_data: JaaleeBleEvent = {
        "device_id": "mock_device_id",
        "address": ADDRESS,
        EVENT_CLASS: EVENT_CLASS_BUTTON,
        EVENT_TYPE: "press",
        EVENT_PROPERTIES: None,
    }

    # Discover button event
    async_dispatcher_send(
        hass,
        format_discovered_event_class(ADDRESS),
        EVENT_CLASS_BUTTON,
        event_data,
    )
    await hass.async_block_till_done()

    # Find created event entity
    event_states = [s for s in hass.states.async_all() if s.domain == "event"]
    assert len(event_states) == 1
    state = event_states[0]
    assert state.attributes.get("event_type") == "press"
    assert state.attributes.get("device_class") == EventDeviceClass.BUTTON

    # Trigger subsequent event on the existing entity
    next_event: JaaleeBleEvent = {
        "device_id": "mock_device_id",
        "address": ADDRESS,
        EVENT_CLASS: EVENT_CLASS_BUTTON,
        EVENT_TYPE: "double_press",
        EVENT_PROPERTIES: None,
    }
    async_dispatcher_send(
        hass,
        format_event_dispatcher_name(ADDRESS, EVENT_CLASS_BUTTON),
        next_event,
    )
    await hass.async_block_till_done()

    updated_state = hass.states.get(state.entity_id)
    assert updated_state is not None
    assert updated_state.attributes.get("event_type") == "double_press"


async def test_dimmer_event_discovery(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test discovering and triggering dimmer events."""
    event_data: JaaleeBleEvent = {
        "device_id": "mock_device_id",
        "address": ADDRESS,
        EVENT_CLASS: EVENT_CLASS_DIMMER,
        EVENT_TYPE: "rotate_left",
        EVENT_PROPERTIES: {"steps": 1},
    }

    async_dispatcher_send(
        hass,
        format_discovered_event_class(ADDRESS),
        EVENT_CLASS_DIMMER,
        event_data,
    )
    await hass.async_block_till_done()

    dimmer_state = next(
        (s for s in hass.states.async_all() if "dimmer" in s.entity_id), None
    )
    assert dimmer_state is not None
    assert dimmer_state.attributes.get("event_type") == "rotate_left"
    assert dimmer_state.attributes.get("steps") == 1


async def test_event_entity_restoration(
    hass: HomeAssistant,
    entry: MockConfigEntry,
) -> None:
    """Test pre-existing event entities in registry are restored during setup."""
    ent_reg = er.async_get(hass)
    # Register an event entity before config entry setup
    ent_reg.async_get_or_create(
        "event",
        DOMAIN,
        f"{ADDRESS}-{EVENT_CLASS_BUTTON}",
        config_entry=entry,
    )

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    # Entity is restored with no initial event
    restored = next((s for s in hass.states.async_all() if s.domain == "event"), None)
    assert restored is not None
    assert restored.attributes.get("event_type") is None

    # Now firing an event updates it
    event_data: JaaleeBleEvent = {
        "device_id": "mock_device_id",
        "address": ADDRESS,
        EVENT_CLASS: EVENT_CLASS_BUTTON,
        EVENT_TYPE: "triple_press",
        EVENT_PROPERTIES: None,
    }
    async_dispatcher_send(
        hass,
        format_event_dispatcher_name(ADDRESS, EVENT_CLASS_BUTTON),
        event_data,
    )
    await hass.async_block_till_done()

    updated = hass.states.get(restored.entity_id)
    assert updated.attributes.get("event_type") == "triple_press"
