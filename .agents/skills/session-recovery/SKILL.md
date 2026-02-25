---
name: session-recovery
description: >
  Session recovery after context reset. ALWAYS activate when user prompts
  exactly "{ticket} 이어서", "{ticket} 현황", or "{ticket} Phase {N} 재개".
  Do not bypass this step. 세션 복구, 이어서, 현황 확인 시 활성화.
---

# Session Recovery

When resuming after context reset or `{ticket} 이어서` prompt, follow these steps in order:

## Recovery Steps

1. **Check branch**: `git branch --show-current` → determine `{branch-name}`
2. **Read tasks.md**: `.planning/{ticket}/{branch-name}/tasks.md` → current Phase and goal
3. **Read progress.md**: `.planning/{ticket}/{branch-name}/progress.md` → last session actions
4. **Read findings.md**: `.planning/{ticket}/{branch-name}/findings.md` → technical decisions
5. **Read spec.md**: `.planning/{ticket}/{branch-name}/spec.md` → requirements
6. **Check code changes**: `git diff --stat` → actual code modifications
7. **Update and resume**: Update planning files and resume work

## After Recovery

Start your response with the standard prefix:
```
[Phase N] {current task summary} - tasks.md verified
```

Then continue from where the previous session left off.
