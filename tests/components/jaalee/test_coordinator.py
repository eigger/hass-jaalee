"""Exercise the production passive coordinator through a loaded HA entry."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import deliver_advertisement, make_service_info


async def test_coordinator_processes_advertisement_and_updates_entities(
    hass: HomeAssistant,
    loaded_entry: MockConfigEntry,
) -> None:
    """Test updating sensor values on subsequent advertisements."""
    # (0 + 45) / 175 * 65535 = 16852 (0x41D4) -> 0.0°C
    # (60 / 100) * 65535 = 39321 (0x9999) -> 60.0%
    # battery: 0x50 -> 80%
    data = bytes(16) + b"\xf5\x25\x41\xd4\x99\x99\x00\x50"
    info = make_service_info(data=data)
    await deliver_advertisement(hass, loaded_entry, info)

    assert loaded_entry.runtime_data.device_data.last_service_info is info

    states = hass.states.async_all()
    temp_state = next((s for s in states if "temperature" in s.entity_id), None)
    hum_state = next((s for s in states if "humidity" in s.entity_id), None)
    batt_state = next((s for s in states if "battery" in s.entity_id), None)

    assert temp_state is not None
    assert temp_state.state == "0.0"

    assert hum_state is not None
    assert hum_state.state == "60.0"

    assert batt_state is not None
    assert batt_state.state == "80"
