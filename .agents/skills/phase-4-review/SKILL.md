---
name: phase-4-review
description: >
  Multi-perspective review from 11 different viewpoints after implementation.
  ALWAYS activate when user prompts "{ticket} 검토 시작" or when entering Phase 4.
  NOT "review everything generally" — each perspective gets its own focused pass.
  검토, 리뷰, Phase 4 진입 시 활성화.
---

# Phase 4: Multi-perspective Review (11 Perspectives)

After implementation, review from different perspectives. Each lens focuses on exactly one dimension for deeper review.

## Review Table

| Step | Perspective | Type | Question |
|------|------------|------|----------|
| 1 | Purpose alignment | Functional | Does the implementation match the original purpose? |
| 2 | Bugs, security, critical | Safety | Are there potential bugs or security issues? |
| 3 | Improvement side effects | Change impact | Do improvements introduce new problems? |
| 4 | Function/file size | Structure | Should large functions/files be split? |
| 5 | Code integration/reuse | Deduplication | Can any parts be integrated with or reuse existing code? |
| 6 | Side effects | Impact scope | Do changes affect other modules? |
| 7 | Full diff review | Integration | Review the entire diff one more time |
| 8 | Dead code | Cleanup | Has any code become unnecessary during implementation? |
| 9 | Code quality | Quality gate | Is code quality sufficiently high? |
| 10 | User flow (UX) | Usability | Are there problems in the user's usage flow? |
| 11 | Chain review | Iterative | Do fixes from review create new problems? |

## Chain Review Termination

Repeat until no more issues are found. If new issues keep appearing after 3 iterations, escalate to user.

## Recording Findings

Record all review findings in `findings.md` → Review Findings table:

| Review Perspective | Finding | Action |
|-------------------|---------|--------|

Also update `progress.md` → Review Log section.
