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

`phase-guard.sh` 훅이 모든 Write/Edit/Bash 호출에서 실행되어, 현재 Phase에서 허용되지 않는 파일 수정을 차단합니다.

| Phase | `.planning/**` | `src/test/**` | `src/main/**` | Other |
|-------|----------------|---------------|---------------|-------|
| 1, 2, 5, 6 | ✅ | ❌ | ❌ | ❌ |
| 3 (ATDD) | ✅ | ✅ | ❌ | ❌ |
| 4 (구현) | ✅ | ✅ | ✅ | ✅ |

---

## 빠른 시작

```
/start-work PL-12345
```

1. Phase 1: 개발자 설계 질문 → 코드베이스 분석 → Reverse Interview → 계획 수립 → 3중 검토
2. Phase 2: `.planning/PL-12345/` 하위에 6개 planning 파일 자동 생성
3. Phase 3: spec.md 기반 인수 테스트 생성 (Red 상태 허용)
4. Phase 4: 인수 테스트를 통과시키는 구현
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
| 3 | ATDD 인수 테스트 | `/generate-acceptance-tests` | spec.md 기반 인수 테스트 작성 (Red 허용) |
| 4 | 구현 | `/implement` | 인수 테스트를 통과시키는 구현 + Discovery Report |
| 5 | 다층 검토 | `/review` | 9개 관점 순차 검토 (7~9는 AI 코드 전용) |
| 6 | 최종 게이트 | `/deliver` | 배포 준비도 평가, 커밋, PR |

**Phase 전환:** `/advance-phase` | **세션 복구:** `/resume` | **테스트 검증:** `/verify-acceptance-tests`

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
| **설계 질문** | 1 | AI 분석 전에 개발자 판단을 먼저 기록 (Anchoring Bias 방지) |
| **인수 조건 작성** | 3 | 테스트 코드 생성 전에 개발자가 직접 인수 조건 정의 |
| **Explain Checkpoint** | 4 | 복잡한 로직 구현 후 "이 코드가 뭘 하는지 설명해보세요" |
| **Discovery Report** | 4 | 재사용한 메서드, 새로 도입한 패턴 공유 |
| **Why Review** | 4→5 | 핵심 결정 + 질문 이력을 학습 부채로 관리 |
| **소유권 확인** | 5 | "핵심 설계 결정 3개를 설명해보세요" |
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

---

## 참고 문서

- [CLAUDE.md](CLAUDE.md) - 워크플로우 규칙 (에이전트가 읽는 SSoT)
- [.claude/commands/](.claude/commands/) - Phase별 슬래시 커맨드
- [.claude/templates/](.claude/templates/) - planning 파일 템플릿