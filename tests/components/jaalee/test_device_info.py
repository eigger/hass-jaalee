"""DeviceInfo is built with keyword arguments only (TypedDict and dataclass)."""

from __future__ import annotations

import ast
from pathlib import Path

from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.jaalee.sensor import _device_info

PACKAGE = Path(__file__).parents[3] / "custom_components" / "jaalee"

# Deprecated since HA 2026.12 (removed 2027.12); ATTR_NAME is not deprecated.
DEPRECATED_CONSTANTS = {
    "ATTR_CONFIGURATION_URL",
    "ATTR_CONNECTIONS",
    "ATTR_DEFAULT_NAME",
    "ATTR_HW_VERSION",
    "ATTR_IDENTIFIERS",
    "ATTR_MANUFACTURER",
    "ATTR_MODEL",
    "ATTR_MODEL_ID",
    "ATTR_SERIAL_NUMBER",
    "ATTR_SUGGESTED_AREA",
    "ATTR_SW_VERSION",
    "ATTR_VIA_DEVICE",
}


def test_full_device_info_has_all_fields() -> None:
    assert _device_info("Tag", "Jaalee", "JHT", "1.0", "2.0") == DeviceInfo(
        name="Tag",
        manufacturer="Jaalee",
        model="JHT",
        sw_version="1.0",
        hw_version="2.0",
    )


def test_unset_values_are_omitted_not_none() -> None:
    assert _device_info("Tag", None, None, None, None) == DeviceInfo(name="Tag")
    assert _device_info(None, "Jaalee", None, "1.0", None) == DeviceInfo(
        manufacturer="Jaalee", sw_version="1.0"
    )
    assert _device_info(None, None, None, None, None) == DeviceInfo()


def test_device_info_is_cached() -> None:
    assert _device_info("Tag", "Jaalee", None, None, None) is _device_info(
        "Tag", "Jaalee", None, None, None
    )


def test_no_deprecated_device_info_constants_or_item_assignment() -> None:
    for path in PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module == "homeassistant.const"
            ):
                names = {alias.name for alias in node.names}
                assert not names & DEPRECATED_CONSTANTS, path
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.value, ast.Name)
                        and target.value.id in {"info", "device_info"}
                    ):
                        raise AssertionError(f"{path}:{node.lineno} item assignment")
