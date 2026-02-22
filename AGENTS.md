# File-based Planning Workflow

파일 시스템을 AI 에이전트의 영구 메모리로 활용하고, 검토 주도 개발(Review-Driven Development)로 품질을 보장하는 워크플로우입니다.

## 해결하는 문제

AI 에이전트는 다음과 같은 한계가 있습니다:
- 컨텍스트가 리셋되면 작업 내용을 잊어버림
- 긴 작업 중에는 원래 목표를 잃어버림
- 실패한 시도가 추적되지 않아 같은 실수를 반복함
- "전반적으로 검토해줘"라고 하면 아무것도 깊이 보지 않음
- 구현은 잘하지만, 구현의 적절성을 스스로 판단하지 못함

## 세 가지 접근의 결합

| 접근 방식 | 역할 | 도구 |
|-----------|------|------|
| **Spec-Driven Development** | "무엇을" 만들지 사전에 명확히 정의 (Top-down) | 계획 수립 도구를 활용하세요 |
| **File-based Planning** | "어떻게" 진행되는지 과정을 추적 (Bottom-up) | Planning Files (spec.md, plan.md, tasks.md, findings.md, progress.md, README.md) |
| **Review-Driven Development** | 다관점 검토로 품질을 보장 (Quality Gate) | 코드 리뷰를 수행하세요 + 수동 검토 단계 |

**Spec으로 방향을 정하고, Planning으로 과정을 추적하고, Review로 품질을 보장합니다.**

### 단일 진입점: "{티켓번호} 작업 시작" 프롬프트

사용자는 `"{티켓번호} 작업 시작"` 프롬프트 하나로 전체 흐름을 시작합니다:

```
"{티켓번호} 작업 시작" 입력
  → Phase 1: 계획 인터뷰 및 검증
  → 사용자 승인
  → Phase 2: Planning Files 자동 생성 (spec.md, plan.md, tasks.md, findings.md, progress.md, README.md)
  → Phase 3~5: 구현, 검토, 배포
```

## 워크플로우 전체 흐름

```
Phase 1: 계획 수립 및 검증 (4단계) ─── 계획을 세우고, 세 번 검토한다
Phase 2: Planning Files 생성       ─── 영구 메모리를 준비한다
Phase 3: 구현 (1단계)             ─── 구현은 단 한 단계다
Phase 4: 다층 검토 (11단계)       ─── 11개 관점으로 검토한다
Phase 5: 최종 게이트 및 배포       ─── 배포 수준인지 최종 확인한다
```

계획 4단계 + 구현 1단계 + 검토 11단계. 이 비율이 이 워크플로우의 철학입니다.
에이전트에게 구현은 쉽고, 올바른 구현이 어렵습니다.

---

## Phase 1: 계획 수립 및 검증

복잡한 작업을 시작하기 전에 4단계의 계획 검증을 거칩니다.

### 1단계: 계획 수립
계획 수립 도구를 활용하여 계획 인터뷰를 시작합니다.
- 코드베이스를 탐색하고 아키텍처를 분석하세요
- 사용자와 인터뷰를 통해 요구사항, 제약조건, 기술적 결정을 확정
- 실행 계획을 문서화
- **계획 완료 및 사용자 승인 후, 자동으로 Phase 2(Planning Files 생성)로 전환**

### 2단계: 계획 검토
계획이 올바른지 검토합니다.
- 요구사항을 빠짐없이 반영했는가?
- 기존 코드베이스의 패턴과 일관성이 있는가?
- 영향받는 모듈을 모두 파악했는가?

### 3단계: 검토의 검토 (메타 검증)
검토가 정확한지 다시 검토합니다.
- AI의 확증 편향(Confirmation Bias)을 완화하기 위한 자기 반성 단계
- "검토에서 놓친 것은 없는가?"

