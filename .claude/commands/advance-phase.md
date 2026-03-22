# Phase Gate: Advance to Next Phase

Complete the current Phase and transition to the next Phase.

## Procedure

1. Confirm branch name and ticket number with `git branch --show-current`
2. Read the current Phase from `.planning/{ticket}/current-phase`
3. Verify all checkboxes for the current Phase are complete in `.planning/{ticket}/{branch}/tasks.md`

## Phase Gate Checklist

Confirm the following for the current Phase:

- [ ] All tasks in the current Phase are complete?
- [ ] Results have been presented to the user?
- [ ] User has approved?

## Why Review Gate (Phase 4 → 5 Only)

When transitioning from Phase 4 to Phase 5, execute the Why Review before proceeding:

### Step 1: Collect Review Items

Two sources are combined:

**Source A — AI-extracted decisions:**
Read all files changed in Phase 4 and identify key implementation decisions:
- New patterns or APIs not previously used in the codebase
- Non-obvious architectural choices (why X instead of Y)
- Complex logic that requires domain understanding

There is no fixed number — extract as many as are genuinely noteworthy. Trivial or obvious decisions should be omitted.

**Source B — Developer's Question Log:**
Read `findings.md` → `## Question Log` section. Include all questions the developer asked during any Phase.

### Step 2: Present to Developer
Present both sources together:
```
## Why Review (Phase 4 → 5 Gate)

### 구현 핵심 결정
1. ☐ [결정 요약]
   → 이유: [AI가 이 선택을 한 근거]

### 작업 중 질문했던 항목
1. ☐ [Phase 1에서 질문한 내용 요약]
2. ☐ [Phase 3에서 질문한 내용 요약]
```

Ask: **"이 중 모르거나 더 깊이 이해하고 싶은 항목이 있나요? 번호로 알려주세요."**

### Step 3: Record Learning Debt
Items the developer marks as unknown → record to Obsidian vault:
- Path: `/Users/suktae/work/personal/Obsidian Vault/learning-debt/{current-week}.md`
- Week format: `YYYY-WNN` (e.g., `2026-W12`)

**파일이 없는 경우** → Write로 새로 생성 (frontmatter + Items 섹션 포함):
```markdown
---
tags:
  - learning-debt
  - "{current-week}"
week: {current-week}
created: {date}
---

# {current-week} 학습 부채

> 이번 주 AI 코딩 중 발견된 학습 포인트

## Items

### {항목 제목}
- [ ] 학습 완료
- **티켓**: PL-XXXXX
- **발견일**: {date}
...
```

**파일이 이미 있는 경우** → Read 후 `## Items` 섹션 하단에 Edit으로 항목 추가:
```markdown
### {항목 제목}
- [ ] 학습 완료
- **티켓**: PL-XXXXX
- **발견일**: {date}
- **출처**: {source}
- **위치**: `{file:line}`
- **맥락**: {context}
- **난이도**: {1~3}
- **키워드**: #tag1 #tag2
```

### Step 4: Explain (Optional)
If the developer wants immediate explanation for any item:
- Explain in teacher mode (concept → why it matters → code example)
- After explanation, ask if they want to mark it as resolved or keep it as learning debt

### Step 5: Proceed
After Why Review is complete, continue with the normal transition.

## Transition

If all checks pass:

1. Increment the number in `.planning/{ticket}/current-phase` by 1
2. In `tasks.md`, mark the current Phase as ✅ and the next Phase as 🔄
3. **Cross-validate**: Re-read both files and confirm `current-phase` number matches the 🔄 Phase in `tasks.md`. If mismatch, fix immediately.
4. Guide the user to the slash command for the next Phase:

| Phase | Next Command                   |
|-------|--------------------------------|
| 1 → 2 | `/generate-files`             |
| 2 → 3 | `/generate-acceptance-tests`  |
| 3 → 4 | `/implement`                  |
| 4 → 5 | `/review`                     |
| 5 → 6 | `/deliver`                    |

## Notes

- Do not transition Phases without user approval
- Upon completing Phase 6, delete the current-phase file
