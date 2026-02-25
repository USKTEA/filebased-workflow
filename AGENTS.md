# File-based Planning Workflow

A workflow that uses the filesystem as persistent memory for AI agents and ensures quality through Review-Driven Development. Agents are good at implementation but struggle to judge whether their implementation is appropriate. This workflow compensates: plan in 4 steps, implement in 1, review from 11 perspectives.

## Workflow Phases

| Phase | Name | Summary |
|-------|------|---------|
| 1 | Planning & Verification | Plan → Review → Meta-review → Over-engineering check |
| 2 | Generate Planning Files | Create 6 files in `.planning/{ticket}/{branch}/` |
| 3 | Implementation | Implement according to plan (exactly 1 step) |
| 4 | Multi-perspective Review | Review from 11 different perspectives |
| 5 | Final Gate & Delivery | Deploy readiness assessment + commit/PR |

Phase-specific instructions are loaded automatically via Agent Skills when entering each phase.

## Core Rules

### 1. Plan First
Complex tasks (3+ steps) MUST create `tasks.md` first. Non-negotiable.

### 2. Triple Review
After planning: Review → Meta-review → Over-engineering check. Always.

### 3. 2-Action Rule
After every 2 lookup/search actions, save findings to `findings.md`.

### 4. Read Before Act (Absolute Rule)
Before using ANY tool (terminal, file edit, etc.), you MUST read `tasks.md` first to check the latest state. Never rely on memory alone — always re-read the file.

**Required trigger points:**
- Before modifying any file (code, config, docs)
- When starting a new Phase
- After 5+ consecutive actions (periodic reminder)
- When an error occurs (to avoid losing direction)

**Response prefix rule:**
After reading tasks.md, the first line of your response MUST state the current status:
```
[Phase N] {current task summary} - tasks.md verified
```
Failure to include this prefix will result in immediate user interruption and rollback.

### 5. Update After Act
Update Phase status after completion: `pending` → `in_progress` → `complete`

### 6. Log ALL Errors
Record every error. This prevents repeating the same mistakes.

### 7. Multi-perspective Review
NOT "review everything generally" — review from each perspective individually. One lens per dimension enables deeper review.

### 8. 3-Strike Error Protocol
```
ATTEMPT 1: Diagnose & fix — analyze error, find root cause, targeted fix
ATTEMPT 2: Alternative approach — same error? try a different method
ATTEMPT 3: Full reconsider — question assumptions, search for solutions, consider plan revision
After 3 failures: Escalate to user
```

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

## Prompt Conventions

| Action | Format | Example |
|--------|--------|---------|
| Start work | `{ticket} 작업 시작` | `PL-12345 작업 시작` |
| Resume | `{ticket} 이어서` | `PL-12345 이어서` |
| Resume phase | `{ticket} Phase {N} 재개` | `PL-12345 Phase 3 재개` |
| Start review | `{ticket} 검토 시작` | `PL-12345 검토 시작` |
| Check status | `{ticket} 현황` | `PL-12345 현황` |

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
