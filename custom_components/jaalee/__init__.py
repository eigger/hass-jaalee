"""The Jaalee Bluetooth integration."""

from __future__ import annotations

from functools import partial
import logging
from .jaalee_ble import JaaleeBluetoothDeviceData, SensorUpdate
from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.util.signal_type import SignalType

from .const import (
    CONF_DISCOVERED_EVENT_CLASSES,
    DOMAIN,
    JaaleeBleEvent,
)
from .coordinator import JaaleePassiveBluetoothProcessorCoordinator
from .types import JaaleeConfigEntry

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.EVENT, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

def process_service_info(
    hass: HomeAssistant,
    entry: JaaleeConfigEntry,
    device_registry: DeviceRegistry,
    service_info: BluetoothServiceInfoBleak,
) -> SensorUpdate:
    """Process a BluetoothServiceInfoBleak, running side effects and returning sensor data."""
    coordinator = entry.runtime_data
    data = coordinator.device_data
    update = data.update(service_info)

    return update


def format_event_dispatcher_name(
    address: str, event_class: str
) -> SignalType[JaaleeBleEvent]:
    """Format an event dispatcher name."""
    return SignalType(f"{DOMAIN}_event_{address}_{event_class}")


def format_discovered_event_class(address: str) -> SignalType[str, JaaleeBleEvent]:
    """Format a discovered event class."""
    return SignalType(f"{DOMAIN}_discovered_event_class_{address}")


async def async_setup_entry(hass: HomeAssistant, entry: JaaleeConfigEntry) -> bool:
    """Set up Jaalee Bluetooth from a config entry."""
    address = entry.unique_id
    assert address is not None

    data = JaaleeBluetoothDeviceData()

    device_registry = dr.async_get(hass)
    event_classes = set(entry.data.get(CONF_DISCOVERED_EVENT_CLASSES, ()))
    coordinator = JaaleePassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=partial(process_service_info, hass, entry, device_registry),
        device_data=data,
        discovered_event_classes=event_classes,
        connectable=True,
        entry=entry,
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())
    return True


async def async_unload_entry(hass: HomeAssistant, entry: JaaleeConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def get_entry_id_from_device(hass, device_id: str) -> str:
    device_reg = dr.async_get(hass)
    device_entry = device_reg.async_get(device_id)
    if not device_entry:
        raise ValueError(f"Unknown device_id: {device_id}")
    if not device_entry.config_entries:
        raise ValueError(f"No config entries for device {device_id}")

    _LOGGER.debug(f"{device_id} to {device_entry.config_entries}")
    try:
        entry_id = next(iter(device_entry.config_entries))
    except StopIteration:
        _LOGGER.error("%s None", device_id)
        return None

    return entry_id