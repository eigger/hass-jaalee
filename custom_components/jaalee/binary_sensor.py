"""Support for Jaalee binary sensors."""

from __future__ import annotations

from .jaalee_ble import (
    BinarySensorDeviceClass as JaaleeBinarySensorDeviceClass,
    SensorUpdate,
)

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataUpdate,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.sensor import sensor_device_info_to_hass_device_info

from .coordinator import JaaleePassiveBluetoothDataProcessor
from .device import device_key_to_bluetooth_entity_key
from .types import JaaleeConfigEntry

BINARY_SENSOR_DESCRIPTIONS = {
    JaaleeBinarySensorDeviceClass.BATTERY: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.BATTERY,
        device_class=BinarySensorDeviceClass.BATTERY,
    ),
    JaaleeBinarySensorDeviceClass.BATTERY_CHARGING: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.BATTERY_CHARGING,
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    JaaleeBinarySensorDeviceClass.CO: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.CO,
        device_class=BinarySensorDeviceClass.CO,
    ),
    JaaleeBinarySensorDeviceClass.COLD: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.COLD,
        device_class=BinarySensorDeviceClass.COLD,
    ),
    JaaleeBinarySensorDeviceClass.CONNECTIVITY: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.CONNECTIVITY,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    JaaleeBinarySensorDeviceClass.DOOR: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.DOOR,
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    JaaleeBinarySensorDeviceClass.HEAT: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.HEAT,
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    JaaleeBinarySensorDeviceClass.GARAGE_DOOR: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.GARAGE_DOOR,
        device_class=BinarySensorDeviceClass.GARAGE_DOOR,
    ),
    JaaleeBinarySensorDeviceClass.GAS: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.GAS,
        device_class=BinarySensorDeviceClass.GAS,
    ),
    JaaleeBinarySensorDeviceClass.GENERIC: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.GENERIC,
    ),
    JaaleeBinarySensorDeviceClass.LIGHT: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.LIGHT,
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    JaaleeBinarySensorDeviceClass.LOCK: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.LOCK,
        device_class=BinarySensorDeviceClass.LOCK,
    ),
    JaaleeBinarySensorDeviceClass.MOISTURE: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.MOISTURE,
        device_class=BinarySensorDeviceClass.MOISTURE,
    ),
    JaaleeBinarySensorDeviceClass.MOTION: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.MOTION,
        device_class=BinarySensorDeviceClass.MOTION,
    ),
    JaaleeBinarySensorDeviceClass.MOVING: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.MOVING,
        device_class=BinarySensorDeviceClass.MOVING,
    ),
    JaaleeBinarySensorDeviceClass.OCCUPANCY: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.OCCUPANCY,
        device_class=BinarySensorDeviceClass.OCCUPANCY,
    ),
    JaaleeBinarySensorDeviceClass.OPENING: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.OPENING,
        device_class=BinarySensorDeviceClass.OPENING,
    ),
    JaaleeBinarySensorDeviceClass.PLUG: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.PLUG,
        device_class=BinarySensorDeviceClass.PLUG,
    ),
    JaaleeBinarySensorDeviceClass.POWER: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.POWER,
        device_class=BinarySensorDeviceClass.POWER,
    ),
    JaaleeBinarySensorDeviceClass.PRESENCE: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.PRESENCE,
        device_class=BinarySensorDeviceClass.PRESENCE,
    ),
    JaaleeBinarySensorDeviceClass.PROBLEM: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.PROBLEM,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    JaaleeBinarySensorDeviceClass.RUNNING: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.RUNNING,
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    JaaleeBinarySensorDeviceClass.SAFETY: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.SAFETY,
        device_class=BinarySensorDeviceClass.SAFETY,
    ),
    JaaleeBinarySensorDeviceClass.SMOKE: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.SMOKE,
        device_class=BinarySensorDeviceClass.SMOKE,
    ),
    JaaleeBinarySensorDeviceClass.SOUND: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.SOUND,
        device_class=BinarySensorDeviceClass.SOUND,
    ),
    JaaleeBinarySensorDeviceClass.TAMPER: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.TAMPER,
        device_class=BinarySensorDeviceClass.TAMPER,
    ),
    JaaleeBinarySensorDeviceClass.VIBRATION: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.VIBRATION,
        device_class=BinarySensorDeviceClass.VIBRATION,
    ),
    JaaleeBinarySensorDeviceClass.WINDOW: BinarySensorEntityDescription(
        key=JaaleeBinarySensorDeviceClass.WINDOW,
        device_class=BinarySensorDeviceClass.WINDOW,
    ),
}


def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[bool | None]:
    """Convert a binary sensor update to a bluetooth data update."""
    return PassiveBluetoothDataUpdate(
        devices={
            device_id: sensor_device_info_to_hass_device_info(device_info)
            for device_id, device_info in sensor_update.devices.items()
        },
        entity_descriptions={
            device_key_to_bluetooth_entity_key(device_key): BINARY_SENSOR_DESCRIPTIONS[
                description.device_class
            ]
            for device_key, description in sensor_update.binary_entity_descriptions.items()
            if description.device_class
        },
        entity_data={
            device_key_to_bluetooth_entity_key(device_key): sensor_values.native_value
            for device_key, sensor_values in sensor_update.binary_entity_values.items()
        },
        entity_names={
            device_key_to_bluetooth_entity_key(device_key): sensor_values.name
            for device_key, sensor_values in sensor_update.binary_entity_values.items()
        },
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: JaaleeConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Jaalee BLE binary sensors."""
    coordinator = entry.runtime_data
    processor = JaaleePassiveBluetoothDataProcessor(
        sensor_update_to_bluetooth_data_update
    )
    entry.async_on_unload(
        processor.async_add_entities_listener(
            JaaleeBluetoothBinarySensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(
        coordinator.async_register_processor(processor, BinarySensorEntityDescription)
    )


class JaaleeBluetoothBinarySensorEntity(
    PassiveBluetoothProcessorEntity[JaaleePassiveBluetoothDataProcessor[bool | None]],
    BinarySensorEntity,
):
    """Representation of a Jaalee binary sensor."""

    @property
    def is_on(self) -> bool | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available
