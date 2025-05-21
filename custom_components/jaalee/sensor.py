"""Support for Jaalee sensors."""

from __future__ import annotations

from typing import cast

from .jaalee_ble import SensorDeviceClass as JaaleeSensorDeviceClass, SensorUpdate, Units
from .jaalee_ble.const import (
    ExtendedSensorDeviceClass as JaaleeExtendedSensorDeviceClass,
)

from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataUpdate,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_SW_VERSION,
    ATTR_HW_VERSION,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DEGREE,
    LIGHT_LUX,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfConductivity,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfMass,
    UnitOfPower,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.sensor import sensor_device_info_to_hass_device_info

from .coordinator import JaaleePassiveBluetoothDataProcessor
from .device import device_key_to_bluetooth_entity_key
from .types import JaaleeConfigEntry

SENSOR_DESCRIPTIONS = {
    # Acceleration (m/s²)
    (
        JaaleeSensorDeviceClass.ACCELERATION,
        Units.ACCELERATION_METERS_PER_SQUARE_SECOND,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.ACCELERATION}_{Units.ACCELERATION_METERS_PER_SQUARE_SECOND}",
        native_unit_of_measurement=Units.ACCELERATION_METERS_PER_SQUARE_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Battery (percent)
    (JaaleeSensorDeviceClass.BATTERY, Units.PERCENTAGE): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.BATTERY}_{Units.PERCENTAGE}",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Channel (-)
    (JaaleeExtendedSensorDeviceClass.CHANNEL, None): SensorEntityDescription(
        key=str(JaaleeExtendedSensorDeviceClass.CHANNEL),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Conductivity (µS/cm)
    (
        JaaleeSensorDeviceClass.CONDUCTIVITY,
        Units.CONDUCTIVITY,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.CONDUCTIVITY}_{Units.CONDUCTIVITY}",
        device_class=SensorDeviceClass.CONDUCTIVITY,
        native_unit_of_measurement=UnitOfConductivity.MICROSIEMENS_PER_CM,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Count (-)
    (JaaleeSensorDeviceClass.COUNT, None): SensorEntityDescription(
        key=str(JaaleeSensorDeviceClass.COUNT),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # CO2 (parts per million)
    (
        JaaleeSensorDeviceClass.CO2,
        Units.CONCENTRATION_PARTS_PER_MILLION,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.CO2}_{Units.CONCENTRATION_PARTS_PER_MILLION}",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Current (Ampere)
    (
        JaaleeSensorDeviceClass.CURRENT,
        Units.ELECTRIC_CURRENT_AMPERE,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.CURRENT}_{Units.ELECTRIC_CURRENT_AMPERE}",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Dew Point (°C)
    (JaaleeSensorDeviceClass.DEW_POINT, Units.TEMP_CELSIUS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.DEW_POINT}_{Units.TEMP_CELSIUS}",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Directions (°)
    (JaaleeExtendedSensorDeviceClass.DIRECTION, Units.DEGREE): SensorEntityDescription(
        key=f"{JaaleeExtendedSensorDeviceClass.DIRECTION}_{Units.DEGREE}",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Distance (mm)
    (
        JaaleeSensorDeviceClass.DISTANCE,
        Units.LENGTH_MILLIMETERS,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.DISTANCE}_{Units.LENGTH_MILLIMETERS}",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Distance (m)
    (JaaleeSensorDeviceClass.DISTANCE, Units.LENGTH_METERS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.DISTANCE}_{Units.LENGTH_METERS}",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Duration (seconds)
    (JaaleeSensorDeviceClass.DURATION, Units.TIME_SECONDS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.DURATION}_{Units.TIME_SECONDS}",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Energy (kWh)
    (
        JaaleeSensorDeviceClass.ENERGY,
        Units.ENERGY_KILO_WATT_HOUR,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.ENERGY}_{Units.ENERGY_KILO_WATT_HOUR}",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
    ),
    # Gas (m3)
    (
        JaaleeSensorDeviceClass.GAS,
        Units.VOLUME_CUBIC_METERS,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.GAS}_{Units.VOLUME_CUBIC_METERS}",
        device_class=SensorDeviceClass.GAS,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.TOTAL,
    ),
    # Gyroscope (°/s)
    (
        JaaleeSensorDeviceClass.GYROSCOPE,
        Units.GYROSCOPE_DEGREES_PER_SECOND,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.GYROSCOPE}_{Units.GYROSCOPE_DEGREES_PER_SECOND}",
        native_unit_of_measurement=Units.GYROSCOPE_DEGREES_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Humidity in (percent)
    (JaaleeSensorDeviceClass.HUMIDITY, Units.PERCENTAGE): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.HUMIDITY}_{Units.PERCENTAGE}",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Illuminance (lux)
    (JaaleeSensorDeviceClass.ILLUMINANCE, Units.LIGHT_LUX): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.ILLUMINANCE}_{Units.LIGHT_LUX}",
        device_class=SensorDeviceClass.ILLUMINANCE,
        native_unit_of_measurement=LIGHT_LUX,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Mass sensor (kg)
    (JaaleeSensorDeviceClass.MASS, Units.MASS_KILOGRAMS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.MASS}_{Units.MASS_KILOGRAMS}",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Mass sensor (lb)
    (JaaleeSensorDeviceClass.MASS, Units.MASS_POUNDS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.MASS}_{Units.MASS_POUNDS}",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.POUNDS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Moisture (percent)
    (JaaleeSensorDeviceClass.MOISTURE, Units.PERCENTAGE): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.MOISTURE}_{Units.PERCENTAGE}",
        device_class=SensorDeviceClass.MOISTURE,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Packet Id (-)
    (JaaleeSensorDeviceClass.PACKET_ID, None): SensorEntityDescription(
        key=str(JaaleeSensorDeviceClass.PACKET_ID),
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    # PM10 (µg/m3)
    (
        JaaleeSensorDeviceClass.PM10,
        Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.PM10}_{Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER}",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # PM2.5 (µg/m3)
    (
        JaaleeSensorDeviceClass.PM25,
        Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.PM25}_{Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER}",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Power (Watt)
    (JaaleeSensorDeviceClass.POWER, Units.POWER_WATT): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.POWER}_{Units.POWER_WATT}",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Precipitation (mm)
    (
        JaaleeExtendedSensorDeviceClass.PRECIPITATION,
        Units.LENGTH_MILLIMETERS,
    ): SensorEntityDescription(
        key=f"{JaaleeExtendedSensorDeviceClass.PRECIPITATION}_{Units.LENGTH_MILLIMETERS}",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Pressure (mbar)
    (JaaleeSensorDeviceClass.PRESSURE, Units.PRESSURE_MBAR): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.PRESSURE}_{Units.PRESSURE_MBAR}",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.MBAR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Raw (-)
    (JaaleeExtendedSensorDeviceClass.RAW, None): SensorEntityDescription(
        key=str(JaaleeExtendedSensorDeviceClass.RAW),
    ),
    # Rotation (°)
    (JaaleeSensorDeviceClass.ROTATION, Units.DEGREE): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.ROTATION}_{Units.DEGREE}",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Signal Strength (RSSI) (dB)
    (
        JaaleeSensorDeviceClass.SIGNAL_STRENGTH,
        Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.SIGNAL_STRENGTH}_{Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT}",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    # Speed (m/s)
    (
        JaaleeSensorDeviceClass.SPEED,
        Units.SPEED_METERS_PER_SECOND,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.SPEED}_{Units.SPEED_METERS_PER_SECOND}",
        device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Temperature (°C)
    (JaaleeSensorDeviceClass.TEMPERATURE, Units.TEMP_CELSIUS): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.TEMPERATURE}_{Units.TEMP_CELSIUS}",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Text (-)
    (JaaleeExtendedSensorDeviceClass.TEXT, None): SensorEntityDescription(
        key=str(JaaleeExtendedSensorDeviceClass.TEXT),
    ),
    # Timestamp (datetime object)
    (
        JaaleeSensorDeviceClass.TIMESTAMP,
        None,
    ): SensorEntityDescription(
        key=str(JaaleeSensorDeviceClass.TIMESTAMP),
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    # UV index (-)
    (
        JaaleeSensorDeviceClass.UV_INDEX,
        None,
    ): SensorEntityDescription(
        key=str(JaaleeSensorDeviceClass.UV_INDEX),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Volatile organic Compounds (VOC) (µg/m3)
    (
        JaaleeSensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS}_{Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER}",
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Voltage (volt)
    (
        JaaleeSensorDeviceClass.VOLTAGE,
        Units.ELECTRIC_POTENTIAL_VOLT,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.VOLTAGE}_{Units.ELECTRIC_POTENTIAL_VOLT}",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Volume (L)
    (
        JaaleeSensorDeviceClass.VOLUME,
        Units.VOLUME_LITERS,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.VOLUME}_{Units.VOLUME_LITERS}",
        device_class=SensorDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        state_class=SensorStateClass.TOTAL,
    ),
    # Volume (mL)
    (
        JaaleeSensorDeviceClass.VOLUME,
        Units.VOLUME_MILLILITERS,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.VOLUME}_{Units.VOLUME_MILLILITERS}",
        device_class=SensorDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.MILLILITERS,
        state_class=SensorStateClass.TOTAL,
    ),
    # Volume Flow Rate (m3/hour)
    (
        JaaleeSensorDeviceClass.VOLUME_FLOW_RATE,
        Units.VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.VOLUME_FLOW_RATE}_{Units.VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR}",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Volume Storage (L)
    (
        JaaleeExtendedSensorDeviceClass.VOLUME_STORAGE,
        Units.VOLUME_LITERS,
    ): SensorEntityDescription(
        key=f"{JaaleeExtendedSensorDeviceClass.VOLUME_STORAGE}_{Units.VOLUME_LITERS}",
        device_class=SensorDeviceClass.VOLUME_STORAGE,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Water (L)
    (
        JaaleeSensorDeviceClass.WATER,
        Units.VOLUME_LITERS,
    ): SensorEntityDescription(
        key=f"{JaaleeSensorDeviceClass.WATER}_{Units.VOLUME_LITERS}",
        device_class=SensorDeviceClass.WATER,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        state_class=SensorStateClass.TOTAL,
    ),
}

