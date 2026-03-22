# File-based Planning Workflow

A workflow that uses the filesystem as persistent memory for AI agents and ensures quality through ATDD (Acceptance Test-Driven Development) and Review-Driven Development. Plan in 4 steps, test from spec, implement to pass tests, review from 9 perspectives.

## 3-Layer Enforcement Architecture

| Layer | Location | Role |
|-------|----------|------|
| **Rules** | `CLAUDE.md` (this file) | WHY & WHAT — Workflow rule definitions |
| **Procedures** | `.claude/commands/*.md` | HOW — Per-phase detailed procedures (slash commands) |
| **Enforcement** | `.claude/hooks/*.sh` | BLOCK — Per-phase file modification blocking (technical enforcement) |

### Phase Guard (Hook-based Blocking)

`.claude/hooks/phase-guard.sh` runs on every Write/Edit/Bash tool call.
It reads `.planning/{ticket}/current-phase` and enforces per-phase path restrictions.

| Phase          | `.planning/**` | `src/test/**` | `src/main/**` | Other |
|----------------|----------------|---------------|---------------|-------|
| 1, 2, 5, 6    | ✅              | ❌             | ❌             | ❌     |
| 3 (ATDD)       | ✅              | ✅             | ❌             | ❌     |
| 4 (Implement)  | ✅              | ✅             | ✅             | ✅     |
| Inactive       | ✅              | ✅             | ✅             | ✅     |

Blocked modifications return exit 2 with an error message.
When `current-phase` file does not exist, all file modifications are allowed (non-workflow mode).

## Workflow Phases

| Phase | Name                    | Command                         |
|-------|-------------------------|---------------------------------|
| 1     | Planning & Verification | `/start-work`                   |
| 2     | Generate Planning Files | `/generate-files`               |
| **3** | **ATDD Acceptance Tests** | **`/generate-acceptance-tests`** |
| 4     | Implementation          | `/implement`                    |
| 5     | Multi-perspective Review | `/review`                      |
| 6     | Final Gate & Delivery   | `/deliver`                      |

Phase transition: `/advance-phase` | Session recovery: `/resume` | Test verification: `/verify-acceptance-tests`

### Automatic Activation

When a ticket pattern is detected, the workflow activates automatically:

| User Input Pattern             | Action                                                        |
|--------------------------------|---------------------------------------------------------------|
| `PL-XXXXX 작업 시작`           | Run `/start-work` → set `current-phase=1`                    |
| `PL-XXXXX 이어서` / `현황`     | Run `/resume` to recover session state                        |
| `PL-XXXXX 검토 시작`           | Run `/review`                                                 |

The phase-guard hook enforces file restrictions regardless of activation method.

## Core Rules

### 1. Plan First
Complex tasks (3+ steps) MUST create `tasks.md` first. Non-negotiable.

### 2. Triple Review
After planning: Review → Meta-review → Over-engineering check. Always.

### 3. 2-Action Rule
After every 2 lookup/search actions, save findings to `findings.md`.

### 4. Read Before Act (Absolute Rule)
Before modifying any file, you MUST read `tasks.md` first. Never rely on memory alone.

**Required trigger points:**
- Before modifying any file (code, config, docs)
- When starting a new Phase
- After 5+ consecutive actions (periodic reminder)
- When an error occurs (to avoid losing direction)

**Response prefix rule (Phase 4 only):**
After reading tasks.md, the first line of your response MUST state the current status:
```
[Phase 4] {current task summary} - tasks.md verified
```

### 5. Update After Act
Update Phase status: `⏸️ 대기` → `🔄 진행 중` → `✅ 완료`

### 6. Log ALL Errors
Record every error to `findings.md`. This prevents repeating the same mistakes.

### 6-1. Log Developer Questions
When the developer asks a question during any Phase (about patterns, concepts, APIs, architecture, etc.), record it in `findings.md` → `## Question Log` table. These are surfaced during the Why Review gate (Phase 4→5) and transferred to Obsidian as learning debt.

### 7. Multi-perspective Review
NOT "review everything generally" — review from each perspective individually. One lens per dimension enables deeper review.

### 8. 3-Strike Error Protocol
```
ATTEMPT 1: Diagnose & fix — analyze error, find root cause, targeted fix
ATTEMPT 2: Alternative approach — same error? try a different method
ATTEMPT 3: Full reconsider — question assumptions, search for solutions, consider plan revision
After 3 failures: Escalate to user
```

### 9. Phase Gate Rule (Hook-enforced)
At the end of each Phase, you MUST:
1. Present a summary of results to the user
2. Wait for user feedback
3. Proceed to the next Phase only after user approval via `/advance-phase`

Never auto-transition. The phase-guard hook blocks file modifications outside the current Phase's allowed paths.

### 10. ATDD Strict Rules (Phase 3)

Acceptance tests MUST be integration tests that verify end-to-end behavior. Mock-based unit tests are NOT acceptance tests.

- **No Mocks for Business Logic**: Mocking business logic dependencies is forbidden. Exception: non-business infrastructure (authentication, auditing, external APIs) may use mocks.
- **Required Stack**: Use real database connections and real service instances for acceptance tests.
- **Embrace Compile Errors**: In Phase 3, it is EXPECTED that tests may not compile because production code does not exist yet. Do NOT use mocks to bypass compile errors.
- **Existing Code Modification**: When production classes already exist, write compilable integration tests against them.
- **New Feature Development**: Accept compile-error state (Red) in Phase 3. Resolve in Phase 4 implementation.

## Planning Files

Location: `.planning/{ticket-number}/{branch-name}/`

```
spec.md       — Requirements specification
plan.md       — Implementation plan
tasks.md      — Task tracking (North Star)
findings.md   — Technical findings & decisions
progress.md   — Session-by-session work log
README.md     — Feature description (Background, Goal, How it works)
```

Templates: `.claude/templates/`

## Prompt Conventions

| Action | Format | Example |
|--------|--------|---------|
| Start work | `/start-work {ticket}` | `/start-work PL-12345` |
| Resume | `/resume {ticket} 이어서` | `/resume PL-12345 이어서` |
| Check status | `/resume {ticket} 현황` | `/resume PL-12345 현황` |
| Generate tests | `/generate-acceptance-tests` | `/generate-acceptance-tests` |
| Verify tests | `/verify-acceptance-tests` | `/verify-acceptance-tests` |
| Advance phase | `/advance-phase` | `/advance-phase` |
| Start review | `/review` | `/review` |

## When to Apply

**Use this workflow:**
- Multi-step tasks (3+ steps)
- Cross-module changes
- Research/investigation tasks
- New feature implementation

**Skip this workflow:**
- Simple Q&A
- Single-file edits
- Quick lookups