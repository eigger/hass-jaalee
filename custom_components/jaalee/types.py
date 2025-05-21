"""The Jaalee Bluetooth integration."""

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from .coordinator import JaaleePassiveBluetoothProcessorCoordinator

type JaaleeConfigEntry = ConfigEntry[JaaleePassiveBluetoothProcessorCoordinator]
