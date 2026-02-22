# Findings & Decisions

> **기술적 발견, 중요한 결정이 있을 때마다 이 파일을 즉시 업데이트하세요.**

## Requirements

- AGENTS.md: 에이전트 무관 공통 워크플로우 (Single Source of Truth)
- CLAUDE.md, GEMINI.md: AGENTS.md symlink
- README.md: 개발자 온보딩 + 에이전트별 플러그인 안내
- templates/ 정비: Phase 4/5, Review 섹션 추가
- Jira 티켓 연동: description fetch/push + `PLANNING_START/END` 직렬화

## Research Findings

### 에이전트별 자동 로딩 파일명

| 에이전트       | 자동 로딩 파일                  | 비고             |
|----------------|--------------------------------|------------------|
| Claude Code    | CLAUDE.md                      | 프로젝트 루트    |
| OpenAI Codex   | AGENTS.md                      | 프로젝트 루트    |
| Google Gemini  | GEMINI.md                      | Gemini CLI       |
| GitHub Copilot | .github/copilot-instructions.md | 이번 스코프 제외 |

### CLAUDE.md 분석

Claude-specific 의존성 목록:
1. `/oh-my-claudecode:plan` 슬래시 커맨드
2. `architect` 에이전트 위임
3. `PreToolUse` 훅 (자동 tasks.md 리로드)
4. `.claude/docs/{브랜치}/` 경로 컨벤션
5. `OMC plan skill`, `OMC code-review` 도구 참조
6. `Purple 프로젝트` 특정 프로젝트명

에이전트 무관한 핵심 (그대로 재사용 가능):
- 해결하는 문제 (5가지)
- 5-Phase 워크플로우 구조
- 3-File Pattern (tasks.md, findings.md, progress.md)
- 11-관점 다층 검토 테이블
- 핵심 규칙 8가지
- 3-Strike Error Protocol
- 적용 기준
- 세션 복구 절차 (경로만 변경)

### 기존 templates/ 분석

| 템플릿      | 에이전트 무관 | 수정 필요                                                               |
|-------------|---------------|-------------------------------------------------------------------------|
| spec.md     | ✅            | 없음                                                                    |
| plan.md     | ✅            | 없음                                                                    |
| tasks.md    | ⚠️            | Phase 4가 Testing만 있음 → Multi-perspective Review 필요, Phase 5 없음 |
| findings.md | ⚠️            | Review Findings 섹션 없음 (records/에서는 이미 활용 중)                |
| progress.md | ⚠️            | Review Log 섹션 없음                                                   |
| README.md   | ✅            | 없음                                                                    |

## Resources

### 문서

- `.planning/PL-25324/workflow/CLAUDE.md` - 원본 Claude 전용 워크플로우
- `.planning/PL-25324/workflow/spec.md` - 이 프로젝트 요구사항
- `records/` - PL-24646 실제 사용 사례

### 참고 자료

- [Spec-Driven Development](../../spec-driven-development.md)
- [File-based Planning Workflow](../../file-based-workflow.md)
- [Planning with Files 플러그인](../../planning-with-files.md)

## Technical Decisions

