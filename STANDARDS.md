# 적용한 공통 규칙

- 표준: https://github.com/eigger/hass-repo-standards/tree/v1.1.5
- 참조 커밋 SHA: f56987f7f765a774c926fb8005fe5df68bb32451
- Standards release: v1.1.5
- Resolved standards SHA: f56987f7f765a774c926fb8005fe5df68bb32451
- 채택일: 2026-10-18
- profile: integration / ha (실제 HA fixture·통합 로딩 필수)
- 적용 점검표: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md)
- 중앙 현황표: https://github.com/eigger/hass-repo-standards/blob/main/docs/adoption-status.md
- 조율 / 구현 / 독립 리뷰·검증 담당: 조율 `root` / 구현 `jaalee_implementation` / 독립 리뷰·검증 `jaalee_review`
- 중앙 현황 갱신일: 2026-10-18
- 실제 기본 브랜치: master
- 테스트 경로: tests/components/jaalee/
- 변경 전 지원 최소 HA / 선언 근거: 2025.1.0 / `hacs.json`
- 적용 후 지원 최소 HA: 2025.1.0 (변경 없음, 역사적 기준 보존)
- current HA 테스트 환경: Python 3.14.5, pytest-homeassistant-custom-component 0.13.373, HA 2026.10.2
- 최소 HA 검증 환경: Python 3.13.14, pytest-homeassistant-custom-component 0.13.201, HA 2025.1.0
- 최소 package 검증: bluetooth-sensor-state-data 1.7.5 (최소 HA), sensor-state-data 2.20.0

## 예외

현재 등록된 예외 없음.
## 2026-10-23 ZIP release and Downloads update

Base commit: `080e4c63d2524e5fc2ef03537aaf49cc4d78a1f6`. HACS remains Custom. `hacs.json` now selects `jaalee.zip`; publishing the next release builds and attaches that integration ZIP through the pinned central action. Analytics Usage is replaced by Downloads. The archive contains tracked integration files at its root. No existing release/tag/assets are modified.

Implementation and review: root; generated release caller reuses the independently reviewed central ZIP contract. Support minimum, manifest, code, dependencies, README body and prior adoption exceptions are preserved. Verification evidence is recorded in ADOPTION_CHECKLIST.md; this scoped update does not establish full standards compliance.

## 2026-10-25 중앙 검사기 갱신

- 검토한 중앙 main: `1863343638014adb8a4001afc8fddc1a27dc500f` (git ls-remote 확인). 이전 기본 기준 `c696e15c164daa6c7deca4140b899bd0e80e8846`의 채택 이력은 위 기록을 보존합니다.
- 모든 중앙 workflow/action pin과 reusable workflow의 standards-ref를 같은 검토 SHA로 맞춥니다. HACS-04는 actions/*의 full SHA 고정을 유지하면서 SHA 값 차이를 허용합니다.
- Validate에 중앙 템플릿의 무조건 실행 standards job을 추가합니다. 기존 HACS/Hassfest와 HA test job 이름·입력은 보존하며, 기본 브랜치를 사용하는 중앙 실행 조건을 적용합니다.
- 통합 코드·런타임 의존성·지원 최소·배포 버전은 이번 변경 대상이 아닙니다. 기존 채택 범위를 전체 완료로 바꾸지 않으며 실제 검증 결과와 남은 항목은 ADOPTION_CHECKLIST.md의 같은 날짜 기록을 참조합니다.


### 2026-10-25 Standards 파일·표시 이름 분리

- 기존 Validate의 중앙 검사 job을 `standards.yml`로 옮기고 workflow/job 표시 이름을 `Standards`로 줄였습니다. Validate의 HACS/Hassfest, 검사 항목·통과 기준·실행 단계·조건·권한은 유지합니다.
- 위치 인식과 중앙 명명 안내를 맞춘 검토 소스: `ca740d88b32fa5dcbc94c41fce2908450c76ed50` ([중앙 PR #24](https://github.com/eigger/hass-repo-standards/pull/24), 현재 이 PR의 의존 변경). 이전 기준 `1863343638014adb8a4001afc8fddc1a27dc500f`의 검증 이력은 앞 기록으로 보존합니다. 모든 중앙 pin·standards-ref는 같은 새 검토 소스로 맞춥니다.
### 2026-10-25 immutable central release reference migration

- User-requested partial migration: current central caller references use immutable `v1.0.0` resolved to `44349ee5621eea5d80e5c427f7a2435d2c2491bb`. Prior scoped ZIP SHA evidence is retained here: `ca740d88b32fa5dcbc94c41fce2908450c76ed50`. Runtime code, dependencies, support minimum, manifest and integration version are unchanged.
