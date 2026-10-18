"""Test Jaalee Bluetooth config flow."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.config_entries import SOURCE_BLUETOOTH, SOURCE_REAUTH, SOURCE_USER
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.jaalee.const import DOMAIN
from custom_components.jaalee.jaalee_ble.parser import JaaleeBluetoothDeviceData

from .conftest import ADDRESS, DEFAULT_NAME, make_service_info


async def test_bluetooth_discovery_flow(
    hass: HomeAssistant, advertisement: BluetoothServiceInfoBleak
) -> None:
    """Test discovering a Jaalee device over Bluetooth and confirming setup."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=advertisement,
    )
    if (
        result["type"] is FlowResultType.ABORT
        and result["reason"] == "already_in_progress"
    ):
        progress = hass.config_entries.flow.async_progress_by_handler(DOMAIN)
        assert len(progress) == 1
        result = await hass.config_entries.flow.async_configure(progress[0]["flow_id"])

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    with patch(
        "custom_components.jaalee.async_setup_entry", return_value=True
    ) as mock_setup:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == DEFAULT_NAME
    assert result2["result"].unique_id == ADDRESS
    assert len(mock_setup.mock_calls) == 1


async def test_bluetooth_discovery_already_configured(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
    advertisement: BluetoothServiceInfoBleak,
) -> None:
    """Test discovering an already configured device aborts."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=advertisement,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_bluetooth_discovery_not_supported(
    hass: HomeAssistant,
    enable_bluetooth: None,
) -> None:
    """Test discovering an unsupported Bluetooth device aborts."""
    unsupported_info = BluetoothServiceInfoBleak(
        name="UnknownDevice",
        address="99:88:77:66:55:44",
        rssi=-70,
        manufacturer_data={},
        service_data={},
        service_uuids=["00001234-0000-1000-8000-00805f9b34fb"],
        source="local",
        device=None,
        advertisement=None,
        connectable=True,
        time=0,
        tx_power=None,
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=unsupported_info,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "not_supported"


async def test_user_flow_select_device(
    hass: HomeAssistant,
    advertisement: BluetoothServiceInfoBleak,
) -> None:
    """Test user initiation discovers available devices for selection."""
    with patch(
        "custom_components.jaalee.config_flow.async_discovered_service_info",
        return_value=[advertisement],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "custom_components.jaalee.async_setup_entry", return_value=True
    ) as mock_setup:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={CONF_ADDRESS: ADDRESS},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["result"].unique_id == ADDRESS
    assert result2["title"] == DEFAULT_NAME
    assert len(mock_setup.mock_calls) == 1


async def test_user_flow_no_devices_found(
    hass: HomeAssistant, enable_bluetooth: None
) -> None:
    """Test user flow aborts when no BLE devices are discovered."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_user_flow_already_configured_device_ignored(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
    advertisement: BluetoothServiceInfoBleak,
) -> None:
    """Test user flow ignores already configured devices."""
    with patch(
        "custom_components.jaalee.config_flow.async_discovered_service_info",
        return_value=[advertisement],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_reauth_step(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Test reauth flow aborts with reauth_successful."""
    device = JaaleeBluetoothDeviceData()
    info = make_service_info()
    device.update(info)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_REAUTH, "entry_id": entry.entry_id},
        data={"device": device},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
