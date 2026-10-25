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


## 2026-10-23 HACS ZIP and Downloads (scoped)

- Target base: `080e4c63d2524e5fc2ef03537aaf49cc4d78a1f6`; reviewed release central: `fd4162c0b93fbe8e109f99c787773ae09ba157e1`.
- Scope: HACS-04/CI-11 release ZIP and DOC-03/05 Downloads replacing Analytics Usage. No release is created during this update.
- Local scoped validation: PASS — canonical badge check, no Analytics Usage, release metadata/caller contract, actionlint 1.7.12, native git diff --check, unchanged tracked integration/manifest/dependencies/tests.
- Actual archive build: PASS at `d58d1184fb99ca2ba5293e222fad86161d2e1384`; `jaalee.zip`, 21 files, SHA256 `31dc74da9d475ea2466579f9cfc56a3622aaf545ada734ff1fffaab153a3401d`. All archive members matched checkout bytes; manifest.json and __init__.py are at ZIP root. Final documentation-only follow-up preserves this integration tree. Windows Python 3.14.6; validation WSL Python 3.14.4/PyYAML 6.0.3/packaging 26.0.
- Full central integration checker: FAIL (pre-existing or unadopted contracts outside this scoped update; not treated as PASS). Findings:

```text
DOC-01 README.md: Exactly one ordered header marker pair required
DOC-01 README.ko.md: Exactly one ordered header marker pair required
HA-02 custom_components/jaalee/manifest.json: categories requires 1–3 actual product categories (HA-02 project policy)
HA-11 custom_components/jaalee/translations/ko.json: Required contract file is missing
TEST-08 tests/components/jaalee/test_coordinator.py: Required contract file is missing
HA-13 custom_components/__init__.py: Required contract file is missing
HA-11 custom_components/jaalee/translations/ko.json: [Errno 2] No such file or directory: '/mnt/d/Source/Github/.hacs-custom-zip/hass-jaalee/custom_components/jaalee/translations/ko.json'
GOV-02 .github/workflows/tests.yml: standards-ref must equal the reviewed reusable workflow SHA
GOV-02 .github/workflows/tests.yml: standards-ref must equal the reviewed reusable workflow SHA
TEST-08 tests/__init__.py: must exist and be empty
TEST-08 tests/components/__init__.py: must exist and be empty
TEST-08 tests/components/jaalee/__init__.py: must exist and be empty
TEST-03 tests/conftest.py: must match the central template exactly
TEST-08 tests/components/jaalee/conftest.py: Exactly one ordered domain-fixtures marker pair required
CI-02 .github/workflows/tests.yml: name and events must match the central template (actual default branch)
CI-02 .github/workflows/validate.yml: name and events must match the central template (actual default branch)
CI-01 .github/workflows/validate.yml: central standards composite action pinned to full SHA required
```

- Existing CI workflows are preserved, except hass-kocom-smarthome where matching reviewed central references are synchronized. Existing support minimum and prior exceptions remain.
- Independent review and remote CI: tracked in this branch's pull request; merge requires resolved actionable findings and successful applicable checks. No real release upload, device or new real HA runtime validation is claimed by these local packaging checks.


## 2026-10-25 중앙 검사기 부분 갱신 검증

- 검토한 중앙 SHA: `1863343638014adb8a4001afc8fddc1a27dc500f`; 적용 시작 커밋: `03b0d9215e8619c090825a7e85fe1f2745774331`.
- 범위: 중앙 pin·standards-ref·검토 기준 기록 정합화 및 누락 standards job 추가. HA 구현·요구 버전은 유지합니다.
- 로컬: Python 3.14.5 / PyYAML 6.0.3, `python scripts/check_integration.py <target>` (검토한 중앙 source에서 실행): FAIL — 아래 미충족 항목을 확인했으며 성공으로 표시하지 않음.
- actionlint: PASS. PR CI·독립 리뷰 결과는 PR 링크와 check 결과를 확인합니다. 이 로컬 결과만으로 전체 채택 완료를 주장하지 않습니다.
- 수정 전에도 최신 검사기로 검사 시 17개 진단이 있었습니다. 이번 검사기가 드러내는 잔여 항목은 다음과 같습니다. 승인 예외나 실패 무시를 추가하지 않았습니다.

