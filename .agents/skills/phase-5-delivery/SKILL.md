---
name: phase-5-delivery
description: >
  Final gate assessment and delivery. Activate when all reviews are complete
  and ready for commit/PR, or when entering Phase 5. Includes deploy readiness
  check and commit conventions.
  배포, 커밋, PR, 최종 게이트, Phase 5 진입 시 활성화.
---

# Phase 5: Final Gate & Delivery

## Deploy Readiness Assessment

A final judgment synthesizing all reviews. Even if individual reviews pass, the overall quality may not be deploy-ready.

- Is the quality sufficient for deployment as-is?
- Do all tests pass?
- Has `progress.md` been updated with session work log?
- Are all Phases in `tasks.md` marked complete?

## Pre-Commit: Jira Sync (Push)

Before committing, sync local planning files to Jira:

```bash
python3 scripts/jira-sync.py push {ticket-number}
```
<!-- SYNC: jira-sync push procedure -->

If the script fails or Jira has newer content, use `--force` to overwrite:
```bash
python3 scripts/jira-sync.py push {ticket-number} --force
```

## Commit Convention

Commit message format: `[{ticket-number}] work summary`

Example: `[PL-12345] 로그인 API 인증 오류 수정`

## PR Creation

Include in the PR description:
- Summary of changes
- Test plan
- Link to planning files if relevant
