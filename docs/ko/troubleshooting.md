# Jaalee 문제 해결

[English](../troubleshooting.md) | **한국어**

이 문서는 Home Assistant에서 Jaalee BLE 기기 사용 시 발생하는 문제에 대한 해결 절차를 제공합니다.

일반적인 Bluetooth 및 프록시 문제 해결은 공통 [Bluetooth 프록시 안내](https://github.com/eigger/hass-repo-standards/blob/main/docs/bluetooth.ko.md#troubleshooting)도 함께 참조하세요.

## 자주 발생하는 문제

### 1. 기기가 검색되지 않는 경우

- **배터리 확인**: CR2032 코인 전지의 잔량이 충분한지(2.8V 이상) 확인합니다. 방전된 배터리는 BLE 신호 송출을 멈추게 합니다.
- **거리 및 전파 간섭**: 센서를 Bluetooth 동글 또는 ESPHome Bluetooth 프록시 가까이로 옮겨보세요. 금속 차폐나 2.4GHz Wi-Fi 간섭으로 수신 반경이 좁아질 수 있습니다.
- **Home Assistant 블루투스 확인**: Home Assistant의 공식 `bluetooth` 통합구성요소가 정상 동작 중인지 확인하세요.

### 2. 센서 값이 '사용할 수 없음(Unavailable)' 상태이거나 갱신되지 않는 경우

- Jaalee 센서는 수 초 간격으로 패킷을 브로드캐스팅합니다. 오랜 시간 패킷을 수신하지 못하면 Home Assistant가 센서를 사용 불가로 표시합니다.
- Bluetooth 어댑터나 ESPHome 프록시의 연결 상태를 점검하세요.
- **설정** > **시스템** > **로그**에서 블루투스 관련 오류가 없는지 확인합니다.

### 3. 디버그 로그 활성화

문제 분석을 위해 디버그 로그가 필요한 경우:

1. `configuration.yaml`에 다음 설정을 추가합니다:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.jaalee: debug
   ```
2. Home Assistant를 다시 시작합니다.
3. 문제를 재현한 후 관련 로그를 확인합니다. 분석이 끝나면 디버그 로깅을 다시 비활성화하세요.
