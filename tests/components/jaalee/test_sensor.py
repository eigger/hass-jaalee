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


async def test_sensors(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test sensor creation and state values."""
    # With VALID_JAALEE_DATA:
    # temp: 25.0 °C, hum: 50.0 %, battery: 100 %
    from homeassistant.components.sensor import SensorStateClass
    from homeassistant.helpers import entity_registry as er

    from .conftest import ADDRESS

    ent_reg = er.async_get(hass)

    # Temperature sensor
    temp_entry = ent_reg.async_get("sensor.jaalee_jht_eeff_temperature")
    assert temp_entry is not None
    assert temp_entry.unique_id == f"{ADDRESS}-temperature"

    temp_state = hass.states.get("sensor.jaalee_jht_eeff_temperature")
    assert temp_state is not None
    assert temp_state.state == "25.0"
    assert temp_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert temp_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE
    assert temp_state.attributes["state_class"] == SensorStateClass.MEASUREMENT

    # Humidity sensor
    hum_entry = ent_reg.async_get("sensor.jaalee_jht_eeff_humidity")
    assert hum_entry is not None
    assert hum_entry.unique_id == f"{ADDRESS}-humidity"

    hum_state = hass.states.get("sensor.jaalee_jht_eeff_humidity")
    assert hum_state is not None
    assert hum_state.state == "50.0"
    assert hum_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert hum_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.HUMIDITY
    assert hum_state.attributes["state_class"] == SensorStateClass.MEASUREMENT

    # Battery sensor
    batt_entry = ent_reg.async_get("sensor.jaalee_jht_eeff_battery")
    assert batt_entry is not None
    assert batt_entry.unique_id == f"{ADDRESS}-battery"

    batt_state = hass.states.get("sensor.jaalee_jht_eeff_battery")
    assert batt_state is not None
    assert batt_state.state == "100"
    assert batt_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert batt_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY
    assert batt_state.attributes["state_class"] == SensorStateClass.MEASUREMENT
