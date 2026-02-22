# Tasks: 기능명

<!-- 기능의 한국어 이름을 제목에 포함합니다. -->

## Goal

<!-- 명확한 최종 목표를 작성합니다. -->

## Current Phase

<!-- 현재 진행 중인 단계를 표시합니다. 이모지: 🔄 진행 중, ✅ 완료, ⏸️ 대기 -->

🔄 Phase 1: Requirements & Discovery

## Phases

<!-- 각 단계의 작업을 체크박스로 관리합니다. -->

### Phase 1: Requirements & Discovery 🔄

- [ ] 요구사항 정의
- [ ] 기존 코드 분석
- [ ] 스펙 문서 작성 (spec.md)
- [ ] 스펙 리뷰 및 승인

### Phase 2: Planning & Structure ⏸️

- [ ] 구현 계획 작성 (plan.md)
- [ ] 기존 코드 상세 분석
- [ ] 관련 클래스/메서드 존재 여부 확인

### Phase 3: Implementation ⏸️

- [ ] UI Layer 구현
- [ ] Application Layer 구현
- [ ] Domain Layer 구현
- [ ] Infrastructure Layer 구현 (필요시)
- [ ] 단계별 컴파일 검증
- [ ] 테스트 작성 및 실행

### Phase 4: Multi-perspective Review ⏸️

- [ ] 목적 부합 검토: 구현이 원래 목적에 맞는가?
- [ ] 버그/보안/크리티컬 검토: 잠재적 버그나 보안 문제는?
- [ ] 개선 부작용 검토: 개선에 새로운 문제는?
- [ ] 함수/파일 크기 검토: 적절히 나눠야 하는가?
- [ ] 코드 통합/재사용 검토: 기존 코드와 통합 가능한 부분은?
- [ ] 사이드 이펙트 검토: 다른 모듈에 영향은?
- [ ] 전체 변경 사항 통합 검토
- [ ] 불필요한 코드 검토: 데드코드는?
- [ ] 코드 품질 검토
- [ ] 사용자 흐름(UX) 검토
- [ ] 연쇄 검토: 수정이 새 문제를 만들지 않는가?

### Phase 5: Final Gate & Delivery ⏸️

- [ ] 배포 준비도 평가
- [ ] 커밋 및 PR 작성

## Notes

<!-- 필요시 추가 항목을 덧붙입니다. -->

- 진행할 때마다 Phase 상태를 업데이트하세요: ⏸️ 대기 → 🔄 진행 중 → ✅ 완료
- 결정 사항은 findings.md의 Technical Decisions에 기록하세요.
- 오류는 findings.md의 Issues Encountered에 기록하세요.