```text
DOC-01 README.md: Exactly one ordered header marker pair required
DOC-01 README.ko.md: Exactly one ordered header marker pair required
HA-02 custom_components/jaalee/manifest.json: categories requires 1–3 actual product categories (HA-02 project policy)
HA-11 custom_components/jaalee/translations/ko.json: Required contract file is missing
TEST-08 tests/components/jaalee/test_coordinator.py: Required contract file is missing
HA-13 custom_components/__init__.py: Required contract file is missing
HA-11 custom_components/jaalee/translations/ko.json: [Errno 2] No such file or directory: 'custom_components/jaalee/translations/ko.json'
TEST-08 tests/__init__.py: must exist and be empty
TEST-08 tests/components/__init__.py: must exist and be empty
TEST-08 tests/components/jaalee/__init__.py: must exist and be empty
TEST-03 tests/conftest.py: must match the central template exactly
TEST-08 tests/components/jaalee/conftest.py: Exactly one ordered domain-fixtures marker pair required
```
- 독립 리뷰: 별도 review_checker_rollout 담당자가 19개 리포의 workflow 69개·기존 job 100개를 구조 비교했습니다. 새 CI 회귀 지적 없음. 기존 job ID·입력·권한·지원 최소와 통합 코드 보존 및 새 standards job의 중앙 템플릿 일치 확인. 실행 변경 없는 이 기록 추가 전 작업 트리를 검토했습니다.


## 2026-10-25 CI 실패 보완 검증

- 이전 부분 갱신의 실패 진단을 실제 수정했습니다. 표준 README 관리 영역과 실제 설치 앵커를 중앙 렌더러로 적용하고, 제품 기능에 근거한 manifest categories 및 검토 근거를 기록했습니다. 기존 제품별 사용 설명·지원 최소·회귀 테스트를 보존합니다.
- 범위: custom_components namespace 파일, 정확한 중앙 루트 테스트 설정·빈 package 파일, domain fixture 관리 영역을 보완했습니다. 기존 HA fixture와 통신 mock은 유지합니다.
- 실제 배포용 영어 문자열과 strings.json을 정합화했습니다. 한국어 번역과 실제 not_supported abort 키를 추가했습니다.
- 기존 실제 HA 광고 갱신 회귀를 test_coordinator.py로 옮기고 production coordinator의 last_service_info 연결을 검증했습니다. 테스트 개수와 기존 센서 결과 검증을 보존합니다.
- 원격 Hassfest는 categories를 지원하는 검토 Core `ec18d8b25d1ee39aa8b85a72a170e42bee33228c`의 공식 validator 경로를 사용합니다. 통합 지원 최소를 올리지 않습니다.
- 현재 환경 실제 버전: `{"python": "3.14.5", "homeassistant": "2026.10.2", "pytest-homeassistant-custom-component": "0.13.373"}`. 각 리포 별도 격리 환경에서 의존성을 설치하고 pip check PASS.
- `python -m pytest tests/components/jaalee/ -q`: **30 passed**, skip 없음. 최신 중앙 검사기·actionlint·Ruff lint/format·git diff --check PASS.
- 최소 HA 조합과 최종 head 원격 CI는 이 PR의 갱신된 checks 결과로 확인합니다. 실물 기기·실제 외부 API/서버 검증은 수행하지 않았습니다.
- 독립 리뷰: 주 담당 root가 해당 작업 트리를 검토했습니다. 제품 분류의 실제 기능 근거, 기존 테스트 보존·의미 있는 파일 이동, fixture 역할 alias, 번역 및 README 관리 영역을 확인했으며 manifest 키 순서 지적 수정 후 추가 회귀 지적 없음.
