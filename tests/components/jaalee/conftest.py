"""Fixtures and test helpers for Jaalee Bluetooth integration."""

from __future__ import annotations

from time import monotonic

import pytest
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from habluetooth import get_manager
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.jaalee.const import DOMAIN

ADDRESS = "AA:BB:CC:DD:EE:FF"
DEFAULT_NAME = "JHT EEFF"
DEVICE_UUID = "0000f525-0000-1000-8000-00805f9b34fb"

# 24-byte payload:
# 16-byte UUID prefix + 0xF525 (2 bytes) + temp 0x6666 (25.0°C) + hum 0x8000 (50.0%) + 0x00 + battery 0x64 (100%)
VALID_JAALEE_DATA = bytes(16) + b"\xf5\x25\x66\x66\x80\x00\x00\x64"


def _make_ble_device(address: str, name: str, rssi: int = -55) -> BLEDevice:
    return BLEDevice(address, name, details={})


def make_advertisement_data(
    data: bytes = VALID_JAALEE_DATA,
    name: str = DEFAULT_NAME,
    service_uuids: list[str] | None = None,
    rssi: int = -55,
) -> AdvertisementData:
    if service_uuids is None:
        service_uuids = [DEVICE_UUID]
    return AdvertisementData(
        local_name=name,
        manufacturer_data={76: data},
        service_data={},
        service_uuids=service_uuids,
        tx_power=None,
        rssi=rssi,
        platform_data=(),
    )


def make_service_info(
    address: str = ADDRESS,
    name: str = DEFAULT_NAME,
    data: bytes = VALID_JAALEE_DATA,
    service_uuids: list[str] | None = None,
    rssi: int = -55,
) -> BluetoothServiceInfoBleak:
    device = _make_ble_device(address, name, rssi=rssi)
    adv = make_advertisement_data(
        data=data,
        name=name,
        service_uuids=service_uuids,
        rssi=rssi,
    )
    return BluetoothServiceInfoBleak.from_scan(
        "00:00:00:00:00:01",
        device,
        adv,
        monotonic(),
        True,
    )


async def deliver_advertisement(
    hass: HomeAssistant,
    entry: MockConfigEntry,
    info: BluetoothServiceInfoBleak,
) -> None:
    """Deliver an advertisement to the coordinator."""
    from homeassistant.components.bluetooth import BluetoothChange

    coordinator = entry.runtime_data
    coordinator._async_handle_bluetooth_event(info, BluetoothChange.ADVERTISEMENT)
    await hass.async_block_till_done()


@pytest.fixture
async def advertisement(
    hass: HomeAssistant,
    enable_bluetooth: None,
) -> BluetoothServiceInfoBleak:
    """Deliver a Jaalee BLE advertisement to the Bluetooth manager."""
    info = make_service_info()
    get_manager().scanner_adv_received(info)
    await hass.async_block_till_done()
    return info


@pytest.fixture
def entry(hass: HomeAssistant) -> MockConfigEntry:
    """Create a mock Jaalee config entry."""
    config = MockConfigEntry(
        domain=DOMAIN,
        unique_id=ADDRESS,
        title=DEFAULT_NAME,
        data={},
    )
    config.add_to_hass(hass)
    return config


@pytest.fixture
async def loaded_entry(
    hass: HomeAssistant,
    entry: MockConfigEntry,
    advertisement: BluetoothServiceInfoBleak,
) -> MockConfigEntry:
    """Set up the mock entry and wait for completion."""
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    fresh_info = make_service_info()
    from homeassistant.components.bluetooth import BluetoothChange

    coordinator = entry.runtime_data
    coordinator._async_handle_bluetooth_event(fresh_info, BluetoothChange.ADVERTISEMENT)
    await hass.async_block_till_done()
    return entry
