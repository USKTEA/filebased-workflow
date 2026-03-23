# File-based Planning Workflow

파일 시스템을 AI 에이전트의 영구 메모리로 활용하고, ATDD(Acceptance Test-Driven Development)와 Review-Driven Development로 품질을 보장하는 워크플로우입니다.

## 소개

### 이 워크플로우란?

AI 에이전트와 협업할 때 발생하는 고질적인 문제들을 해결하기 위한 파일 기반 작업 관리 방식입니다.

> 이 워크플로우는 [ahastudio/file-based-planning-workflow](https://github.com/ahastudio/file-based-planning-workflow)를 참고하여 만들었습니다.

### 해결하는 문제

| 문제 | 해결 방법 |
|------|-----------|
| AI가 컨텍스트를 잃으면 목표·이력 모두 사라짐 | planning 파일이 영구 메모리 + tasks.md가 북극성 |
| 머릿속 요구사항이 구체화되지 않은 채 구현에 들어감 | spec.md로 요구사항·제약·성공기준·시나리오를 사전 확정 |
| 자기 검토가 피상적이고 관점이 획일적임 | 4단계 계획 검토 + 9개 관점 다층 검토 |
| 구현 코드가 스펙을 실제로 만족하는지 확인이 안 됨 | ATDD 인수 테스트가 스펙 충족을 자동 검증 |
| "이 코드 왜 이렇게 짰지?" 맥락이 없음 | findings.md에 의사결정 근거와 시행착오 기록 |
| AI가 짠 코드를 개발자가 이해 못 한 채 넘어감 | Delta Log + Question Log + Why Review로 학습 부채 관리 |

---

## v2 변경 사항 (v1 → v2)

### 아키텍처: Agent Skills → Claude-only 3-Layer Architecture

v1에서는 멀티에이전트 지원을 위해 Agent Skills 방식을 사용했습니다:
- `.agents/skills/` 디렉토리에 각 phase별 Skills 정의
- `AGENTS.md`를 중앙 규칙 저장소로 사용
- `CLAUDE.md`, `GEMINI.md` → `AGENTS.md` symlink로 다중 에이전트 지원

v2는 **Claude-only 아키텍처**로 전환하여 단순화했습니다:
- **3-Layer Enforcement**: Rules (CLAUDE.md) → Procedures (.claude/commands/) → Enforcement (.claude/hooks/)
- `CLAUDE.md`: 워크플로우 규칙 (Single Source of Truth, symlink 아님)
- `.claude/commands/*.md`: Phase별 슬래시 커맨드 절차서
- `.claude/hooks/*.sh`: 파일 수정 차단 기술적 강제 (phase-guard.sh, completion-check.sh)
- 삭제됨: `.agents/`, `AGENTS.md`, `GEMINI.md`, `.gemini/`, `.claude/skills/` symlinks

### 6 Phase 아키텍처 (5 → 6 Phase)

v1: 5 Phase (Plan → Files → Implement → Review → Deliver)

v2: 6 Phase (Plan → Files → **ATDD Tests** → Implement → Review → Deliver)

**새로운 Phase 3: ATDD 인수 테스트**
- spec.md 기반으로 인수 테스트를 **구현 전에 작성** (Red 상태 허용)
- 비즈니스 로직은 실제 DB/서비스로 테스트 (Mock 금지)
- 컴파일 에러는 의도적이며 Phase 4에서 해결

### 검토 관점: 11 → 9 (간소화)

v1: 11개 관점

v2: 9개 관점 (1~6: 일반 코드, 7~9: AI 생성 코드 전용)
- 1~6: 통상적 코드리뷰 관점 (가독성, 성능, 보안 등)
- 7~9: AI 코드 특화 관점 (소유권 확인, 암묵적 가정 감시, 추상화 수준)

### Phase Guard Hook (기술적 강제)

v1: 프롬프트 기반 규칙만 존재

v2: `phase-guard.sh` 훅이 모든 Write/Edit/Bash 호출을 감시하여 **파일 수정 차단**
- Phase 1,2,5,6: `.planning/**` 만 수정 가능 (나머지 차단)
- Phase 3 (ATDD): `.planning/**` + `src/test/**` 수정 가능
- Phase 4 (구현): 모든 파일 수정 가능
- 자체 보호: `.claude/hooks/**` 파일은 워크플로우 중 수정 불가

### Reverse Interview 강화 (Phase 1)

v1: 기본 interview

v2: 구조화된 6단계 프로세스
1. 개발자 설계 질문 (Anchoring Bias 방지)
2. AI 코드베이스 분석
3. Domain Context 수집 (제약 질문 전에)
4. 비즈니스 로직 검증
5. 5개 제약 차원 선택 (Concurrency, Failure, State, Volume, Security)
6. Interview 실행

### 개발자 학습 지원 (신규)

v1: planning 파일만으로 기본 지원

v2: 명시적 학습 메커니즘
- **Delta Log**: 개발자 판단 vs AI/최종 판단 차이 추적
- **Question Log**: Phase 중 개발자 질문을 findings.md에 기록, Why Review에서 학습 부채로 전환
- **Why Review**: Phase 4→5 게이트에서 핵심 결정 + 질문 이력 표면화
- **Explain Checkpoint**: 복잡 로직 구현 후 개발자 설명 요청
- **Discovery Report**: 재사용 메서드, 새 패턴 공유
- **소유권 확인**: "핵심 설계 결정 3개를 설명해보세요"

### 슬래시 커맨드 (신규)

v1: Agent Skills로 자동 로드

v2: 명시적 슬래시 커맨드
- `/start-work`: Phase 1 시작
- `/generate-files`: Phase 2 실행
- `/generate-acceptance-tests`: Phase 3 실행
- `/implement`: Phase 4 실행
- `/review`: Phase 5 실행
- `/deliver`: Phase 6 실행
- `/advance-phase`: Phase 전환 (사용자 승인 후)
- `/resume`: 세션 복구
- `/verify-acceptance-tests`: 테스트 검증

### 자동 활성화 패턴

v1: 프롬프트 감지로 `AGENTS.md` 로드

v2: 명시적 slash command 패턴 감지
- `PL-XXXXX 작업 시작` → `/start-work` 자동 실행
- `PL-XXXXX 이어서` / `현황` → `/resume` 자동 실행
- `PL-XXXXX 검토 시작` → `/review` 자동 실행

### 제거된 기능

- Jira 양방향 동기화 (별도 프로젝트로 분리 가능)
- CodeRabbit 자동 리뷰 참조 (수동 리뷰로 단순화)
- 멀티에이전트 지원 (Claude-only로 최적화)
- symlink 의존성 (프로젝트 복사 시 이점 증가)

---

### 핵심 철학: 계획 4단계 + 테스트 1단계 + 구현 1단계 + 검토 9단계

```
Phase 1: 계획 수립 및 검증 (6스텝)  ─── 계획을 세우고, 세 번 검토한다
Phase 2: Planning Files 생성        ─── 영구 메모리를 준비한다
Phase 3: ATDD 인수 테스트 작성      ─── 스펙에서 테스트를 먼저 만든다
Phase 4: 구현 (1단계)              ─── 테스트를 통과시키는 구현을 한다
Phase 5: 다층 검토 (9관점)         ─── 9개 관점으로 검토한다
Phase 6: 최종 게이트 및 배포        ─── 배포 수준인지 최종 확인한다
```

에이전트에게 구현은 쉽고, **올바른 구현**이 어렵습니다. 이 비율이 이 워크플로우의 철학입니다.

---

## 3-Layer Enforcement Architecture

단순히 "이렇게 해라"는 프롬프트만으로는 에이전트가 규칙을 무시합니다. 이 워크플로우는 3개 레이어로 규칙을 강제합니다:

| Layer | Location | Role |
|-------|----------|------|
| **Rules** | `CLAUDE.md` | WHY & WHAT — 워크플로우 규칙 정의 |
| **Procedures** | `.claude/commands/*.md` | HOW — Phase별 상세 절차 (슬래시 커맨드) |
| **Enforcement** | `.claude/hooks/*.sh` | BLOCK — Phase별 파일 수정 차단 (기술적 강제) |

### Phase Guard

`phase-guard.sh` 훅이 모든 Write/Edit/Bash 호출에서 실행되어, 현재 Phase에서 허용되지 않는 파일 수정을 차단합니다. 이는 단순한 프롬프트 규칙을 넘어 **기술적으로 강제**되는 메커니즘입니다.

| Phase | `.planning/**` | `src/test/**` | `src/main/**` | Other |
|-------|----------------|---------------|---------------|-------|
| 1, 2, 5, 6 | ✅ | ❌ | ❌ | ❌ |
| 3 (ATDD) | ✅ | ✅ | ❌ | ❌ |
| 4 (구현) | ✅ | ✅ | ✅ | ✅ |

Blocked 수정 시도는 exit 2 에러로 반환되며, `current-phase` 파일이 없으면 모든 수정이 허용됩니다 (비워크플로우 모드).

---

## 빠른 시작

```
/start-work PL-12345
```

1. Phase 1: 개발자 설계 질문 → 코드베이스 분석 → Reverse Interview → 계획 수립 → 3중 검토
2. Phase 2: `.planning/PL-12345/` 하위에 6개 planning 파일 자동 생성
3. Phase 3: spec.md 기반 인수 테스트 생성 (Red 상태 허용)
4. Phase 4: 인수 테스트를 통과시키는 구현 + Discovery Report
5. Phase 5: 9개 관점 다층 검토 + Why Review
6. Phase 6: 배포 준비도 평가 → 커밋 & PR

**추가 설정 없이 바로 시작할 수 있습니다.**

---

## 파일 구조

```
CLAUDE.md                          ← 워크플로우 규칙 (Single Source of Truth)
.claude/
  commands/                        ← Phase별 슬래시 커맨드
    start-work.md                  ← /start-work (Phase 1)
    generate-files.md              ← /generate-files (Phase 2)
    generate-acceptance-tests.md   ← /generate-acceptance-tests (Phase 3)
    implement.md                   ← /implement (Phase 4)
    review.md                      ← /review (Phase 5)
    deliver.md                     ← /deliver (Phase 6)
    advance-phase.md               ← /advance-phase (Phase 전환)
    resume.md                      ← /resume (세션 복구)
    verify-acceptance-tests.md     ← /verify-acceptance-tests (테스트 검증)
  hooks/                           ← 기술적 강제 훅
    phase-guard.sh                 ← Phase별 파일 수정 차단
    completion-check.sh            ← 미완료 Phase 경고
  templates/                       ← planning 파일 템플릿
    spec.md / plan.md / tasks.md / findings.md / progress.md / README.md
  settings.local.json              ← 훅 설정
.planning/                         ← 작업별 planning 파일 (자동 생성)
  {티켓번호}/
    current-phase                  ← 현재 Phase 번호 (1~6)
    {브랜치명}/
      spec.md / plan.md / tasks.md / findings.md / progress.md / README.md
```

---

## 워크플로우 요약

| Phase | 단계명 | 슬래시 커맨드 | 설명 |
|-------|--------|---------------|------|
| 1 | 계획 수립 및 검증 | `/start-work` | 설계 질문 → 분석 → Reverse Interview → 계획 → 3중 검토 |
| 2 | Planning Files 생성 | `/generate-files` | 6개 planning 파일 자동 생성 |
| 3 | ATDD 인수 테스트 | `/generate-acceptance-tests` | spec.md 기반 인수 테스트 작성 (Red 허용, Mock 금지) |
| 4 | 구현 | `/implement` | 인수 테스트를 통과시키는 구현 + Discovery Report |
| 5 | 다층 검토 | `/review` | 9개 관점 순차 검토 (7~9는 AI 코드 특화) + Why Review |
| 6 | 최종 게이트 | `/deliver` | 배포 준비도 평가, 커밋, PR |

**Phase 전환:** `/advance-phase` | **세션 복구:** `/resume` | **테스트 검증:** `/verify-acceptance-tests`

---

## 슬래시 커맨드 상세

### Phase 커맨드

#### `/start-work {ticket}` — Phase 1: 계획 수립 및 검증

6단계 Spec-Driven Planning을 실행합니다:

1. **개발자 설계 질문**: AI 분석 전에 개발자에게 3개의 설계 판단 질문 → Delta Log에 기록
2. **AI 코드베이스 분석**: 아키텍처 분석 → spec.md 초안 작성 (Happy Path)
3. **Reverse Interview**: 도메인 컨텍스트 확인 → 비즈니스 로직 검증 → 5개 제약 차원(동시성, 장애격리, 상태일관성, 부하, 보안) 중 관련 차원 선택 → 차원별 3~5개 질문
4. **계획 수립**: spec.md 확정 → plan.md 작성
5. **Meta-Review**: 리뷰의 리뷰 (AI 확증 편향 완화)
6. **과설계 검토**: YAGNI 위반, 불필요한 추상화 점검

#### `/generate-files` — Phase 2: Planning Files 생성

`.planning/{ticket}/{branch}/` 하위에 6개 파일을 템플릿 기반으로 생성합니다:
`spec.md`, `plan.md`, `tasks.md`, `findings.md`, `progress.md`, `README.md`

#### `/generate-acceptance-tests` — Phase 3: ATDD 인수 테스트

1. **개발자 인수 조건 작성**: AI 테스트 생성 전에 개발자가 자연어로 인수 조건 3개 이상 작성 → Delta Log에 기록
2. **Spec 추출**: spec.md에서 시나리오, 인수 조건, FR, CON, EC, API 스펙 추출
3. **테스트 코드 생성**: 실제 DB/서비스 기반 통합 테스트 (Mock 금지, 컴파일 에러 허용)

#### `/implement` — Phase 4: 구현

인수 테스트를 통과시키는 구현을 수행합니다:
- **Read Before Act**: 파일 수정 전 반드시 tasks.md 확인 → `[Phase 4] {요약} - tasks.md verified` 접두사 필수
- **2-Action Rule**: 조회 2회마다 findings.md에 기록
- **3-Strike Error Protocol**: 같은 에러 3회 실패 시 사용자에게 에스컬레이션
- **Explain Checkpoint**: 복잡 로직 구현 후 개발자 설명 요청
- **Discovery Report**: 재사용 메서드, 새 패턴 보고

#### `/review` — Phase 5: 다층 검토 (9관점)

9개 관점에서 **순차적으로** 검토합니다 (일괄 검토 아님):

| # | 관점 | 유형 |
|---|------|------|
| 1 | 목적 부합 | 기능 |
| 2 | 버그/보안 | 안전 |
| 3 | 영향 범위/부작용 | 스코프 |
| 4 | 코드 구조/품질 | 품질 |
| 5 | 사용자 흐름 (UX) | 사용성 |
| 6 | Chain Review | 반복 |
| 7 | 추상화 수준 감사 | AI 코드 |
| 8 | 소유권 확인 | AI 코드 |
| 9 | 암묵적 가정 감사 | AI 코드 |

7~9번은 **개발자 먼저 답변 → AI 보완** 순서로 진행되며, 놓친 부분은 Question Log에 학습 부채로 등록합니다.

#### `/deliver` — Phase 6: 최종 게이트 및 배포

- 배포 준비도 평가 (테스트 통과, tasks.md 완료 여부, progress.md 갱신)
- 커밋 메시지: `[{ticket}] 작업 요약`
- PR 생성 (변경 요약, 테스트 계획 포함)

### 유틸리티 커맨드

#### `/advance-phase`

현재 Phase를 완료하고 다음 Phase로 전환합니다:
- 현재 Phase의 모든 태스크 완료 확인
- 사용자 승인 필수 (자동 전환 불가)
- **Phase 4→5 전환 시**: Why Review 게이트 실행 (핵심 결정 + Question Log → 학습 부채로 전환)

#### `/resume {ticket} [이어서|현황]`

세션 복구:
- `이어서`: 중단된 Phase부터 작업 재개
- `현황`: 현재 진행 상태만 요약 보고
- tasks.md와 current-phase 교차 검증 → 불일치 시 사용자에게 보고

#### `/verify-acceptance-tests`

인수 테스트를 실행하고 실패 원인을 분류합니다:

| 분류 | 수정 대상 |
|------|-----------|
| 미구현 | 구현 코드 |
| Assertion 에러 | 테스트 코드 |
| 타입/컴파일 에러 | 테스트 코드 |
| 로직 에러 | 구현 코드 |
| 스펙 모호 | 사용자에게 확인 |

---

## 프롬프트 컨벤션

| 프롬프트 | 동작 |
|----------|------|
| `/start-work PL-12345` | 새 작업 시작 |
| `/resume PL-12345 이어서` | 세션 복구 (중단된 Phase부터 재개) |
| `/resume PL-12345 현황` | 현재 진행 상태 확인 |
| `/advance-phase` | 다음 Phase로 전환 (사용자 승인 후) |

---

## 개발자 학습 지원

이 워크플로우는 AI가 코드를 대신 짜주는 것에서 끝나지 않고, 개발자의 성장을 돕습니다:

| 메커니즘 | Phase | 목적 |
|----------|-------|------|
| **개발자 설계 질문** | 1 | AI 분석 전에 개발자 판단을 먼저 기록 (Anchoring Bias 방지) |
| **인수 조건 정의** | 3 | 테스트 코드 생성 전에 개발자가 직접 인수 조건 작성 |
| **Explain Checkpoint** | 4 | 복잡한 로직 구현 후 "이 코드가 뭘 하는지 설명해보세요" |
| **Discovery Report** | 4 | 재사용한 메서드, 새로 도입한 패턴 공유 |
| **Why Review** | 4→5 | 핵심 결정 + 질문 이력을 학습 부채로 관리 |
| **소유권 확인** | 5 | "핵심 설계 결정 3개를 설명해보세요" |
| **Question Log** | 전체 | Phase 중 개발자 질문 기록 → 학습 부채로 관리 |
| **Delta Log** | 전체 | 개발자 판단 vs AI/최종 판단 차이 추적 |

---

## 다른 프로젝트에 적용하기

### 필수 파일

```bash
# 복사할 파일
CLAUDE.md
.claude/commands/*.md
.claude/hooks/*.sh
.claude/templates/*.md
.claude/settings.local.json
```

### 적용 순서

```bash
# 1. 파일 복사
cp -r source/.claude/ target/.claude/
cp source/CLAUDE.md target/CLAUDE.md

# 2. 훅 실행 권한
chmod +x target/.claude/hooks/*.sh

# 3. .gitignore에 추가
echo ".planning/" >> .gitignore

# 4. (선택) 프로젝트별 내용 추가
# CLAUDE.md에 빌드 명령어, 코딩 컨벤션 등을 추가하세요
```

### 옮기지 않아도 되는 것들

| 파일 | 이유 |
|------|------|
| `.planning/` | 프로젝트별 planning 데이터 (자동 생성) |
| `README.md` | 이 워크플로우 레포 자체의 설명서 |
| `records/` | 과거 이력 |
| `.agents/` | v1 아키텍처 (더 이상 사용 안 함) |
| `AGENTS.md` / `GEMINI.md` | v1 symlink (더 이상 사용 안 함) |

---

## 참고 문서

- [CLAUDE.md](CLAUDE.md) - 워크플로우 규칙 (에이전트가 읽는 SSoT)
- [.claude/commands/](.claude/commands/) - Phase별 슬래시 커맨드
- [.claude/templates/](.claude/templates/) - planning 파일 템플릿
- [.claude/hooks/](.claude/hooks/) - 기술적 강제 훅