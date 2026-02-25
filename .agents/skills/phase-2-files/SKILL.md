---
name: phase-2-files
description: >
  Generate Planning Files after Phase 1 approval. Activate when transitioning
  from planning to file creation, or when entering Phase 2. Creates 6 planning
  files in .planning/{ticket}/{branch}/ directory.
  Planning Files 생성, Phase 2 진입 시 활성화.
---

# Phase 2: Generate Planning Files

After Phase 1 plan is approved, **automatically** create 6 planning files under `.planning/{ticket}/{branch}/`.

## File Structure

```
.planning/{ticket}/{branch}/
  spec.md       — Requirements specification
  plan.md       — Implementation plan
  tasks.md      — Task tracking (North Star)
  findings.md   — Technical findings & decisions
  progress.md   — Session-by-session work log
  README.md     — Feature description (Background, Goal, How it works)
```

## Templates

Use the templates from `templates/` directory in the project root. Each template provides the standard structure. Below is a summary of key sections per file:

### spec.md
- Overview, User Scenarios & Testing (mandatory), Functional Requirements (FR-N: MUST/SHOULD), Constraints (CON-N), Success Criteria (SC-N)

### plan.md
- Summary, Requirements, Critical Files (New/Modified/Reference), Architecture diagram, Implementation Steps, Verification, Considerations

### tasks.md
- Goal (North Star), Current Phase, Phases with checkboxes and Status (pending/in_progress/complete), Key Questions, Decisions Made, Errors Encountered, Notes

### findings.md
- Requirements checklist, Research Findings (codebase structure, existing patterns), Technical Decisions table, Issues Encountered, Review Findings table, Resources

### progress.md
- Session entries (date ascending, newest at bottom), Actions taken, Files created/modified, Test Results table, Review Log table, Error Log table, 5-Question Reboot Check

### README.md
- Background (why), Goal (what), How it works (activation/deactivation), Related Documents links

## After Creation

Verify all 6 files exist, then proceed to Phase 3 (Implementation).
