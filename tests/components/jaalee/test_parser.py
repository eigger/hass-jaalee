"""Unit tests for Jaalee BLE advertisement parser."""

from __future__ import annotations

from custom_components.jaalee.jaalee_ble.parser import (
    JaaleeBluetoothDeviceData,
    to_mac,
)

from .conftest import (
    DEFAULT_NAME,
    VALID_JAALEE_DATA,
    make_service_info,
)


def test_to_mac() -> None:
    """Test MAC address formatter."""
    raw = bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])
    assert to_mac(raw) == "AA:BB:CC:DD:EE:FF"


def test_parser_valid_advertisement() -> None:
    """Test parsing a valid Jaalee BLE advertisement."""
    info = make_service_info()
    parser = JaaleeBluetoothDeviceData()

    assert parser.supported(info) is True
    update = parser.update(info)

    assert parser.title == DEFAULT_NAME
    assert parser.get_device_name() == f"Jaalee {DEFAULT_NAME}"
    assert parser._device_id_to_type.get(None) == "Temperature/Humidity sensor"
    assert parser.last_service_info is info

    # Verify parsed values:
    # temp: 0x6666 = 26214 -> (26214 / 65535.0) * 175 - 45 = 25.0 °C
    # hum: 0x8000 = 32768 -> (32768 / 65535.0) * 100 = 50.0 %
    # battery: 0x64 = 100 %
    values = {k.key: v.native_value for k, v in update.entity_values.items()}
    assert values["temperature"] == 25.0
    assert values["humidity"] == 50.0
    assert values["battery"] == 100


def test_parser_invalid_length() -> None:
    """Test payload length other than 24 bytes is rejected."""
    short_data = bytes(16) + b"\xf5\x25\x66\x66\x80\x00\x00"  # 23 bytes
    info = make_service_info(data=short_data)
    parser = JaaleeBluetoothDeviceData()

    update = parser.update(info)
    assert len(update.entity_values) == 0
    assert parser.last_service_info is None


def test_parser_invalid_device_id() -> None:
    """Test payload with device ID other than 0xF525 is rejected."""
    wrong_device_data = bytes(16) + b"\x12\x34\x66\x66\x80\x00\x00\x64"  # device 0x1234
    info = make_service_info(data=wrong_device_data)
    parser = JaaleeBluetoothDeviceData()

    update = parser.update(info)
    assert len(update.entity_values) == 0
    assert parser.last_service_info is None


def test_parser_missing_manufacturer_id_76() -> None:
    """Test advertisement without Apple/Jaalee manufacturer ID 76 is ignored."""
    info = make_service_info()
    info.manufacturer_data = {100: VALID_JAALEE_DATA}
    parser = JaaleeBluetoothDeviceData()

    update = parser.update(info)
    assert len(update.entity_values) == 0
    assert parser.last_service_info is None


def test_parser_empty_service_uuids() -> None:
    """Test advertisement without service UUIDs does not parse."""
    info = make_service_info(service_uuids=[])
    parser = JaaleeBluetoothDeviceData()

    update = parser.update(info)
    assert len(update.entity_values) == 0
    assert parser.last_service_info is None


def test_parser_temperature_calculation() -> None:
    """Test precise temperature and humidity conversion math."""
    # (0 + 45) / 175 * 65535 = 16851.85 -> 16852 (0x41D4) -> 0.0°C
    # (60 / 100) * 65535 = 39321 (0x9999) -> 60.0%
    data = bytes(16) + b"\xf5\x25\x41\xd4\x99\x99\x00\x50"  # 80% battery
    info = make_service_info(data=data)
    parser = JaaleeBluetoothDeviceData()

    update = parser.update(info)
    values = {k.key: v.native_value for k, v in update.entity_values.items()}
    assert values["temperature"] == 0.0
    assert values["humidity"] == 60.0
    assert values["battery"] == 80
