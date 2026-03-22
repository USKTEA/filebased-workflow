# Tasks: 기능명

<!-- 기능의 한국어 이름을 제목에 포함합니다. -->

## Goal

<!-- 명확한 최종 목표를 작성합니다. -->

## Current Phase

<!-- 현재 진행 중인 단계를 표시합니다. 이모지: 🔄 진행 중, ✅ 완료, ⏸️ 대기 -->

🔄 Phase 1: Planning & Verification

## Phases

<!-- 각 단계의 작업을 체크박스로 관리합니다. -->

### Phase 1: Planning & Verification 🔄

- [ ] 요구사항 정의
- [ ] 기존 코드 분석
- [ ] 계획 리뷰 (Plan Review)
- [ ] 메타 리뷰 (Meta-Review)
- [ ] 과설계 체크 (Over-engineering Check)
- [ ] 사용자 승인

### Phase 2: Generate Planning Files ⏸️

- [ ] spec.md 작성
- [ ] plan.md 작성
- [ ] tasks.md 작성
- [ ] findings.md 작성
- [ ] progress.md 작성
- [ ] README.md 작성
- [ ] 사용자 승인

### Phase 3: ATDD 인수 테스트 작성 ⏸️

- [ ] spec.md 분석 (AC, FR, CON 추출)
- [ ] 인수 테스트 생성
- [ ] 커버리지 리포트 확인 (모든 FR/CON 매핑)
- [ ] 사용자 승인

### Phase 4: Implementation ⏸️

- [ ] Application Layer 구현
- [ ] Domain Layer 구현
- [ ] Infrastructure Layer 구현 (필요시)
- [ ] 단계별 컴파일 검증
- [ ] 인수 테스트 통과 확인

### Phase 5: Multi-perspective Review ⏸️

- [ ] 목적 부합 검토: 구현이 원래 목적에 맞는가?
- [ ] 버그/보안 검토: 잠재적 버그나 보안 문제는?
- [ ] 영향 범위 검토: 변경이 새로운 문제를 만들거나 다른 모듈에 영향은?
- [ ] 코드 구조/품질 검토: 데드코드, 중복, 과대 함수, 통합 기회는?
- [ ] 사용자 흐름(UX) 검토
- [ ] 연쇄 검토: 수정이 새 문제를 만들지 않는가?
- [ ] 추상화 수준 감사: raw/low-level API에 더 나은 대안은?
- [ ] 소유권 확인: 핵심 설계 결정 3개를 설명할 수 있는가?
- [ ] 암묵적 전제 감사: 이 코드가 작동하기 위한 인프라/환경 전제는?

### Phase 6: Final Gate & Delivery ⏸️

- [ ] 배포 준비도 평가
- [ ] 커밋 및 PR 작성

## Notes

<!-- 필요시 추가 항목을 덧붙입니다. -->

- 진행할 때마다 Phase 상태를 업데이트하세요: ⏸️ 대기 → 🔄 진행 중 → ✅ 완료
- 결정 사항은 findings.md의 Technical Decisions에 기록하세요.
- 오류는 findings.md의 Issues Encountered에 기록하세요.
- Phase 전환은 `/advance-phase`로 수행합니다.
