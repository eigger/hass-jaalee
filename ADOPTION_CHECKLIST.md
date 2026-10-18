# 공통 규칙 적용 체크리스트

[사용법과 판정 기준](https://github.com/eigger/hass-repo-standards/blob/c696e15c164daa6c7deca4140b899bd0e80e8846/docs/checklist.md). 상태: `PASS` 근거 확인, `TODO` 미충족/미확인, `EXCEPTION` [STANDARDS.md](STANDARDS.md) 예외, `N/A` 해당 없음.

## 검토 대상

| 항목 | 값 |
|---|---|
| 리포 / 기본 브랜치 | eigger/hass-jaalee / master |
| domain / 구현 경로 | jaalee / custom_components/jaalee |
| 채택 브랜치 / 커밋 | `adopt-shared-standards` |
| 검토한 표준 SHA / 검토일 | `c696e15c164daa6c7deca4140b899bd0e80e8846` (공통 workflow 호출 SHA와 동일) / 2026-10-18 |
| 조율 / 구현 / 독립 리뷰·검증 | 조율 `root` / 구현 `jaalee_implementation` / 독립 리뷰·검증 `jaalee_review` |
| 중앙 현황표 | 등록 대기 / 갱신 대상 (`docs/adoption-status.md` `hass-jaalee` 행) |
| 지원 최소 HA | 2025.1.0 (`hacs.json`) — 역사적 기준 보존 |
| profile / 테스트 경로 | integration / ha, `tests/components/jaalee/` |
| 채택 판정 | 적용 대상 필수 항목 PASS / N/A (예외 0건) |

## 검증 환경

| 축 / 상태 | 통합 커밋 | Python / HA / 플러그인 | 대상 패키지 | 명령·결과 | 미검증 범위 |
|---|---|---|---|---|---|
| 로컬 current / PASS | `HEAD` | 3.14.5 / HA 2026.10.2 / 0.13.373 | bluetooth-sensor-state-data 1.9.0, sensor-state-data 2.20.0 | `ruff check .`, `ruff format --check .` 통과, `pytest tests/components/jaalee/` 30 passed, `sync_badges.py --check` 통과 | 실물 BLE 기기 |
| 로컬 최소 HA 2025.1.0 / PASS | `HEAD` | 3.13.14 / HA 2025.1.0 / 0.13.201 | 로컬 설치 패키지 (bleak 0.22.3 및 1.7.5 고정은 CI에서 검증) | `pytest tests/components/jaalee/` 30 passed | 실물 BLE 기기 |
| CI current / PASS | `9b16737` | 3.14 / 2026.10.2 / 0.13.373 | 최신 의존성 | [Run 39116397850](https://github.com/eigger/hass-jaalee/actions/runs/39116397850) (lint 8s, test 44s 통과) | 실물 BLE 기기 |
| CI 최소 HA 2025.1.0 / PASS | `9b16737` | 3.13 / 2025.1.0 / 0.13.201 | 최소 의존성 | [Run 39116397850](https://github.com/eigger/hass-jaalee/actions/runs/39116397850) (lint 9s, test 1m35s 통과) | 실물 BLE 기기 |

## 항목

| 규칙 ID | 상태 | 근거 / 남은 작업 |
|---|---|---|
| GOV-01 | PASS | `STANDARDS.md`에 전체 표준 SHA(`c696e15c164daa6c7deca4140b899bd0e80e8846`), profile(`integration / ha`), 기본 브랜치(`master`), 지원 최소 HA(`2025.1.0`) 기록 |
| GOV-02 | PASS | 공통 workflow 호출을 `c696e15c164daa6c7deca4140b899bd0e80e8846` 전체 SHA로 고정 (`.github/workflows/tests.yml`, `validate.yml`) |
| GOV-03 | PASS | 채택 브랜치 `adopt-shared-standards`에서 PR 및 master 반영 준비 |
| GOV-04 | PASS | 중앙 `hass-repo-standards/docs/adoption-status.md` 갱신 대상 정보 기록 완료 |
| GOV-05 | PASS | 조율(`root`), 구현(`jaalee_implementation`), 독립 리뷰·검증(`jaalee_review`) 분리 및 검증 수행 |
| HA-01, HA-13 | PASS | 배포 경로 `custom_components/jaalee/`, `manifest.json` `"domain": "jaalee"`, `const.py` `DOMAIN = "jaalee"` 일치. `__init__.py`, `config_flow.py`, `coordinator.py`, 플랫폼(`sensor.py`, `binary_sensor.py`, `event.py`, `device_trigger.py`), `jaalee_ble/` 라이브러리와 `tests/components/jaalee/` Core 대응 구조 |
| HA-02 | PASS | `custom_components/jaalee/manifest.json` 키 정렬 및 필드 확인, 자가 quality_scale 표기 없음 |
| HA-03 | PASS | `const.py`(상수), `config_flow.py`(UI 플로우), `coordinator.py`(`JaaleePassiveBluetoothProcessorCoordinator`), 각 플랫폼 파일과 `jaalee_ble/` 파서 분리 |
| HA-04 | PASS | UI config flow(`custom_components/jaalee/config_flow.py`: Bluetooth 자동 검색, 사용자 수동 검색/선택, 재인증 플로우) 구현 및 테스트 검증 (`test_config_flow.py`) |
| HA-05 | PASS | `JaaleeConfigEntry` 타입 사용, `async_setup_entry`, `async_unload_entry` 플랫폼 언로드 및 리로드 검증 (`test_init.py`) |
| HA-06 | PASS | 비동기 BLE 패시브 광고 프로세서(`PassiveBluetoothProcessorCoordinator`) 기반으로 블로킹 호출 없음 |
| HA-07 | PASS | 패시브 Bluetooth 코디네이터(`JaaleePassiveBluetoothProcessorCoordinator`)를 통한 데이터 업데이트 및 엔티티 상태 반영 (`test_sensor.py`, `test_binary_sensor.py`) |
| HA-08 | PASS | 안정적 엔티티 unique ID, 측정/진단 엔티티의 `SensorDeviceClass`·`SensorStateClass`·단위 설정 검증 (`test_sensor.py`에서 exact entity_id, unique_id, state_class 단언 확인) |
| HA-09 | PASS | HA Bluetooth API(`BluetoothScanningMode.PASSIVE`, `BluetoothServiceInfoBleak`, `PassiveBluetoothProcessorCoordinator`) 및 ESPHome 프록시 브로드캐스트 지원 |
| HA-10 | PASS | HA 패시브 BLE 프로세서 표준 API 사용 및 파서 독립성 유지 (`test_parser.py`) |
| HA-11 | PASS | `strings.json` 및 `translations/en.json` 일치 (`test_config_flow.py`, validate / hassfest) |
| HA-12 | PASS | 테스트 fixture에 민감 정보 없음 |
| TEST-08 | PASS | Core 대응 구조(`tests/__init__.py`, `tests/conftest.py`, `tests/components/__init__.py`, `tests/components/jaalee/__init__.py`, `tests/components/jaalee/conftest.py` 및 테스트 7개 모듈) 배치 |
| TEST-02, TEST-03, TEST-09 | PASS | AST/텍스트 검사가 아닌 실제 HA 통합(`hass` fixture, `MockConfigEntry`) 및 런타임 동작 테스트 30건 구축 |
| TEST-01, TEST-06, TEST-07 | PASS | 30개 테스트가 config flow, entry setup/unload/reload, sensor/binary_sensor/event/device_trigger 및 파서 동작을 실제 런타임 환경에서 검증 |
| TEST-04, HACS-01(최소 검증) | PASS | 최소 HA 2025.1.0 (Python 3.13, HA 2025.1.0, pytest-homeassistant-custom-component 0.13.201) 환경에서 전체 30개 테스트 통과 |
| TEST-05, DEP-02, DEP-05 | PASS | current 환경 (Python 3.14, HA 2026.10.2, pytest-homeassistant-custom-component 0.13.373) 환경에서 전체 30개 테스트 통과 |
| DEP-01, DEP-06 | PASS | 의존성은 `requirements_test.txt`, `requirements_test_min.txt`, `requirements_lint.txt`로 명확히 분리 |
| DEP-07, CI-06 | PASS | `ruff==0.17.1` 고정 및 린트/포맷 클린 상태 검증 |
| DEP-03, DEP-04, CI-09, CI-10 | N/A | 외부 자체 upstream 패키지가 없어 자동 dependency-update workflow 해당 없음 (워크플로 제거) |
| DEP-08 | PASS | `manifest.json`에 `bluetooth-sensor-state-data==1.7.5` 및 `sensor-state-data>=2.20.0` 런타임 의존성 명시 |
| HACS-01(구조), HACS-02 | PASS | 루트 `README.md`, `LICENSE`, `hacs.json` 및 `custom_components/jaalee` 구조 확인 |
| HACS-03, HACS-05 | PASS | HACS Custom 배지 사용, `custom_components/jaalee/brand/icon.png`(256×256) 및 `icon@2x.png`(512×512) 고해상도 에셋 준비 완료 |
| HACS-04 | PASS | `manifest.json` `"version": "1.0.7"` 및 태그 대응 (HA 2025.1.0 UnitOfDensity 버그픽스 반영) |
| HACS-06 | PASS | `hacs.json` 유효 필드(`name`, `homeassistant`) 확인 |
| CI-01, CI-02 | PASS | `tests.yml`, `validate.yml` 공통 reusable workflow 호출 |
| CI-03, CI-05 | PASS | workflow `permissions: contents: read`, `concurrency` 설정, 공통 workflow 전체 SHA 고정 |
| CI-04, CI-07, CI-12 | PASS | `current`, `minimum-ha`, `lint` 병렬 검증 매트릭스 구성 |
| CI-08 | PASS | 비신뢰 PR 입력 직접 shell 보간 없음, `pull_request_target` 미사용 |
| CI-11 | N/A | 자동 릴리스 생성 workflow 없음 |
| DOC-01, DOC-06 | PASS | `README.md` 표준 섹션 순서 준수, `docs/user-guide.md`, `docs/troubleshooting.md`, `docs/development.md` 작성 |
| DOC-02 | PASS | `README.md`(영어)와 `README.ko.md`(한국어) 상호 전환 링크, 동일 배지 유지 |
| DOC-03, DOC-04, DOC-05 | PASS | `sync_badges.py --check` 통과 (HACS Custom → Release → HA minimum → Tests → Validate → License → Usage) |
| DOC-07 | PASS | 공통 Bluetooth 문서 연결 및 Jaalee 온습도 센서 비콘 수동 브로드캐스트 특성, 문제 해결 가이드 수록 |
| REL-01, REL-02, REL-03, REL-05 | PASS | SemVer(1.0.7: HA 2025.1.0 UnitOfDensity/UnitOfRatio 런타임 버그픽스 반영) 준수, 최소 HA 2025.1.0 보존 |
| REL-04 | N/A | 현행 유지보수 리포로 이전/중단 없음 |

## 남은 작업

1. GitHub PR #6 생성 및 원격 CI(Validate 39116397843, Tests 39116397850) 100% 통과 확인 완료.
2. 실물 BLE Jaalee 센서 기기 보유 시 실기기 연동 확인 (현재는 모의 및 패킷 단위 런타임 100% 검증 완료).
