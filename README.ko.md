<!-- hass-standards:header:start -->
# Jaalee BLE Integration for Home Assistant

Jaalee 저전력 블루투스(BLE) 온습도 센서를 위한 Home Assistant HACS 커스텀 통합구성요소입니다.

[English](README.md) | **한국어**

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-jaalee?style=flat)](https://github.com/eigger/hass-jaalee/releases)
[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5?style=flat)](#hacs-권장)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.1.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-jaalee/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-jaalee/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-jaalee?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-jaalee/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-jaalee/releases)
<!-- hass-standards:badges:end -->
<!-- hass-standards:header:end -->

Jaalee 저전력 블루투스(BLE) 온습도 센서를 위한 Home Assistant 커스텀 통합구성요소입니다.

## 지원 기기

- **Jaalee JHT**: 온도, 습도, 배터리 센서 비콘

원격 Bluetooth 연결은 [Bluetooth proxy 설정 안내](https://github.com/eigger/hass-repo-standards/blob/main/docs/bluetooth.ko.md)를 따르세요.
기기별 상세 안내와 문제 해결은 [docs/ko/user-guide.md](docs/ko/user-guide.md) 및 [docs/ko/troubleshooting.md](docs/ko/troubleshooting.md)를 확인하세요.

## 요구 사항

- Home Assistant 2025.1.0 이상
- 작동 중인 Bluetooth 어댑터 또는 ESPHome Bluetooth 프록시
- 주변에서 브로드캐스팅 중인 Jaalee BLE 기기 (제조사 ID 76 / 0x004C, 서비스 UUID 0xF525)

## 설치

### HACS (권장)

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-jaalee)
<!-- hass-standards:installation:end -->

1. Home Assistant에서 HACS를 엽니다.
2. **Jaalee**를 검색해 엽니다.
3. **다운로드**를 클릭한 후 Home Assistant를 다시 시작합니다.

### 수동 설치

1. `custom_components/jaalee` 디렉터리를 Home Assistant의 `<config>/custom_components/` 경로에 복사합니다.
2. Home Assistant를 다시 시작합니다.

## 설정

Jaalee 기기는 Bluetooth 브로드캐스트를 통해 자동으로 검색됩니다:
1. Home Assistant에서 **설정** > **기기 및 서비스**로 이동합니다.
2. 주변에 검색된 Jaalee 기기 카드가 표시되면 **구성**을 클릭합니다.
3. 자동 검색되지 않는 경우 **통합구성요소 추가**를 클릭하고 **Jaalee**를 검색하여 목록에서 기기를 선택합니다.

## 문서

- [사용자 가이드](docs/ko/user-guide.md) ([English](docs/user-guide.md))
- [문제 해결](docs/ko/troubleshooting.md) ([English](docs/troubleshooting.md))
- [개발 안내](docs/development.md)

<!-- hass-standards:support:start -->
## 지원

- [Issues](https://github.com/eigger/hass-jaalee/issues): 버그를 신고하거나 기능을 요청하세요.
- [Discussions](https://github.com/eigger/hass-jaalee/discussions): 질문하고 사용 경험을 공유하세요.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## 라이선스

[MIT License](LICENSE) 라이선스로 배포됩니다.
<!-- hass-standards:license:end -->
