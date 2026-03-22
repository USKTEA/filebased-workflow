# Session Recovery

Resume work after a context reset.

## Input

$ARGUMENTS

Extract the ticket number from the argument above (e.g., `PL-12345 이어서`, `PL-12345 현황`, `PL-12345 Phase 3 재개`).

## Recovery Steps (in order)

1. **Check branch**: `git branch --show-current` → determine `{branch-name}`
2. **Check current-phase**: `.planning/{ticket}/current-phase` → current Phase
3. **Read tasks.md**: `.planning/{ticket}/{branch-name}/tasks.md` → current Phase and goal
4. **Read progress.md**: `.planning/{ticket}/{branch-name}/progress.md` → last session actions
5. **Read findings.md**: `.planning/{ticket}/{branch-name}/findings.md` → technical decisions
6. **Read spec.md**: `.planning/{ticket}/{branch-name}/spec.md` → requirements
7. **Check code changes**: `git diff --stat` → actual code modifications

## State Cross-Validation

After reading both `current-phase` and `tasks.md`, verify they agree:
- Extract the phase number from `current-phase` file
- Extract the active phase (🔄 status) from `tasks.md`
- **If they disagree**: Report the mismatch to the user and ask which is correct. Update the incorrect one before proceeding.

## Learning Debt Aging Check

After recovery, check for stale learning debt in Obsidian vault:
1. Read the current week's and previous weeks' learning debt files via Obsidian MCP (`read-note`)
2. Count items where `- [ ] 학습 완료` is unchecked and `발견일` is 4+ weeks ago
3. If stale items exist, warn the user:
   ```
   ⚠️ 학습 부채 {N}개가 4주 이상 미소화 상태입니다.
   가장 오래된 항목: {제목} ({발견일})
   소화 방법: 직접 코드 작성 연습 / 자기 말로 설명 작성 / 팀 내 공유
   ```
4. This is a soft reminder — do not block workflow progression.

## After Recovery

Start the response with the standard prefix:
```
[Phase N] {current task summary} - tasks.md verified
```

Continue work from where the previous session was interrupted.

## `현황` Mode

If the argument contains `현황`:
- Execute the 7 steps above, but instead of resuming work, summarize and report the current state
- Output the completion status per Phase, remaining tasks, and last session summary
