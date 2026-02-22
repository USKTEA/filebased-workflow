# Feature Specification: AI 에이전트 공통 워크플로우 컨벤션

## Overview

개발자가 AI 에이전트에 특정 프롬프트를 입력하면, 에이전트가 AGENTS.md를 읽고 File-based Planning Workflow를 실행한다.
Claude, Codex, Gemini 어떤 AI 에이전트든 동일한 워크플로우를 따를 수 있다.

현재 `.planning/PL-25324/workflow/CLAUDE.md`에 Claude Code 전용으로 작성된 워크플로우를 에이전트 무관한 자연어로 전환한다.

## User Scenarios & Testing (mandatory)

### User Story 1: 새 작업 시작

- As: 개발자는
- I: AI 에이전트에게 "{티켓번호} 작업 시작"이라고 말할 수 있다
- So: 어떤 AI 에이전트든 동일한 File-based Planning Workflow를 실행하기 위해

#### Acceptance Scenarios

Scenario 1: **최초 작업 시작**

- Given: 프로젝트에 AGENTS.md가 있고, `.planning/PL-XXXXX/`가 없을 때
- When: "PL-XXXXX 작업 시작"이라고 말하면
- Then: 에이전트가 AGENTS.md를 읽고, templates/에서 planning 파일을 생성하고, Phase 1을 시작한다

Scenario 2: **세션 복구 (이어서 작업)**

- Given: `.planning/PL-XXXXX/{하위디렉토리}/tasks.md`가 이미 존재할 때
- When: "PL-XXXXX 작업 시작"이라고 말하면
- Then: 에이전트가 tasks.md를 읽고, 중단된 Phase부터 재개한다

Scenario 3: **로컬 파일 없을 때 Jira에서 fetch**

- Given: 로컬 `.planning/PL-XXXXX/`가 없고, Jira 티켓이 존재할 때
- When: "PL-XXXXX 작업 시작"이라고 말하면
- Then: Jira 티켓 description의 `PLANNING_START~END` 영역을 파싱하여 로컬 파일로 생성한다

Scenario 4: **Jira 티켓이 존재하지 않을 때**

- Given: Jira 티켓(`https://htbeyond.atlassian.net/browse/PL-XXXXX`)이 존재하지 않을 때
- When: "PL-XXXXX 작업 시작"이라고 말하면
- Then: 경고를 표시하고 중단한다

### User Story 2: 에이전트 간 동일 워크플로우

- As: 팀은
- I: 각자 다른 AI 에이전트(Claude, Codex, Gemini)를 사용하더라도 동일한 워크플로우를 실행할 수 있다
- So: 팀 전체의 개발 품질을 일관되게 유지하기 위해

#### Acceptance Scenarios

Scenario 1: **Claude Code 사용자**

- Given: 프로젝트에 CLAUDE.md(→ AGENTS.md symlink)가 있을 때
- When: Claude Code가 CLAUDE.md를 자동 로딩하면
- Then: AGENTS.md의 워크플로우를 읽고 동일하게 실행한다

Scenario 2: **Gemini 사용자**

- Given: 프로젝트에 GEMINI.md(→ AGENTS.md symlink)가 있을 때
- When: Gemini CLI가 GEMINI.md를 자동 로딩하면
- Then: AGENTS.md의 워크플로우를 읽고 동일하게 실행한다

## Functional Requirements (mandatory)

- FR-1: MUST AGENTS.md에 5-Phase 워크플로우, 3-File Pattern, 11-관점 검토, 핵심 규칙 8가지를 포함
- FR-2: MUST Claude 전용 표현을 자연어 지시문으로 전환 (Claude 고유 용어 0건)
- FR-3: MUST CLAUDE.md, GEMINI.md는 AGENTS.md의 symlink으로 생성
- FR-4: MUST `.planning/{티켓번호}/{하위디렉토리}/` 경로 컨벤션을 정의 (브랜치명 기반)
- FR-5: MUST 프롬프트 기반 컨벤션 정의 ("{티켓번호} 작업 시작" 등)
- FR-6: SHOULD templates/tasks.md에 Phase 4(Multi-perspective Review), Phase 5(Final Gate) 추가
- FR-7: SHOULD templates/findings.md에 Review Findings 섹션 추가
- FR-8: SHOULD templates/progress.md에 Review Log 섹션 추가
- FR-9: SHOULD README.md에 빠른 시작, 에이전트별 설정, 플러그인 설치 가이드 포함
- FR-10: MUST 작업 시작 시 `./scripts/jira-sync.py pull {티켓번호}`를 실행하여 Jira 티켓에서 planning 파일을 fetch
  - 에이전트가 직접 Jira에 접근하지 않음 (인증 장벽, 파싱 오류, 토큰 낭비 방지)
  - 스크립트가 실패하면 경고 표시 후 중단
