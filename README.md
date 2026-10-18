# Jaalee BLE Integration for Home Assistant

<!-- hass-standards:badges:start -->
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat-square)](#installation)
[![Release](https://img.shields.io/github/v/release/eigger/hass-jaalee?style=flat-square)](https://github.com/eigger/hass-jaalee/releases)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.1.0-41BDF5?style=flat-square)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/tests.yml?branch=master&style=flat-square&label=Tests)](https://github.com/eigger/hass-jaalee/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/validate.yml?branch=master&style=flat-square&label=Validate)](https://github.com/eigger/hass-jaalee/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-jaalee?style=flat-square)](LICENSE)
[![Analytics reporting installs](https://img.shields.io/badge/dynamic/json?style=flat-square&color=41BDF5&label=Usage&query=%24.jaalee.total&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json)](https://analytics.home-assistant.io/)
<!-- hass-standards:badges:end -->

**English** | [한국어](README.ko.md)

Home Assistant custom component for Jaalee Bluetooth Low Energy (BLE) temperature and humidity sensors.

## Supported devices

- **Jaalee JHT**: Temperature, humidity, and battery sensor beacon.

For a remote Bluetooth connection, follow the [Bluetooth proxy setup guide](https://github.com/eigger/hass-repo-standards/blob/main/docs/bluetooth.md).
See [docs/user-guide.md](docs/user-guide.md) and [docs/troubleshooting.md](docs/troubleshooting.md) for device-specific instructions.

## Requirements

- Home Assistant 2025.1.0 or newer
- Working Bluetooth adapter or ESPHome Bluetooth proxy
- Jaalee BLE beacon advertising nearby (Manufacturer ID 76 / 0x004C, service UUID 0xF525)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant.
2. Go to **Integrations** > Three dots menu (top right) > **Custom repositories**.
3. Add `https://github.com/eigger/hass-jaalee` with category **Integration**.
4. Click **Download**, then restart Home Assistant.

### Manual Installation

1. Copy the `custom_components/jaalee` folder into your Home Assistant `<config>/custom_components/` directory.
2. Restart Home Assistant.

## Configuration

Jaalee sensors are automatically discovered via Bluetooth advertisements:
1. In Home Assistant, go to **Settings** > **Devices & services**.
2. If your Jaalee beacon is broadcasting nearby, click **Configure** on the discovered Jaalee card.
3. If not discovered automatically, click **Add Integration**, search for **Jaalee**, and select your device from the list.

## Documentation

- [User Guide](docs/user-guide.md) ([한국어](docs/ko/user-guide.md))
- [Troubleshooting](docs/troubleshooting.md) ([한국어](docs/ko/troubleshooting.md))
- [Development](docs/development.md)

## Support

- Issues: [GitHub Issues](https://github.com/eigger/hass-jaalee/issues)
- Discussions: [GitHub Discussions](https://github.com/eigger/hass-jaalee/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
