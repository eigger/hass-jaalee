from __future__ import annotations

import logging

from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfoBleak
from sensor_state_data import (
    SensorLibrary,
)

_LOGGER = logging.getLogger(__name__)

def to_mac(addr: bytes) -> str:
    """Return formatted MAC address."""
    return ":".join(f"{i:02X}" for i in addr)

class JaaleeBluetoothDeviceData(BluetoothData):
    """Data for BTHome Bluetooth devices."""

    def __init__(self) -> None:
        super().__init__()

        # The last service_info we saw that had a payload
        # We keep this to help in reauth flows where we want to reprocess and old
        # value with a new bindkey.
        self.last_service_info: BluetoothServiceInfoBleak | None = None


    def supported(self, data: BluetoothServiceInfoBleak) -> bool:
        if not super().supported(data):
            return False
        return True

    def _start_update(self, service_info: BluetoothServiceInfoBleak) -> None:
        """Update from BLE advertisement data."""
        #_LOGGER.info("Parsing Jaalee BLE advertisement data: %s", service_info)
        if 76 in service_info.manufacturer_data:
            #_LOGGER.info("BLE Info: %s", service_info)
            data = service_info.manufacturer_data[76]
            for uuid in service_info.service_uuids:
                #_LOGGER.info("Jaalee %s BLE UUID %s data: %s", service_info.name, uuid, data.hex())
                if self._parse_jaalee(service_info, data):
                    self.last_service_info = service_info
        return None

    def _parse_jaalee(
        self, service_info: BluetoothServiceInfo, data: bytes
    ) -> bool:
        """Parser for Jaalee sensors"""
        if len(data) != 24:
            return False
        
        device = (data[16] << 8) + data[17]
        if device != 0xF525:
            return False

        # determine the device type
        manufacturer = "Jaalee"
        bettery = data[23]
        temperature = (data[18] << 8) + data[19]
        humidity = (data[20] << 8) + data[21]
        
        multiplier = pow(10.0, 2)

        #http://sensor.jaalee.com/scan_api.html
        temperature = round(((temperature / 65535.0) * 175 - 45) * multiplier) / multiplier
        humidity = round(((humidity / 65535.0) * 100) * multiplier) / multiplier

        identifier = service_info.address.replace(":", "")[-8:]
        self.set_title(f"JHT {identifier}")
        self.set_device_name(f"{manufacturer} JHT {identifier}")
        self.set_device_type(f"Temperature/Humidity sensor")
        self.set_device_manufacturer(manufacturer)

        self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, round(bettery, 1))
        self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, round(temperature, 2))
        self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, round(humidity, 2))

        return True