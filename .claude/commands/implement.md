# Phase 4: Implementation

Implementation is exactly **1 step** in the entire workflow.

## Prerequisites

1. Confirm branch name and ticket number with `git branch --show-current`
2. Verify `.planning/{ticket}/current-phase` is `4`
3. Read `.planning/{ticket}/{branch}/tasks.md` to check the current state

## Rules During Implementation

### Read Before Act (Absolute Rule)

**Before modifying any file, you MUST read `tasks.md` first.**

The first line of the response must be:
```
[Phase 4] {current task summary} - tasks.md verified
```

A response without this prefix is a rule violation.

### Required Trigger Points
- Before modifying any file
- After 5+ consecutive actions (periodic check)
- When an error occurs (to avoid losing direction)

### Update After Act

After completing work, update the Phase status: `⏸️ Pending` → `🔄 In Progress` → `✅ Complete`

### 2-Action Rule

After every 2 lookup/search actions, save findings to `findings.md`.
Do not accumulate only in memory.

### 3-Strike Error Protocol

```
Attempt 1: Diagnose & fix — analyze error, find root cause, targeted fix
Attempt 2: Alternative approach — same error? try a different method
Attempt 3: Full reconsider — question assumptions, search for solutions, consider plan revision
After 3 failures: Escalate to user
```

### Error Logging

Record all errors in `findings.md` → Issues Encountered section.

### Technical Findings

Record technical findings discovered during implementation immediately in `findings.md`.

## Code Quality Checklist

Review the project conventions in CLAUDE.md before implementation and follow these principles.

### Follow Existing Patterns
- Explore existing implementations in the same domain before writing new code and follow established patterns
- When introducing a new pattern, record the rationale in findings.md

### Prefer Higher-Level APIs
- Prefer type-safe APIs provided by the framework
- Raw/low-level APIs are only allowed when higher-level APIs cannot express the operation, and the reason must be documented

### Scope Verification
- Refer to the Data Structure Analysis table in spec.md to check whether implementation strategies differ per concrete type
- When the same operation applies to different data structures, design query paths independently for each

## Upon Completion

### Explain Checkpoint (Mid-Phase 4)

When AI implements complex logic, pause and ask the developer:

> **"이 코드가 뭘 하는지 자기 말로 설명해주세요."**

Purpose: Check understanding during implementation, not after.

Trigger conditions (any one):
- New pattern not previously used in the codebase
- 3+ nested control structures
- Complex database queries (aggregation, joins, etc.)
- Event/listener/callback chain spanning 2+ classes

If the developer cannot explain:
- Record in `findings.md` → `## Question Log`
- Continue implementation, but mark for Why Review

If the developer explains correctly:
- No action needed, continue

This is NOT a gate — do not block progress. It is a learning signal.

### Structural Test Augmentation

After all Phase 3 ATDD tests are Green, review the implementation code to find branches not covered by spec-based tests.

#### What to do

1. **Scan branches**: Identify conditionals and error handling in the implementation
2. **Compare with Phase 3 tests**: Find branches that no existing test exercises
3. **Add tests for uncovered branches**: In the same test class under a structural tests group
4. **Loop boundaries**: If loops are involved, test with 0, 1, and N iterations
5. **Spec back-tracking**: If an uncovered path reveals a missed requirement, add it as an acceptance test

#### What to cover vs skip

| Cover (business value) | Skip (noise) |
|------------------------|--------------|
| Business condition branches | Simple null checks |
| Error handling with different behavior per branch | Getter / setter / DTO mapping |
| State transition branches | Logging / auditing branches |
| Fallback / default branches with side effects | Framework-generated code |

### Discovery Report (MUST — after implementation, before verification)

After implementation is complete, present the developer with a discovery report:

1. **Reused Methods**: List all existing methods/classes that AI reused during implementation
   > "구현 중 다음 기존 메서드를 재사용했습니다. 이 중 몰랐던 것이 있나요?"

2. **New Patterns Introduced**: List any patterns used for the first time in this codebase
   > "이번 구현에서 새로 도입된 패턴입니다. 왜 이 패턴이 필요한지 설명할 수 있나요?"

3. **Why Review**: Ask the developer:
   > "이번 구현에서 AI가 한 것 중, 직접 했으면 다르게 했을 부분이 있나요?"

Record discoveries in `findings.md` → `## Delta Log` section. Unknown methods or unexplainable patterns go to `## Question Log` as learning debt.

**Purpose**: Recreates the "accidental discovery" that happens naturally when coding manually.

### Verification

1. Run tests
2. Run lint/format checks
3. Update tasks.md

## Phase Gate

After implementation is complete, present the results to the user and wait for approval.
**Do not proceed to the next Phase before approval.**
