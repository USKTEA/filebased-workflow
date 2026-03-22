# Phase 5: Multi-perspective Review (9 Perspectives)

After implementation, review from 9 different perspectives.
Not "a general review of everything" — perform a focused pass for each perspective individually.

## Prerequisites

1. Confirm branch name and ticket number with `git branch --show-current`
2. Verify `.planning/{ticket}/current-phase` is `5`
3. Read `.planning/{ticket}/{branch}/tasks.md` to check the current state

## Review Table

| Step | Perspective              | Type       | Question                                                                          |
|------|--------------------------|------------|-----------------------------------------------------------------------------------|
| 1    | Purpose alignment        | Functional | Does the implementation match the original purpose?                               |
| 2    | Bugs/Security            | Safety     | Are there potential bugs or security issues?                                      |
| 3    | Impact & side effects    | Scope      | Do the changes create new problems or affect other modules?                       |
| 4    | Code structure & quality | Quality    | Dead code, duplication, oversized functions, consolidation opportunities?         |
| 5    | User flow (UX)           | Usability  | Are there any issues from the user's perspective?                                 |
| 6    | Chain review             | Iterative  | Do the fixes create new problems?                                                |
| 7    | Abstraction level audit  | Abstraction| Are there raw/low-level APIs where the framework provides higher-level alternatives? |
| 8    | Ownership check          | Learning   | Can I explain the 3 most important design decisions in this code?                 |
| 9    | Implicit assumption audit| Assumption | What infrastructure/environment assumptions does this code require to work?       |

## AI-Generated Code Review Notes

Steps 7-9 are specifically designed for reviewing AI-generated code. The key principle: **developer answers FIRST, then AI supplements.**

- **Step 7**: Ask the developer first: "이 구현에서 raw/low-level API를 쓴 부분이 있다면, 더 나은 대안이 있다고 생각하시나요?" After the developer answers, AI analyzes and reveals any additional alternatives the developer missed. Missed alternatives → Question Log as learning debt.
- **Step 8**: The developer themselves must answer: "이 코드의 가장 중요한 설계 결정 3개를 설명해주세요." If unable to answer, register as learning debt in findings.md Question Log.
- **Step 9**: Ask the developer first: "이 코드가 작동하려면 어떤 인프라/환경 전제가 필요한가요? 3개 먼저 말씀해주세요." After the developer answers, AI reveals any additional assumptions the developer missed. Missed assumptions → Question Log as learning debt.

## Chain Review Termination

Repeat until no more issues are found.
If new issues continue to appear after 3 iterations, escalate to the user.

## Recording Findings

Record all review findings in `findings.md` → Review Findings table:

| Review Perspective | Finding | Action |
|-------------------|---------|--------|

Also update the `progress.md` → Review Log section.

## Phase Gate

After all 9 perspective reviews are complete, present the results to the user and wait for approval.
**Do not proceed to the next Phase before approval.**