### 4단계: 과도함 검토
계획이 과도하지 않은지 검토합니다.
- 불필요한 추상화는 없는가?
- YAGNI(You Aren't Gonna Need It) 위반은 없는가?
- 구현 후 "줄여봐"보다 계획 단계에서 "과도하지 않은지 봐"가 비용 효율적

최종 실행 계획이 승인되면 Phase 2로 진행합니다.

## Phase 2: Planning Files 생성

Phase 1의 계획이 완료되고 사용자가 승인하면, **자동으로** `.planning/{티켓번호}/{하위디렉토리}/` 하위에 6개의 계획 파일을 생성합니다:

```
.planning/{티켓번호}/{하위디렉토리}/
  spec.md       -- 요구사항 명세
  plan.md       -- 구현 계획
  tasks.md      -- 작업 추적 (북극성)
  findings.md   -- 기술적 발견사항 및 결정
  progress.md   -- 세션별 작업 내역
  README.md     -- 기능 설명 (Background, Goal, How it works)
```

## Phase 3: 구현

전체 워크플로우 중 구현은 **단 한 단계**입니다.

작업 중 다음 규칙을 따릅니다:
- **파일 수정 전**: `tasks.md`를 읽고 `[Phase N] 작업 요약 - tasks.md 확인 완료`로 응답 시작 (Rule 4: 절대 규칙)
- **파일 수정 후**: 진행 상황을 `tasks.md`에 반영
- **에러 발생 시**: 즉시 `findings.md`의 Issues Encountered에 기록
- **기술적 발견 시**: `findings.md`에 즉시 기록
- **5회 연속 작업 후**: `tasks.md`를 다시 읽어 방향 확인
- **구현 완료 후**: 테스트를 작성하고 실행

## Phase 4: 다층 검토 (11개 관점)

구현 후 서로 다른 관점으로 검토합니다. "전반적으로 검토해줘"가 아니라 각각 다른 렌즈를 씌워야 해당 관점에 집중합니다.

| 단계 | 검토 관점 | 검토 유형 | 질문 |
|------|-----------|-----------|------|
| 1 | 목적 부합 | 기능 검증 | 구현이 원래 목적에 맞게 잘 됐는가? |
| 2 | 버그, 보안, 크리티컬 | 안전성 검증 | 잠재적 버그나 보안 문제는 없는가? |
| 3 | 개선 부작용 | 변경 검증 | 개선한 내용에 새로운 문제는 없는가? |
| 4 | 함수/파일 크기 | 구조 개선 | 매우 큰 함수/파일을 적절히 나눠야 하는가? |
| 5 | 코드 통합/재사용 | 중복 제거 | 기존 코드와 통합하거나 재사용할 수 있는 부분은? |
| 6 | 사이드 이펙트 | 영향 범위 검증 | 변경이 다른 모듈에 영향을 주지 않는가? |
| 7 | 전체 변경 사항 | 통합 검토 | 전체 diff를 다시 한 번 검토 |
| 8 | 불필요한 코드 | 데드코드 제거 | 구현 과정에서 불필요해진 코드는 없는가? |
| 9 | 코드 품질 | 품질 게이트 | 코드 품질이 충분히 높은가? |
| 10 | 사용자 흐름 (UX) | 사용성 검증 | 사용자의 사용 흐름에 문제는 없는가? |
| 11 | 연쇄 검토 | 반복 검증 | 검토 중 발견된 문제의 수정이 새로운 문제를 만들지 않는가? |

**연쇄 검토 종료 조건**: 더 이상 문제가 발견되지 않을 때까지 반복하되, 3회 반복 후에도 새 문제가 계속 발생하면 사용자에게 에스컬레이션합니다.

## Phase 5: 최종 게이트 및 배포

### 배포 준비도 평가
모든 검토를 종합하는 최종 판단입니다. 개별 검토를 다 통과해도 전체적으로 배포 수준이 아닐 수 있습니다.

- 이대로 배포해도 될 정도의 퀄리티인가?
- 테스트가 모두 통과하는가?
- `progress.md`에 세션 작업 내역을 기록했는가?
- `tasks.md`의 모든 Phase가 complete인가?

### 커밋 및 PR
커밋 메시지는 `[{티켓번호}] 작업 요약` 형태를 따릅니다. 예: `[PL-12345] 로그인 API 인증 오류 수정`

---

## Planning Files

### 파일 저장 위치
Planning Files는 `.planning/{티켓번호}/{하위디렉토리}/` 하위에 생성합니다.

```
.planning/
└── PL-12345/feature-name/
    ├── spec.md         -- 요구사항 명세
    ├── plan.md         -- 구현 계획
    ├── tasks.md        -- 작업 추적 (북극성)
    ├── findings.md     -- 기술적 발견사항 및 결정
    ├── progress.md     -- 세션별 작업 내역
    └── README.md       -- 기능 설명 (Background, Goal, How it works)
```

### spec.md - 요구사항 명세

```markdown
# Feature Specification: 기능명

## Overview
기능의 핵심 내용

## User Scenarios & Testing (mandatory)

### User Story 1: 시나리오명
- As: ~는
- I: ~할 수 있다
- So: ~하기 위해

#### Acceptance Scenarios
Scenario 1: **시나리오명**
- Given: ~할 때
- When: ~하면
- Then: 결과

## Functional Requirements (mandatory)
- FR-1: MUST 요구사항 설명
- FR-2: SHOULD 요구사항 설명

## Constraints (mandatory)
- CON-1: MUST 제약사항 설명

## Success Criteria (mandatory)
- SC-1: 성공 기준 설명
```

### plan.md - 구현 계획

```markdown
# Implementation Plan: 기능명

## Summary
주요 구현 방식 1-2문장 요약

## Requirements
1. 요구사항 1
2. 요구사항 2

## Critical Files

### New Files
- path/to/NewFile

### Modified Files
- path/to/ExistingFile

### Reference Files
- path/to/ReferenceFile

## Architecture
아키텍처 다이어그램

## Implementation Steps

### Step 1: 제목
구현 내용

### Step 2: 제목
구현 내용

## Verification
검증 방법

## Considerations
구현 시 고려사항
```

### tasks.md - 작업 계획 및 추적

```markdown
# Project: [PL-번호] [프로젝트명]

## Goal
명확한 최종 목표 (북극성 역할)

## Current Phase
Phase N: [현재 단계명]

## Phases

### Phase 1: Requirements & Discovery
- [x] 사용자 요구사항 확인
- [x] 기존 코드베이스 탐색
- **Status:** complete

### Phase 2: Planning & Structure
- [ ] 아키텍처 설계
- [ ] 인터페이스 정의
- [ ] 과도함 검토 (오버엔지니어링 체크)
- **Status:** in_progress

### Phase 3: Implementation
- [ ] 핵심 기능 구현
- [ ] 테스트 작성 및 실행
- **Status:** pending

### Phase 4: Multi-perspective Review
- [ ] 목적 부합 검토
- [ ] 버그/보안/크리티컬 검토
- [ ] 사이드 이펙트 검토
- [ ] 코드 품질/구조 검토
- [ ] 전체 변경 사항 통합 검토
- **Status:** pending

### Phase 5: Final Gate & Delivery
- [ ] 배포 준비도 평가
- [ ] 커밋 및 PR 작성
- **Status:** pending

## Key Questions
1. [답을 찾아야 할 질문]

## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|

## Notes
- Phase 상태를 업데이트하세요: pending -> in_progress -> complete
- 중요한 결정 전에 이 계획을 다시 읽으세요 (attention manipulation)
- 모든 오류를 기록하세요 - 같은 실수를 반복하지 않습니다
```

### findings.md - 기술적 발견사항 및 결정

```markdown
# Findings & Decisions

## Requirements
- [ ] 요구사항 목록

## Research Findings

### 코드베이스 구조
- 관련 모듈, 패턴, 의존성 등

### 기존 패턴
- 프로젝트에서 사용 중인 컨벤션

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered

### 1. [이슈 제목]
**문제**: 설명
**해결**: 조치 내용
**결과**: 성공/실패

## Review Findings
검토 과정에서 발견된 사항을 기록합니다.

| 검토 관점 | 발견 사항 | 조치 |
|-----------|-----------|------|

## Resources
- 참조 문서, 코드 위치 (파일:라인) 등
```

### progress.md - 세션별 작업 내역

날짜순(오름차순)으로 기록합니다. 가장 최근 세션이 맨 아래에 위치합니다.

```markdown
# Progress Log

## Session [날짜]

### Phase N: [제목]
- **Status:** in_progress
- **Started:** [시각]
- Actions taken:
  - 수행한 작업 목록
- Files created/modified:
  - 변경된 파일 목록

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|

## Review Log
| 검토 단계 | 관점 | 결과 | 발견된 문제 |
|-----------|------|------|-------------|

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|

## 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| 1. 현재 어느 단계인가? | Phase N |
| 2. 다음에 할 일은? | 남은 Phases |
| 3. 목표는? | [goal statement] |
| 4. 지금까지 배운 것? | See findings.md |
| 5. 완료한 작업은? | See above |
```

### README.md - 기능 설명

```markdown
# 기능명

## Background
왜 이 기능이 필요한가

## Goal
무엇을 달성하려 하는가

## How it works

### 활성화
- 동작 설명

### 비활성화
- 동작 설명

## Related Documents
- [spec.md](spec.md): 요구사항 및 상세 스펙
- [plan.md](plan.md): 기술 구현 계획
```

---

## 핵심 규칙

### 1. Plan First
복잡한 작업(3단계 이상)은 반드시 `tasks.md`를 먼저 생성합니다. 비협상입니다.

### 2. 계획은 3번 검토
계획 수립 후 반드시 검토 -> 메타 검증 -> 과도함 검토를 거칩니다.

### 3. 2-Action Rule
2번의 조회/검색 작업 후 반드시 발견사항을 `findings.md`에 저장합니다.

### 4. Read Before Act (절대 규칙)
어떤 도구(터미널, 파일 수정 등)를 사용하기 전에, **반드시 `tasks.md`를 먼저 읽어 최신 상태를 확인하라.**
메모리(컨텍스트)에만 의존하여 코드를 수정하려 하지 마라. 반드시 파일을 다시 읽어라.

**필수 실행 시점:**
- **파일을 수정하기 전** (코드, 설정, 문서 등)
- **새로운 Phase를 시작할 때**
- **5회 이상 연속 작업 후** (주기적 리마인드)
- **에러가 발생했을 때** (방향을 잃지 않기 위해)

**응답 접두어 규칙:**
tasks.md를 읽은 후, 응답의 첫 줄에 반드시 현재 상태를 명시하라:
```
[Phase N] {현재 작업 요약} - tasks.md 확인 완료
```
이 접두어가 없는 응답은 규칙 위반이다. 사용자는 접두어 없는 응답을 발견하면 즉시 작업을 중단시킬 수 있다.

> 이 규칙은 플러그인의 자동 리로드 훅을 자연어로 대체한다.
> 프로그래밍적 강제는 불가능하므로, "응답 접두어"로 검증 가능성을 확보한다.

### 5. Update After Act
Phase 완료 후 상태를 업데이트합니다: `pending` -> `in_progress` -> `complete`

### 6. Log ALL Errors
모든 에러를 기록합니다. 이것이 같은 실수 반복을 방지합니다.

### 7. 다관점 검토
"전반적으로 검토해줘"가 아니라, 각 관점별로 개별 검토합니다.
하나의 렌즈로 하나의 차원만 봐야 깊이 있는 검토가 가능합니다.

### 8. 3-Strike Error Protocol
```
ATTEMPT 1: 진단 및 수정 - 에러 분석, 근본 원인 파악, 대상 수정
ATTEMPT 2: 대안 접근 - 같은 에러 발생 시 다른 방법 시도
ATTEMPT 3: 전면 재고 - 가정 의심, 해법 검색, 계획 수정 고려
3회 실패 후: 사용자에게 에스컬레이션
```

## 적용 기준

**사용하는 경우:**
- 다단계 작업 (3단계 이상)
- 여러 모듈에 걸친 변경
- 조사/연구가 필요한 작업
- 새로운 기능 구현

**건너뛰는 경우:**
- 단순 질문 답변
- 단일 파일 수정
- 빠른 조회

---

## 프롬프트 컨벤션

작업을 시작하거나 재개할 때 다음 프롬프트 형식을 사용합니다.

| 상황 | 프롬프트 형식 | 예시 |
|------|--------------|------|
| 새 작업 시작 | `{티켓번호} 작업 시작` | `PL-12345 작업 시작` |
| 작업 이어서 진행 | `{티켓번호} 이어서` | `PL-12345 이어서` |
| 특정 Phase 재개 | `{티켓번호} Phase {N} 재개` | `PL-12345 Phase 3 재개` |
| 검토 단계 시작 | `{티켓번호} 검토 시작` | `PL-12345 검토 시작` |
| 상태 확인 | `{티켓번호} 현황` | `PL-12345 현황` |

---

## Jira 티켓 연동

> **중요: 에이전트는 Jira에 직접 접근하지 않는다.**
> 인증 장벽, 파싱 오류로 인한 데이터 유실, 토큰 낭비를 방지하기 위해
> 반드시 `jira-sync.py` 스크립트를 통해서만 Jira와 통신한다.

### 사전 요구사항

프로젝트 루트에 `scripts/jira-sync.py` 스크립트가 존재해야 하며,
의존성 설치와 환경 변수 설정이 필요하다:

```bash
# 의존성 설치
pip3 install -r scripts/requirements.txt

# 대화형 설정 (권장 - .env 파일에 자동 저장)
python3 scripts/jira-sync.py setup

# 또는 직접 환경 변수 설정
export JIRA_BASE_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
```

> 환경 변수가 없으면 pull/push 실행 시 대화형으로 값을 입력받고 `.env` 파일에 저장한다.

- **API 토큰**: https://id.atlassian.com/manage/api-tokens 에서 API 토큰 발급 (스코프 없는 클래식 토큰 권장)
- **인증 방식**: 기본값은 Basic Auth. 스코프 토큰 사용 시 `.env`에 `JIRA_AUTH_METHOD=bearer` 추가
- **Auto-Routing**: 스크립트가 `JIRA_BASE_URL`에서 cloudId를 자동 취득하여 API Gateway(`api.atlassian.com`)를 사용한다. 추가 환경 변수 불필요.

### 스크립트 실행 전 의존성 확인

에이전트는 `jira-sync.py`를 최초 실행하기 전에 반드시 의존성을 확인한다:

```bash
# 1. Python 3 존재 확인
python3 --version

# 2. requests 라이브러리 설치 확인
python3 -c "import requests" 2>/dev/null || pip3 install -r scripts/requirements.txt
```

- Python 3이 없으면 사용자에게 설치를 안내하고 작업을 중단한다.
- `requests`가 없으면 `pip3 install -r scripts/requirements.txt`로 설치를 시도한다.
- `pip3`도 없거나 설치가 실패하면 사용자에게 수동 설치를 안내하고 작업을 중단한다.

### 작업 시작 시 (Pull)

작업 시작 프롬프트(`{티켓번호} 작업 시작`)를 받으면:

1. **의존성 확인**: 위의 "스크립트 실행 전 의존성 확인" 절차를 수행한다 (세션당 1회).
2. **에이전트는 직접 브라우징을 시도하지 말고**, 반드시 터미널에서 스크립트를 실행한다:
   ```bash
   python3 scripts/jira-sync.py pull {티켓번호}
   ```
3. 스크립트가 Jira API 인증, 데이터 파싱, `.planning/{티켓번호}/{하위디렉토리}/` 내 파일 생성을 안전하게 처리한다.
4. **충돌 감지**: 각 파일별로 타임스탬프를 비교하여, 로컬이 더 최신이면 해당 파일을 스킵한다. 강제 덮어쓰기가 필요하면 `--force` 플래그를 사용한다:
   ```bash
   python3 scripts/jira-sync.py pull {티켓번호} --force
   ```
5. 스크립트 실행이 끝난 후, 에이전트는 생성된 로컬 파일만 읽고 작업을 시작한다.
6. 스크립트가 실패하면(티켓 미존재, 인증 오류, 의존성 누락 등) 에이전트는 경고를 표시하고 작업을 중단한다.

### 커밋/작업 완료 시 (Push)

커밋을 진행하기 전:

1. 로컬 planning 파일을 Jira에 동기화하기 위해 반드시 스크립트를 실행한다:
   ```bash
   python3 scripts/jira-sync.py push {티켓번호}
   ```
2. **충돌 감지**: 각 파일별로 타임스탬프를 비교하여, Jira가 더 최신이면 해당 파일을 스킵한다. 강제 덮어쓰기가 필요하면 `--force` 플래그를 사용한다:
   ```bash
   python3 scripts/jira-sync.py push {티켓번호} --force
   ```
3. 스크립트가 기존 Jira description을 안전하게 보존하면서, `PLANNING_START`~`PLANNING_END` 영역만 멱등성(Idempotency) 있게 업데이트한다.
4. 에이전트가 직접 텍스트를 조합하여 Jira description을 덮어쓰지 않는다.

### 직렬화 형식 (스크립트 내부 처리)

스크립트는 다음 형식으로 Jira description의 planning 영역을 관리한다:

```
(기존 Jira 티켓 설명 내용 - 그대로 보존)

=== PLANNING_START ===

=== FILE: spec.md [2026-02-22 15:30:00 KST] ===
(spec.md 내용)

=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===
(tasks.md 내용)

=== FILE: findings.md [2026-02-22 15:30:00 KST] ===
(findings.md 내용)

=== FILE: progress.md [2026-02-22 15:30:00 KST] ===
(progress.md 내용)

=== FILE: plan.md [2026-02-22 15:30:00 KST] ===
(plan.md 내용)

=== FILE: README.md [2026-02-22 15:30:00 KST] ===
(README.md 내용)

=== PLANNING_END ===
```

- 각 FILE 마커에 KST 타임스탬프가 포함되어 양방향 충돌 감지에 사용된다
- 로컬 파일 하단에 `<!-- LAST_SYNC: 2026-02-22 15:30:00 KST -->` 메타데이터가 삽입된다
- 최초 push 시 planning 영역이 없으면 description 끝에 append
- 이후 push 시 기존 `PLANNING_START`~`PLANNING_END` 영역을 교체

---

## 세션 복구

컨텍스트 리셋 또는 `{티켓번호} 이어서` 프롬프트 후 작업을 재개할 때:

1. `git branch --show-current`로 현재 브랜치 확인 → `{하위디렉토리}` 결정
2. `.planning/{티켓번호}/{하위디렉토리}/tasks.md`를 읽어 현재 Phase와 목표 확인
3. `.planning/{티켓번호}/{하위디렉토리}/progress.md`를 읽어 마지막 작업 내역 확인
4. `.planning/{티켓번호}/{하위디렉토리}/findings.md`를 읽어 기술적 결정사항 확인
5. `.planning/{티켓번호}/{하위디렉토리}/spec.md`를 읽어 요구사항 확인
6. `git diff --stat`으로 실제 코드 변경사항 확인
7. 계획 파일 업데이트 후 작업 재개
