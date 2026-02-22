# Tasks: AI 에이전트 공통 워크플로우 컨벤션

## Goal

`.planning/PL-25324/workflow/CLAUDE.md`의 File-based Planning Workflow를 에이전트 무관한 AGENTS.md로 전환하고, symlink + README.md + 템플릿 정비를 완료한다.

## Current Phase

🔄 Phase 5: Final Gate & Delivery

## Phases

### Phase 1: Requirements & Discovery ✅

- [x] 요구사항 정의 (spec.md)
- [x] 기존 문서 분석 (CLAUDE.md, templates/, records/)
- [x] 아키텍처 결정 (AGENTS.md = SSoT, CLAUDE.md/GEMINI.md = symlink)
- [x] 스펙 리뷰 및 승인

### Phase 2: Planning & Structure ✅

- [x] 구현 계획 작성 (plan.md)
- [x] Claude-specific → 자연어 전환 매핑 확정
- [x] AGENTS.md 문서 구조 확정
- [x] 템플릿 수정 범위 확정

### Phase 3: Implementation ✅

- [x] Step 1: AGENTS.md 작성 (CLAUDE.md 기반 자연어 전환)
- [x] Step 2: Symlink 생성 (CLAUDE.md → AGENTS.md, GEMINI.md → AGENTS.md)
- [x] Step 3: 템플릿 정비 (tasks.md Phase 4/5, findings.md Review Findings, progress.md Review Log)
- [x] Step 4: README.md 작성 (개발자 온보딩 + 에이전트별 설정)
- [x] Step 5: Jira 티켓 연동 - 스크립트 기반으로 전환 (AGENTS.md에 `jira-sync.py` 실행 절차 문서화)
- [x] Step 6: `scripts/jira-sync.py` 스크립트 작성 (pull/push 서브커맨드, 7개 단위 테스트 통과)

### Phase 4: Multi-perspective Review ✅

- [x] 목적 부합 검토: AGENTS.md가 에이전트 무관 워크플로우로서 완전한가? → PASS (7개 핵심 요소 모두 포함)
- [x] 버그/보안/크리티컬 검토: Claude 고유 용어 잔존 없는가? → PASS (0건), jira-sync.py 보안 수정 완료
- [x] 사이드 이펙트 검토: symlink이 모든 환경에서 동작하는가? → PASS (검증 완료)
- [x] 코드 통합/재사용 검토: CLAUDE.md 대비 누락 항목 없는가? → PASS (누락 0건)
- [x] 전체 변경 사항 통합 검토 → README.md 불일치 3건 수정 완료
- [x] 연쇄 검토 → 보안 수정 후 7개 테스트 통과, 연쇄 문제 없음

### Phase 5: Final Gate & Delivery 🔄

- [x] 배포 준비도 평가 → SC-1~SC-6 전수 통과
- [x] 타임스탬프 기반 양방향 충돌 감지 구현 (27개 테스트 통과)
- [x] 인증 안정화 (클래식 토큰 + Basic Auth 확정, JIRA_AUTH_METHOD 옵션)
- [x] 파싱 견고성 수정 (rindex로 내장 마커 대응)
- [x] 문서 업데이트 (AGENTS.md, README.md, jira-sync.py, findings.md, progress.md)
- [x] push 정상 동작 확인
- [ ] 커밋

## Notes

- 진행할 때마다 Phase 상태를 업데이트하세요: ⏸️ 대기 → 🔄 진행 중 → ✅ 완료
- 결정 사항은 findings.md의 Technical Decisions에 기록하세요.
- 오류는 findings.md의 Issues Encountered에 기록하세요.
<!-- LAST_SYNC: 2026-02-22 19:52:50 KST -->
