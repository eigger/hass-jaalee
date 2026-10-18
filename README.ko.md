# Home Assistant용 Jaalee BLE 통합구성요소

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-jaalee?style=flat)](https://github.com/eigger/hass-jaalee/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#설치)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.1.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-jaalee/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-jaalee/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-jaalee/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-jaalee?style=flat)](LICENSE)
[![Analytics reporting installs](https://img.shields.io/badge/dynamic/json?style=flat&color=41BDF5&label=Usage&query=%24.jaalee.total&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json)](https://analytics.home-assistant.io/)
<!-- hass-standards:badges:end -->

[English](README.md) | **한국어**

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

1. Home Assistant에서 HACS 메뉴로 이동합니다.
2. **통합구성요소** > 우측 상단 점 3개 메뉴 > **사용자 지정 저장소**를 엽니다.
3. `https://github.com/eigger/hass-jaalee`를 입력하고 범주로 **통합구성요소**를 선택합니다.
4. **다운로드**를 클릭한 후 Home Assistant를 다시 시작합니다.

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

## 지원

- 버그 보고: [GitHub Issues](https://github.com/eigger/hass-jaalee/issues)
- 질문 및 제안: [GitHub Discussions](https://github.com/eigger/hass-jaalee/discussions)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
