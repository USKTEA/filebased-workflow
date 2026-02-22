# AI 에이전트 공통 워크플로우 컨벤션

## Background

현재 File-based Planning Workflow가 Claude Code 전용(`CLAUDE.md`)으로 작성되어 있어 다른 AI 에이전트(Codex, Gemini)에서는 동일한 워크플로우를 실행할 수 없다.
팀 내 각자 다른 AI 에이전트를 사용하더라도 동일한 개발 품질과 프로세스를 보장할 필요가 있다.

또한, 로컬 `.planning/` 문서와 Jira 티켓 간 동기화가 없어 팀 협업 시 planning 정보가 단절되는 문제가 있다.

## Goal

- `AGENTS.md`를 Single Source of Truth로 작성하여 어떤 AI 에이전트든 동일한 File-based Planning Workflow를 실행할 수 있도록 한다.
- `CLAUDE.md`, `GEMINI.md`는 `AGENTS.md`의 symlink으로 연결하여 DRY 원칙을 유지한다.
- Jira 티켓 양방향 동기화를 통해 팀 협업을 지원한다.
- 개발자 온보딩을 위한 README.md와 에이전트별 설정 가이드를 제공한다.

## How it works

### 워크플로우 시작

개발자가 AI 에이전트에 `{티켓번호} 작업 시작`이라고 말하면:

1. 에이전트가 `AGENTS.md`(또는 symlink인 `CLAUDE.md`/`GEMINI.md`)를 읽는다
2. `.planning/{티켓번호}/{하위디렉토리}/`에 planning 파일이 있는지 확인한다
3. 없으면 Jira 티켓에서 fetch하거나, `templates/`에서 새로 생성한다
4. 5-Phase 워크플로우(계획 → Planning Files → 구현 → 검토 → 배포)를 실행한다

### 파일 구조

```
AGENTS.md                          ← 공통 워크플로우 (Single Source of Truth)
CLAUDE.md → AGENTS.md (symlink)    ← Claude Code 자동 로딩
GEMINI.md → AGENTS.md (symlink)    ← Gemini CLI 자동 로딩

.planning/{티켓번호}/{하위디렉토리}/
├── tasks.md                       ← 작업 추적 (북극성)
├── findings.md                    ← 기술적 발견 및 결정
└── progress.md                    ← 세션별 작업 내역
```

### Jira 티켓 연동 (스크립트 기반)

에이전트는 Jira에 직접 접근하지 않는다. 반드시 스크립트를 통해서만 통신한다.

- **Pull**: `./scripts/jira-sync.py pull {티켓번호}` → Jira description에서 planning 파일 복원
- **Push**: `./scripts/jira-sync.py push {티켓번호}` → 로컬 planning 파일을 Jira에 동기화
- **사전 요구사항**: 환경 변수 설정 필요 (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`)
- **직렬화 형식**: `=== PLANNING_START/END ===`로 기존 description 보존, `=== FILE: {파일명} ===`로 파일 분리. 스크립트가 멱등성 보장

### 에이전트별 자동 로딩

| 에이전트      | 자동 로딩 파일 | 방식              |
|---------------|----------------|--------------------|
| Claude Code   | `CLAUDE.md`    | symlink → AGENTS.md |
| OpenAI Codex  | `AGENTS.md`    | 직접 로딩          |
| Google Gemini | `GEMINI.md`    | symlink → AGENTS.md |

## Related Documents

- [spec.md](spec.md): 요구사항 및 상세 스펙
- [plan.md](plan.md): 기술 구현 계획
- [tasks.md](tasks.md): 작업 추적
- [findings.md](findings.md): 기술적 발견 및 결정
- [progress.md](progress.md): 세션별 작업 내역
<!-- LAST_SYNC: 2026-02-22 19:52:50 KST -->
