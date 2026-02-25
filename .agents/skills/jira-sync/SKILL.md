---
name: jira-sync
description: >
  Jira ticket synchronization via jira-sync.py script. ALWAYS activate when
  user prompts "{ticket} 작업 시작" (pull from Jira) or before committing
  (push to Jira). The agent NEVER accesses Jira directly.
  Jira 동기화, pull, push, 티켓 연동 시 활성화.
---

# Jira Ticket Sync

> **IMPORTANT: The agent NEVER accesses Jira directly.**
> Always use `jira-sync.py` script for authentication, parsing, and idempotency.

## Prerequisites (once per session)

```bash
# 1. Verify Python 3
python3 --version

# 2. Verify requests library
python3 -c "import requests" 2>/dev/null || pip3 install -r scripts/requirements.txt
```

- If Python 3 is missing: inform user and stop
- If `requests` is missing: attempt `pip3 install -r scripts/requirements.txt`
- If `pip3` fails: inform user of manual installation and stop

## Setup (first time)

```bash
python3 scripts/jira-sync.py setup
```

Or set environment variables directly:
```bash
export JIRA_BASE_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
```

- **API Token**: Generate at https://id.atlassian.com/manage/api-tokens (classic token recommended)
- **Auth method**: Default is Basic Auth. For scoped tokens, add `JIRA_AUTH_METHOD=bearer` to `.env`
- **Auto-Routing**: Script auto-discovers cloudId from `JIRA_BASE_URL` and uses API Gateway (`api.atlassian.com`)

## Pull (on work start)

When receiving `{ticket} 작업 시작` prompt:

1. Run dependency check (once per session)
2. Execute pull:
   ```bash
   python3 scripts/jira-sync.py pull {ticket-number}
   ```
3. Script handles: Jira API auth, data parsing, file creation in `.planning/{ticket}/{branch}/`
4. **Conflict detection**: Compares timestamps per file. Skips if local is newer. Use `--force` to overwrite:
   ```bash
   python3 scripts/jira-sync.py pull {ticket-number} --force
   ```
5. After script completes, read only the generated local files and start work
6. If script fails (ticket not found, auth error, missing deps): show warning and stop

## Push (before commit)

Before committing:

1. Execute push:
   ```bash
   python3 scripts/jira-sync.py push {ticket-number}
   ```
   <!-- SYNC: jira-sync push procedure -->
2. **Conflict detection**: Compares timestamps per file. Skips if Jira is newer. Use `--force` to overwrite:
   ```bash
   python3 scripts/jira-sync.py push {ticket-number} --force
   ```
3. Script safely preserves existing Jira description while idempotently updating `PLANNING_START`~`PLANNING_END` region only
4. The agent MUST NOT directly compose text to overwrite Jira description

## Serialization Format (internal)

```
(existing Jira ticket description — preserved as-is)

=== PLANNING_START ===

=== FILE: spec.md [2026-02-22 15:30:00 KST] ===
(spec.md content)

=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===
(tasks.md content)

=== FILE: findings.md [2026-02-22 15:30:00 KST] ===
(findings.md content)

=== FILE: progress.md [2026-02-22 15:30:00 KST] ===
(progress.md content)

=== FILE: plan.md [2026-02-22 15:30:00 KST] ===
(plan.md content)

=== FILE: README.md [2026-02-22 15:30:00 KST] ===
(README.md content)

=== PLANNING_END ===
```

- Each FILE marker includes KST timestamp for bidirectional conflict detection
- Local files have `<!-- LAST_SYNC: timestamp KST -->` metadata at the bottom
- First push: appends planning region to end of description
- Subsequent pushes: replaces existing `PLANNING_START`~`PLANNING_END` region