def hass_device_info(sensor_device_info):
    device_info = sensor_device_info_to_hass_device_info(sensor_device_info)
    if sensor_device_info.sw_version is not None:
        device_info[ATTR_SW_VERSION] = sensor_device_info.sw_version
    if sensor_device_info.hw_version is not None:
        device_info[ATTR_HW_VERSION] = sensor_device_info.hw_version
    return device_info
    
def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[float | None]:
    """Convert a sensor update to a bluetooth data update."""
    return PassiveBluetoothDataUpdate(
        devices={
            device_id: hass_device_info(device_info)
            for device_id, device_info in sensor_update.devices.items()
        },
        entity_descriptions={
            device_key_to_bluetooth_entity_key(device_key): SENSOR_DESCRIPTIONS[
                (description.device_class, description.native_unit_of_measurement)
            ]
            for device_key, description in sensor_update.entity_descriptions.items()
            if description.device_class
        },
        entity_data={
            device_key_to_bluetooth_entity_key(device_key): cast(
                float | None, sensor_values.native_value
            )
            for device_key, sensor_values in sensor_update.entity_values.items()
        },
        entity_names={
            device_key_to_bluetooth_entity_key(device_key): sensor_values.name
            for device_key, sensor_values in sensor_update.entity_values.items()
        },
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: JaaleeConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Jaalee BLE sensors."""
    coordinator = entry.runtime_data
    processor = JaaleePassiveBluetoothDataProcessor(
        sensor_update_to_bluetooth_data_update
    )
    entry.async_on_unload(
        processor.async_add_entities_listener(
            JaaleeBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(
        coordinator.async_register_processor(processor, SensorEntityDescription)
    )


class JaaleeBluetoothSensorEntity(
    PassiveBluetoothProcessorEntity[JaaleePassiveBluetoothDataProcessor[float | None]],
    SensorEntity,
):
    """Representation of a Jaalee BLE sensor."""

    @property
    def native_value(self) -> int | float | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available
