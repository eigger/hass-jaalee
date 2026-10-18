"""Test the Jaalee integration manifest."""

from __future__ import annotations

import json
from pathlib import Path


def test_manifest() -> None:
    """Verify manifest.json metadata and schema conformance."""
    manifest_path = (
        Path(__file__).parents[3] / "custom_components" / "jaalee" / "manifest.json"
    )
    assert manifest_path.is_file()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["domain"] == "jaalee"
    assert manifest["name"] == "Jaalee"
    assert manifest["codeowners"] == ["@eigger"]
    assert manifest["config_flow"] is True
    assert manifest["iot_class"] == "local_push"
    assert manifest["version"] == "1.0.6"
    assert "bluetooth_adapters" in manifest["dependencies"]

    # Bluetooth advertisement matchers
    assert "bluetooth" in manifest
    assert len(manifest["bluetooth"]) >= 1
    matcher = manifest["bluetooth"][0]
    assert matcher["manufacturer_id"] == 76
    assert matcher["connectable"] is False