| Decision                           | Rationale                                                                                     |
|------------------------------------|-----------------------------------------------------------------------------------------------|
| AGENTS.md = Single Source of Truth | 여러 AI 에이전트가 공통으로 인식하는 파일명. Codex는 AGENTS.md를 자동 로딩                   |
| CLAUDE.md, GEMINI.md = symlink     | DRY 원칙. 내용 불일치 리스크 제거. git이 symlink 추적 가능                                   |
| Copilot 제외                       | .github/ 별도 디렉토리. symlink이 깔끔하지 않음. 추후 필요 시 추가                           |
| Jira 연동: 스크립트 기반           | 에이전트 직접 접근 금지. `jira-sync.py pull/push`로 안전하게 처리 (인증·파싱·멱등성 보장)     |
| 직렬화 형식: 영역+파일 구분자      | `PLANNING_START/END`로 기존 description 보존, `FILE: {파일명}`로 파일 분리. 스크립트가 멱등성 보장 |
| `.planning/{티켓번호}/` 경로       | `.claude/docs/`는 Claude 전용. `.planning/`은 숨김 디렉토리로 프로젝트 소스와 분리            |
| 에이전트별 팁은 README.md에        | AGENTS.md는 AI가 읽는 문서, README.md는 사람이 읽는 문서. 역할 분리                          |
| 한국어 유지                        | 팀 업무 언어. 영어 프롬프트 병기로 글로벌 참조 지원                                          |
| CLAUDE.md 원본 보존                | 원본 히스토리 가치. 변환 출처 명시                                                           |
| 클래식 토큰 + Basic Auth 채택      | 스코프 토큰(granular/classic)은 API Gateway에서 인증 불안정. 스코프 없는 클래식 토큰 + Basic Auth가 안정적으로 동작. Bearer Auth는 `JIRA_AUTH_METHOD=bearer`로 옵션 지원 |
| Auto-Routing 유지                  | cloudId를 `/_edge/tenant_info`에서 자동 취득. 환경변수 3개만 필요 (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`) |
| API v3 → v2 다운그레이드           | v3는 description에 ADF(Atlassian Document Format) JSON 필수. plain text 전송 시 400 에러. v2는 plain text 허용하여 마크다운 직접 전송 가능 |

## Issues Encountered

### 1. 스코프 토큰 인증 실패 (401/404)
**문제**: `id.atlassian.com`에서 발급한 스코프 토큰(granular: `read:issue:jira` 등, classic: `read:jira-work` 등)으로 API Gateway 호출 시 401 또는 404 발생
**해결**: 스코프 없는 클래식 토큰 + Basic Auth로 전환. `JIRA_AUTH_METHOD` 환경변수로 Bearer Auth 옵션 지원
**결과**: 성공. 스코프 없는 토큰 + Basic Auth가 안정적으로 동작

### 2. PLANNING_END 마커 내장으로 pull 파싱 실패
**문제**: spec.md 내용에 `=== PLANNING_END ===` 텍스트가 포함되어 있어 `index()`가 첫 번째(내장된) 마커를 찾아 파싱이 중단됨. spec.md만 pull되고 나머지 5개 파일 누락
**해결**: `index()` → `rindex()`로 변경하여 마지막(실제) END 마커를 사용. `parse_planning_section()`과 `replace_or_append_planning()` 두 곳 모두 수정
**결과**: 성공. 27개 테스트 전수 통과 (embedded marker 테스트 포함)

### 3. push 시 description 32,767자 제한 초과
**문제**: Jira description에 non-planning 콘텐츠(~21K chars) + planning 파일(~24K chars) = ~45K chars로 제한 초과
**해결**: non-planning 콘텐츠 정리 후 planning 콘텐츠만 ~24K chars로 제한 내 수용. 구조적으로는 description 크기 제한이 존재하므로 planning 파일 크기 관리 필요
**결과**: 성공. push 정상 동작 확인

## Review Findings

| 검토 관점 | 발견 사항 | 조치 |
|-----------|-----------|------|
| 목적 부합 | AGENTS.md에 CLAUDE.md 핵심 7개 요소 모두 포함. Claude 고유 용어 0건 (grep 전수 검사) | 조치 불필요 |
| 버그/보안/크리티컬 | jira-sync.py 경로 조작(CWE-22) CRITICAL, 티켓 입력값 미검증(CWE-20) HIGH | `validate_filename()`, `validate_ticket()` 추가, 에러 응답 200자 제한 |
| 사이드 이펙트 | symlink 동작 확인 완료 (CLAUDE.md → AGENTS.md, GEMINI.md → AGENTS.md) | 조치 불필요 |
| 코드 통합/재사용 | CLAUDE.md 대비 누락 0건. 6-File Pattern으로 확장, Rule 4 강화, Jira 연동 추가 | 조치 불필요 |
| 전체 변경 사항 통합 | README.md에 파일 구조 불완전(3개→6개), Phase 2 설명 불일치, Jira 스크립트 미언급 | README.md 3건 수정 완료 |
| 연쇄 검토 | 보안 수정 후 7개 단위 테스트 전수 통과. README 수정은 내용 추가만으로 부작용 없음 | 연쇄 문제 없음 |
| API 버전 검토 | API v3는 description에 ADF JSON 필수 → plain text push 시 HTTP 400 확정 | API v2로 다운그레이드. 9개 테스트 통과 |
| 인증 방식 검토 | 스코프 토큰(granular/classic) + Bearer/Basic Auth 모든 조합에서 401/404 발생 | 스코프 없는 클래식 토큰 + Basic Auth로 확정 |
| 파싱 견고성 검토 | spec.md 내용에 `PLANNING_END` 마커가 포함되어 `index()`가 잘못된 위치를 찾음 | `rindex()`로 변경하여 마지막 END 마커 사용. 테스트 추가 |
| 충돌 감지 검토 | 타임스탬프 기반 양방향 충돌 감지 구현. pull/push 시 파일별 최신 여부 비교 | 27개 테스트 전수 통과. `--force` 플래그로 강제 덮어쓰기 지원 |

## Learnings

### 에이전트 직접 Jira 접근은 실패한다 (2026-02-22)

Gemini 피드백으로 확인된 세 가지 실패 지점:
1. **인증 장벽**: AI 에이전트는 브라우저 세션을 공유하지 않아 사내 Jira에 접근 불가
2. **데이터 유실**: LLM이 `PLANNING_START~END`를 정확히 파싱/직렬화하는 것은 불안정 (환각, 실수로 기존 description 유실 위험)
3. **토큰 낭비**: Jira API 응답의 방대한 메타데이터가 컨텍스트를 잠식

해결: `scripts/jira-sync.py` 스크립트 기반으로 전환. 에이전트는 스크립트만 실행하고, 인증·파싱·멱등성은 스크립트가 보장.

### AGENTS.md가 공통 스펙 (2026-02-22)

AGENTS.md는 OpenAI Codex뿐 아니라 여러 AI 에이전트가 공통으로 읽는 파일명.
별도 CONVENTIONS.md를 만들 필요 없이 AGENTS.md 자체가 공통 컨벤션 역할을 하고,
CLAUDE.md, GEMINI.md는 symlink으로 연결하면 된다.

### 스코프 토큰은 API Gateway에서 불안정하다 (2026-02-22)

`id.atlassian.com`에서 발급한 스코프 토큰(granular, classic 모두)은 API Gateway(`api.atlassian.com`)에서 인증이 불안정하다.
Basic Auth + Bearer Auth 모든 조합, `read:issue:jira` + `write:issue:jira` 등 다양한 스코프 조합을 테스트했으나 401/404 발생.
스코프 없는 클래식 토큰 + Basic Auth가 유일하게 안정적으로 동작했다.
`JIRA_AUTH_METHOD=bearer` 옵션은 향후 스코프 토큰 호환성이 개선될 경우를 위해 유지한다.

### 파일 내용에 직렬화 마커가 포함될 수 있다 (2026-02-22)

spec.md 등 planning 파일의 내용에 `=== PLANNING_END ===` 같은 마커 텍스트가 예시로 포함될 수 있다.
`index()`는 첫 번째 매치를 찾으므로 파일 내용 속 마커를 실제 END 마커로 오인한다.
`rindex()`로 마지막 매치를 사용하면 실제 END 마커를 정확히 찾을 수 있다.
<!-- LAST_SYNC: 2026-02-22 19:52:50 KST -->
