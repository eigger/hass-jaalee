# 적용한 공통 규칙

- 표준: https://github.com/eigger/hass-repo-standards/tree/main
- 참조 커밋 SHA: `c696e15c164daa6c7deca4140b899bd0e80e8846`
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
