<!-- hass-standards:header:start -->
# Jaalee BLE Integration for Home Assistant

Home Assistant custom integration for Jaalee Bluetooth Low Energy (BLE) temperature and humidity sensors.

**English** | [한국어](README.ko.md)

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-jaalee?style=flat)](https://github.com/eigger/hass-jaalee/releases)
[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5?style=flat)](#hacs-recommended)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.1.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-jaalee/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-jaalee/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-jaalee?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-jaalee/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-jaalee/releases)
<!-- hass-standards:badges:end -->
<!-- hass-standards:header:end -->

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

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-jaalee)
<!-- hass-standards:installation:end -->

1. Open HACS in Home Assistant.
2. Search for **Jaalee** and open it.
3. Click **Download**, then restart Home Assistant.

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

<!-- hass-standards:support:start -->
## Support

- [Issues](https://github.com/eigger/hass-jaalee/issues): Report bugs or request features.
- [Discussions](https://github.com/eigger/hass-jaalee/discussions): Ask questions and share your experience.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## License

Released under the [MIT License](LICENSE).
<!-- hass-standards:license:end -->
