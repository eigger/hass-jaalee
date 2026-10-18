"""Tests for Jaalee BLE binary sensor platform."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from sensor_state_data import (
    BinarySensorDescription,
    DeviceKey,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
)
from sensor_state_data import (
    BinarySensorDeviceClass as JaaleeBinarySensorDeviceClass,
)

from custom_components.jaalee.binary_sensor import (
    BINARY_SENSOR_DESCRIPTIONS,
    sensor_update_to_bluetooth_data_update,
)


def test_sensor_update_to_bluetooth_data_update() -> None:
    """Test converting a SensorUpdate with binary sensor data to PassiveBluetoothDataUpdate."""
    dev_key = DeviceKey("motion", "dev1")
    dev_info = SensorDeviceInfo(
        name="Test Motion",
        manufacturer="Jaalee",
        model="JHT-Motion",
        hw_version="1.0",
        sw_version="2.0",
    )
    update = SensorUpdate(
        title="Test Motion",
        devices={"dev1": dev_info},
        binary_entity_descriptions={
            dev_key: BinarySensorDescription(
                dev_key, JaaleeBinarySensorDeviceClass.MOTION
            )
        },
        binary_entity_values={dev_key: SensorValue(dev_key, "Motion Sensor", True)},
    )

    bt_update = sensor_update_to_bluetooth_data_update(update)

    assert len(bt_update.entity_descriptions) == 1
    assert len(bt_update.entity_data) == 1
    assert len(bt_update.entity_names) == 1

    first_key = next(iter(bt_update.entity_descriptions))
    assert first_key.key == "motion"
    assert first_key.device_id == "dev1"

    description = bt_update.entity_descriptions[first_key]
    assert description.device_class == BinarySensorDeviceClass.MOTION

    assert bt_update.entity_data[first_key] is True
    assert bt_update.entity_names[first_key] == "Motion Sensor"


def test_binary_sensor_descriptions_complete() -> None:
    """Verify common binary sensor device classes have valid entity descriptions."""
    classes = [
        JaaleeBinarySensorDeviceClass.BATTERY,
        JaaleeBinarySensorDeviceClass.BATTERY_CHARGING,
        JaaleeBinarySensorDeviceClass.MOTION,
        JaaleeBinarySensorDeviceClass.OPENING,
        JaaleeBinarySensorDeviceClass.PRESENCE,
        JaaleeBinarySensorDeviceClass.MOISTURE,
    ]
    for cls in classes:
        assert cls in BINARY_SENSOR_DESCRIPTIONS
        desc = BINARY_SENSOR_DESCRIPTIONS[cls]
        assert desc.key == cls


async def test_binary_sensor_entity_lifecycle(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test dynamically adding and updating binary sensor entities via coordinator."""
    coordinator = loaded_entry.runtime_data
    dev_key = DeviceKey("opening", None)
    dev_info = SensorDeviceInfo(
        name="Door Sensor",
        manufacturer="Jaalee",
        model="JHT-Door",
        hw_version="1.0",
        sw_version="2.0",
    )

    # Initial update: door is open (True -> 'on')
    update_open = SensorUpdate(
        title="Door Sensor",
        devices={None: dev_info},
        binary_entity_descriptions={
            dev_key: BinarySensorDescription(
                dev_key, JaaleeBinarySensorDeviceClass.OPENING
            )
        },
        binary_entity_values={dev_key: SensorValue(dev_key, "Door", True)},
    )
    for processor in coordinator._processors:
        processor.async_handle_update(update_open, True)
    await hass.async_block_till_done()

    door_state = hass.states.get("binary_sensor.door_sensor_door")
    if not door_state:
        # Search by substring if entity id naming varies
        for state in hass.states.async_all():
            if "door" in state.entity_id or "opening" in state.entity_id:
                door_state = state
                break

    assert door_state is not None
    assert door_state.state == STATE_ON
    assert door_state.attributes.get("device_class") == BinarySensorDeviceClass.OPENING

    # Second update: door is closed (False -> 'off')
    update_closed = SensorUpdate(
        title="Door Sensor",
        devices={None: dev_info},
        binary_entity_descriptions={
            dev_key: BinarySensorDescription(
                dev_key, JaaleeBinarySensorDeviceClass.OPENING
            )
        },
        binary_entity_values={dev_key: SensorValue(dev_key, "Door", False)},
    )
    for processor in coordinator._processors:
        processor.async_handle_update(update_closed, True)
    await hass.async_block_till_done()

    door_state = hass.states.get(door_state.entity_id)
    assert door_state.state == STATE_OFF
