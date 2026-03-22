# Phase 6: Final Gate & Delivery

## Prerequisites

1. Confirm branch name and ticket number with `git branch --show-current`
2. Verify `.planning/{ticket}/current-phase` is `6`
3. Read `.planning/{ticket}/{branch}/tasks.md` to confirm all Phases are complete

## Deploy Readiness Assessment

This is the final judgment synthesizing all reviews. Even if individual reviews pass, overall quality may not be at a deployable level.

- Is the quality sufficient to deploy in the current state?
- Do all tests pass?
- Has the session work log been updated in `progress.md`?
- Are all Phases in `tasks.md` marked ✅ complete?

## Commit Convention

Commit message format: `[{ticket-number}] Brief summary of work`

Example: `[PL-12345] Fix authentication error in login API`

## PR Creation

Content to include in the PR description:
- Summary of changes
- Test plan
- Links to planning files (if applicable)

## After Completion

Delete the `.planning/{ticket}/current-phase` file to deactivate the workflow.
