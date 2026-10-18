"""Tests for Jaalee BLE sensor platform."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_UNIT_OF_MEASUREMENT,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import (
    deliver_advertisement,
    make_service_info,
)


async def test_sensors(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test sensor creation and state values."""
    # With VALID_JAALEE_DATA:
    # temp: 25.0 °C, hum: 50.0 %, battery: 100 %
    states = hass.states.async_all()
    entity_ids = [s.entity_id for s in states]

    temp_state = hass.states.get("sensor.jaalee_jht_eeff_temperature")
    if not temp_state:
        # Check alternative entity id format
        for s in states:
            if "temperature" in s.entity_id:
                temp_state = s
                break

    assert temp_state is not None, f"Available entities: {entity_ids}"
    assert temp_state.state == "25.0"
    assert temp_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert temp_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE

    # Humidity sensor
    hum_state = next((s for s in states if "humidity" in s.entity_id), None)
    assert hum_state is not None
    assert hum_state.state == "50.0"
    assert hum_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert hum_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.HUMIDITY

    # Battery sensor
    batt_state = next((s for s in states if "battery" in s.entity_id), None)
    assert batt_state is not None
    assert batt_state.state == "100"
    assert batt_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert batt_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY


async def test_sensor_updates(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test updating sensor values on subsequent advertisements."""
    # (0 + 45) / 175 * 65535 = 16852 (0x41D4) -> 0.0°C
    # (60 / 100) * 65535 = 39321 (0x9999) -> 60.0%
    # battery: 0x50 -> 80%
    data = bytes(16) + b"\xf5\x25\x41\xd4\x99\x99\x00\x50"
    info = make_service_info(data=data)
    await deliver_advertisement(hass, loaded_entry, info)

    states = hass.states.async_all()
    temp_state = next((s for s in states if "temperature" in s.entity_id), None)
    hum_state = next((s for s in states if "humidity" in s.entity_id), None)
    batt_state = next((s for s in states if "battery" in s.entity_id), None)

    assert temp_state is not None
    assert temp_state.state == "0.0"

    assert hum_state is not None
    assert hum_state.state == "60.0"

    assert batt_state is not None
    assert batt_state.state == "80"
