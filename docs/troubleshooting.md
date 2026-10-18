# Jaalee Troubleshooting

**English** | [한국어](ko/troubleshooting.md)

This document provides troubleshooting steps for Jaalee BLE devices in Home Assistant.

For general Bluetooth and proxy troubleshooting, also refer to the shared [Bluetooth proxy user guide](https://github.com/eigger/hass-repo-standards/blob/main/docs/bluetooth.md#troubleshooting).

## Common Issues

### 1. Device Not Discovered

- **Battery Check**: Ensure the CR2032 coin cell has sufficient voltage (>= 2.8V). A dying battery may prevent BLE advertising.
- **Distance / Interference**: Move the sensor closer to your Bluetooth dongle or ESPHome Bluetooth proxy. Metal enclosures or 2.4 GHz Wi-Fi interference can reduce range.
- **Active Bluetooth Integration**: Verify that the official Home Assistant `bluetooth` integration is installed and running without errors.

### 2. Sensor Values Unavailable or Stale

- Jaalee sensors advertise periodically (typically every few seconds). If no packet is received for a prolonged period, Home Assistant marks the entities as unavailable.
- Check if your Bluetooth adapter or ESPHome proxy has disconnected or rebooted.
- Check Home Assistant system logs under **Settings** > **System** > **Logs** for Bluetooth or adapter warnings.

### 3. Enabling Debug Logging

To capture debug logs for Jaalee integration:

1. Add the following to your `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.jaalee: debug
   ```
2. Restart Home Assistant.
3. Reproduce the issue and collect the relevant log entries. Remember to remove or disable debug logging once finished.
