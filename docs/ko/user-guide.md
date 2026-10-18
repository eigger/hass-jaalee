# Jaalee 사용자 가이드

[English](../user-guide.md) | **한국어**

이 문서는 Home Assistant에서 Jaalee BLE 센서를 설정하고 사용하는 방법을 설명합니다.

## 개요

Jaalee 기기(JHT 온습도 센서 비콘 등)는 BLE 브로드캐스트 광고(제조사 ID `76` / `0x004C`, 서비스 UUID `0000f525-0000-1000-8000-00805f9b34fb`)를 통해 주기적으로 센서 측정값을 전송합니다.

Jaalee 센서는 수동(Passive) BLE 광고 방식을 사용하므로:
- 상시 GATT 연결을 유지하지 않아 CR2032 코인 전지로 1년 이상 긴 배터리 수명을 유지합니다.
- 여러 Bluetooth 어댑터와 ESPHome Bluetooth 프록시가 동시에 브로드캐스트 패킷을 수신할 수 있습니다.

## 제공되는 엔티티

Home Assistant에 등록되면 다음 엔티티가 자동 생성됩니다:

| 엔티티 | 도메인 | 설명 | 기기 클래스 |
|---|---|---|---|
| 온도 (Temperature) | `sensor` | 주변 온도 (°C / °F) | `temperature` |
| 습도 (Humidity) | `sensor` | 상대 습도 (%) | `humidity` |
| 배터리 (Battery) | `sensor` | 배터리 잔량 (%) | `battery` |
| 신호 강도 (Signal Strength) | `sensor` | 수신 신호 강도 RSSI (기본 비활성화) | `signal_strength` |

## 기기 검색 및 설정

1. Jaalee 센서에 정상 배터리가 장착되어 있고 Home Assistant 서버 또는 ESPHome Bluetooth 프록시의 수신 범위 내에 있는지 확인합니다.
2. Home Assistant에서 **설정** > **기기 및 서비스**로 이동합니다.
3. **발견됨(Discovered)** 항목에서 Jaalee 기기(예: `JHT <ID>`)를 확인하고 **구성(Configure)**을 클릭합니다.
4. 기기 추가를 확인하여 설정을 완료합니다.

## 이벤트 및 기기 트리거

버튼이나 디머 기능이 포함된 Jaalee 기기 모델의 경우, 브로드캐스트된 이벤트가 `event` 플랫폼 엔티티 및 Home Assistant 자동화의 기기 트리거(Device Trigger)로 연동됩니다.
