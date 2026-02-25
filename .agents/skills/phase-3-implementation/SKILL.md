---
name: phase-3-implementation
description: >
  Implementation phase rules and guidelines. Activate when coding, implementing
  features, modifying source files, or entering Phase 3 of the workflow.
  구현, 코딩, 개발, Phase 3 진입 시 활성화.
---

# Phase 3: Implementation

Implementation is exactly ONE step in the entire workflow.

## Rules During Implementation

- **Before modifying files**: Read `tasks.md` first.
  Start response with: `[Phase N] {summary} - tasks.md verified`
- **After modifying files**: Update progress in `tasks.md`
- **On error**: Immediately log to `findings.md` → Issues Encountered section
- **On technical discovery**: Immediately log to `findings.md`
- **After 5 consecutive actions**: Re-read `tasks.md` to confirm direction
- **On completion**: Write and run tests

## Response Prefix (Mandatory)

After reading tasks.md, the first line of EVERY response MUST be:
```
[Phase N] {current task summary} - tasks.md verified
```
A response without this prefix is a rule violation. The user may immediately stop work upon finding a response without the prefix.

## 3-Strike Error Protocol

```
ATTEMPT 1: Diagnose & fix — analyze error, find root cause, targeted fix
ATTEMPT 2: Alternative approach — same error? try a different method
ATTEMPT 3: Full reconsider — question assumptions, search for solutions
After 3 failures: Escalate to user
```

## 2-Action Rule

After every 2 lookup/search actions, save findings to `findings.md`. Do not accumulate findings only in memory.
