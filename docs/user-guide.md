# Jaalee User Guide

**English** | [한국어](ko/user-guide.md)

This guide describes how to configure and use Jaalee BLE sensors in Home Assistant.

## Overview

Jaalee devices (such as the JHT temperature and humidity sensor beacon) broadcast sensor readings periodically via BLE advertisements (Apple manufacturer ID `76` / `0x004C`, service UUID `0000f525-0000-1000-8000-00805f9b34fb`).

Because Jaalee sensors use passive BLE broadcasting:
- They do not maintain an active GATT connection, preserving long battery life (typically 1+ years on a CR2032 coin cell).
- Multiple Bluetooth adapters and ESPHome Bluetooth proxies can pick up the broadcast packets simultaneously.

## Entities Provided

When added to Home Assistant, the following entities are created:

| Entity | Domain | Description | Device Class |
|---|---|---|---|
| Temperature | `sensor` | Ambient temperature in °C or °F | `temperature` |
| Humidity | `sensor` | Relative humidity percentage (%) | `humidity` |
| Battery | `sensor` | Remaining battery percentage (%) | `battery` |
| Signal Strength | `sensor` | RSSI signal strength (disabled by default) | `signal_strength` |

## Discovery and Configuration

1. Ensure the Jaalee sensor has a fresh battery installed and is within range of your Home Assistant server or an ESPHome Bluetooth proxy.
2. In Home Assistant, go to **Settings** > **Devices & services**.
3. Under **Discovered**, locate your Jaalee device (e.g. `JHT <ID>`) and click **Configure**.
4. Confirm device addition to complete setup.

## Events and Device Triggers

If your Jaalee hardware supports button or dimmer events, they are dynamically registered under the `event` platform and available as Home Assistant device automation triggers.
