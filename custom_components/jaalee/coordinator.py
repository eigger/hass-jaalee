"""The Jaalee Bluetooth integration."""

from collections.abc import Callable
from logging import Logger

from .jaalee_ble import JaaleeBluetoothDeviceData, SensorUpdate

from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataProcessor,
    PassiveBluetoothProcessorCoordinator,
)
from homeassistant.core import HomeAssistant

from .types import JaaleeConfigEntry


class JaaleePassiveBluetoothProcessorCoordinator(
    PassiveBluetoothProcessorCoordinator[SensorUpdate]
):
    """Define a Jaalee Bluetooth Passive Update Processor Coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: Logger,
        address: str,
        mode: BluetoothScanningMode,
        update_method: Callable[[BluetoothServiceInfoBleak], SensorUpdate],
        device_data: JaaleeBluetoothDeviceData,
        discovered_event_classes: set[str],
        entry: JaaleeConfigEntry,
        connectable: bool = False,
    ) -> None:
        """Initialize the Jaalee Bluetooth Passive Update Processor Coordinator."""
        super().__init__(hass, logger, address, mode, update_method, connectable)
        self.discovered_event_classes = discovered_event_classes
        self.device_data = device_data
        self.entry = entry


class JaaleePassiveBluetoothDataProcessor[_T](
    PassiveBluetoothDataProcessor[_T, SensorUpdate]
):
    """Define a Jaalee Bluetooth Passive Update Data Processor."""

    coordinator: JaaleePassiveBluetoothProcessorCoordinator
