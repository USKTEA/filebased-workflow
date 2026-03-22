# Phase 2: Generate Planning Files

After Phase 1 plan is approved, generate 6 planning files under `.planning/{ticket}/{branch}/`.

## Prerequisites

1. Confirm branch name and ticket number with `git branch --show-current`
2. Verify `.planning/{ticket}/current-phase` is `2`

## File Structure

```
.planning/{ticket}/{branch}/
  spec.md       — (Phase 1에서 이미 생성됨 — 여기서는 검토만)
  plan.md       — Implementation plan
  tasks.md      — Task tracking (North Star)
  findings.md   — Technical findings & decisions
  progress.md   — Session-by-session work log
  README.md     — Feature description (Background, Goal, How it works)
```

## Templates

Use the templates in the `.claude/templates/` directory. Key sections for each file:

### spec.md (already created in Phase 1)
- Read and review the existing spec.md from Phase 1
- Fill in any missing sections (FR/CON/SC/EC numbering, etc.)
- Do NOT create from scratch

### plan.md
- Summary, Requirements, Critical Files (New/Modified/Reference), Architecture diagram, Implementation Steps, Verification, Considerations

### tasks.md
- Goal (North Star), Current Phase, Phase 1~6 with checkboxes and Status (⏸️/🔄/✅)

### findings.md
- Requirements checklist, Research Findings, Technical Decisions table, Issues Encountered, Review Findings table

### progress.md
- Session entries (date ascending), Actions, Files created/modified, Test Results, Error Log, Review Log

### README.md
- Background (why), Goal (what), How it works (activation/deactivation), Related Documents

## Phase Gate

After confirming all 6 files have been generated, present the results to the user and wait for approval.
**Do not proceed to the next Phase before approval.**