- FR-11: MUST 커밋 전 `./scripts/jira-sync.py push {티켓번호}`를 실행하여 로컬 planning 파일을 Jira에 동기화
- FR-13: MUST `scripts/jira-sync.py` 스크립트를 프로젝트에 포함 (pull/push 서브커맨드)
- FR-14: MUST 환경 변수 사전 설정 필요 (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`)
- FR-12: MUST Jira description ↔ 로컬 파일 간 직렬화 형식을 정의한다
  - 영역 구분자: `=== PLANNING_START ===` / `=== PLANNING_END ===`로 기존 description과 planning 영역을 분리
  - 파일 구분자: `=== FILE: {파일명} ===`
  - 대상 파일: spec.md, plan.md, tasks.md, findings.md, progress.md, README.md
  - Fetch 시: `PLANNING_START`~`PLANNING_END` 영역만 파싱 → 파일 구분자로 split → 각 파일로 저장
  - Push 시: 기존 description 보존 + `PLANNING_START`~`PLANNING_END` 영역만 교체 (append 또는 modify)
  - 최초 push 시 planning 영역이 없으면 description 끝에 append
  - 형식 예시:
    ```
    (기존 Jira 티켓 설명 내용 - 그대로 보존)

    === PLANNING_START ===

    === FILE: spec.md ===
    (spec.md 내용)

    === FILE: tasks.md ===
    (tasks.md 내용)

    === FILE: findings.md ===
    (findings.md 내용)

    === FILE: progress.md ===
    (progress.md 내용)

    === FILE: plan.md ===
    (plan.md 내용)

    === FILE: README.md ===
    (README.md 내용)

    === PLANNING_END ===
    ```

## Constraints (mandatory)

- CON-1: MUST Jira 티켓 기반 연동 포함 (description fetch 및 sync)
- CON-2: MUST Copilot(.github/copilot-instructions.md)은 이번 스코프에서 제외
- CON-3: MUST 한국어로 작성 (팀 업무 언어)
- CON-4: MUST `.planning/PL-25324/workflow/CLAUDE.md` 원본은 보존 (히스토리 가치)

## Success Criteria (mandatory)

- SC-1: AGENTS.md에 Claude 고유 용어가 0건 (grep 전수 검사)
- SC-2: CLAUDE.md, GEMINI.md symlink이 정상 동작 (`cat CLAUDE.md` → AGENTS.md 내용 출력)
- SC-3: `.planning/PL-25324/workflow/CLAUDE.md`의 모든 핵심 내용이 AGENTS.md에 포함 (누락 0건)
- SC-4: README.md에 3개 에이전트(Claude, Codex, Gemini) 설정 가이드 포함
- SC-5: `jira-sync.py pull` 실행 시 Jira description에서 planning 파일 복원 성공
- SC-6: `jira-sync.py push` 실행 시 기존 description 보존 + planning 영역만 업데이트 성공

## 산출물

| 파일                    | 유형 | 설명                                          |
|-------------------------|------|-----------------------------------------------|
| `AGENTS.md`             | 신규 | 공통 워크플로우 (핵심, Single Source of Truth) |
| `CLAUDE.md`             | 신규 | → AGENTS.md symlink                           |
| `GEMINI.md`             | 신규 | → AGENTS.md symlink                           |
| `README.md`             | 신규 | 개발자 온보딩 + 에이전트별 설정 가이드        |
| `templates/tasks.md`    | 수정 | Phase 4/5 추가                                |
| `templates/findings.md` | 수정 | Review Findings 섹션 추가                     |
| `templates/progress.md` | 수정 | Review Log 섹션 추가                          |
| `scripts/jira-sync.py`  | 신규 | Jira pull/push 스크립트 (인증, 파싱, 멱등성)  |

## 참고

- 팀은 Atlassian 사용 중 (https://htbeyond.atlassian.net)
- 브랜치 규칙: PL-숫자 또는 PL-숫자/요약
- 커밋 컨벤션: [PL-숫자] 작업 요약
- 원본 소스: `.planning/PL-25324/workflow/CLAUDE.md`
- 실제 사용 사례: `records/` (PL-24646)
<!-- LAST_SYNC: 2026-02-22 19:52:13 KST -->
