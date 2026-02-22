# Implementation Plan: AI 에이전트 공통 워크플로우 컨벤션 구축

## Summary

`.planning/PL-25324/workflow/CLAUDE.md`의 File-based Planning Workflow를 에이전트 무관한 자연어로 전환하여 AGENTS.md를 작성하고, CLAUDE.md/GEMINI.md를 symlink으로 연결한다.

## Requirements

1. AGENTS.md: 에이전트 무관 공통 워크플로우 (Single Source of Truth)
2. CLAUDE.md, GEMINI.md: AGENTS.md symlink
3. README.md: 개발자 온보딩 + 에이전트별 플러그인 설치 가이드
4. templates/ 정비: Phase 4(11-관점 검토), Phase 5 추가
5. Jira 티켓 연동: description fetch/push + `PLANNING_START/END` 직렬화

## Critical Files

### New Files

- `AGENTS.md` - 공통 워크플로우 (핵심 산출물)
- `CLAUDE.md` → AGENTS.md symlink
- `GEMINI.md` → AGENTS.md symlink
- `README.md` - 개발자 온보딩 가이드

### Modified Files

- `templates/tasks.md` - Phase 4/5 추가
- `templates/findings.md` - Review Findings 섹션 추가
- `templates/progress.md` - Review Log 섹션 추가

### Reference Files

- `.planning/PL-25324/workflow/CLAUDE.md` - 원본 (변환 소스)
- `.planning/PL-25324/workflow/spec.md` - 요구사항 명세
- `records/tasks.md` - 실제 사용 사례 (PL-24646)

## Architecture

### 파일 참조 구조

```text
CLAUDE.md ──symlink──→ AGENTS.md ←──symlink── GEMINI.md
                          │
                          │ 참조
                          ▼
                      templates/
                   ├── tasks.md
                   ├── findings.md
                   └── progress.md
                          │
                          │ 복사하여 생성
                          ▼
                   .planning/{티켓번호}/
                   ├── tasks.md
                   ├── findings.md
                   └── progress.md
```

### 전환 흐름

```text
1. .planning/PL-25324/workflow/CLAUDE.md (원본, Claude 전용)
       ↓ 자연어 전환
2. AGENTS.md (에이전트 무관)
       ↓ symlink
3. CLAUDE.md, GEMINI.md (각 에이전트 자동 로딩)
```

## Implementation Steps

### Step 1: AGENTS.md 작성

.planning/PL-25324/workflow/CLAUDE.md를 기반으로 자연어 전환:
- Claude-specific 표현 → 자연어 지시문 (매핑 테이블 참조)
- 경로 `.claude/docs/{브랜치}/` → `.planning/{티켓번호}/`
- 프롬프트 컨벤션 섹션 추가

### Step 2: Symlink 생성

```bash
ln -s AGENTS.md CLAUDE.md
ln -s AGENTS.md GEMINI.md
```

### Step 3: 템플릿 정비

- templates/tasks.md: Phase 4 → Multi-perspective Review (11-관점), Phase 5 → Final Gate & Delivery
- templates/findings.md: Review Findings 섹션 + 테이블 추가
- templates/progress.md: Review Log 섹션 + 테이블 추가

### Step 4: README.md 작성

- 소개, 빠른 시작, 파일 구조
- 에이전트별 설정 (Claude Code, Codex, Gemini)
- 플러그인 설치 가이드
- 워크플로우 요약, 프롬프트 컨벤션

### Step 5: Jira 티켓 연동 (스크립트 기반)

- `scripts/jira-sync.py` 스크립트 작성 (pull/push 서브커맨드)
  - `pull`: Jira API로 description fetch → `PLANNING_START`~`PLANNING_END` 파싱 → 로컬 파일 생성
  - `push`: 로컬 파일 직렬화 → 기존 description 보존 + planning 영역만 교체 (멱등성)
- 환경 변수: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- AGENTS.md에 스크립트 실행 기반 연동 절차 문서화 (에이전트 직접 접근 금지)

## Verification

### 검증 항목

```bash
# symlink 동작 확인
cat CLAUDE.md   # AGENTS.md 내용 출력
cat GEMINI.md   # AGENTS.md 내용 출력

# Claude 고유 용어 잔존 검사
grep -i "oh-my-claudecode\|OMC\|PreToolUse\|architect 에이전트\|\.claude/docs" AGENTS.md

# 완전성: .planning/PL-25324/workflow/CLAUDE.md 핵심 내용 포함 여부
# - 5-Phase, 3-File Pattern, 11-관점 검토, 핵심 규칙 8가지, 세션 복구

# Jira 연동 검증
# - jira-sync.py pull 실행 시 planning 파일 복원 성공
# - jira-sync.py push 실행 시 기존 description 보존 + planning 영역만 업데이트
# - 멱등성: 동일 내용 반복 push 시 결과 동일
```

## Considerations

### 기존 코드 재사용

- .planning/PL-25324/workflow/CLAUDE.md의 내용 중 에이전트 무관한 부분(해결하는 문제, 5-Phase, 11-관점, 핵심 규칙 등)은 그대로 재사용
- templates/의 기존 구조를 최대한 유지하고 누락 섹션만 추가

### 호환성

- symlink은 git이 추적 가능하므로 클론 시 유지됨
- Windows에서 symlink 미지원 시 README.md에 수동 복사 안내
<!-- LAST_SYNC: 2026-02-22 19:52:50 KST -->
