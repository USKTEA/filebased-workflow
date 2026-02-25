---
name: phase-1-planning
description: >
  Planning and verification phase with 4-step validation. ALWAYS activate when
  user prompts "{ticket} 작업 시작" to start new work, or when entering Phase 1.
  Covers plan creation, plan review, meta-review, and over-engineering check.
---

# Phase 1: Planning & Verification

Before starting complex work, go through 4 steps of plan validation.

## Step 1: Plan Creation

Use your planning tools to start a planning interview:
- Explore the codebase and analyze architecture
- Confirm requirements, constraints, and technical decisions through user interview
- Document the execution plan
- **After plan completion, present results to user and await approval (see AGENTS.md Phase Gate Rule)**

## Step 2: Plan Review

Review whether the plan is correct:
- Are all requirements reflected without omission?
- Is it consistent with existing codebase patterns?
- Are all affected modules identified?

## Step 3: Meta-Review (Review of the Review)

Review whether the review itself is accurate:
- Self-reflection step to mitigate AI confirmation bias
- "Is there anything the review missed?"

## Step 4: Over-engineering Check

Review whether the plan is excessive:
- Are there unnecessary abstractions?
- Any YAGNI (You Aren't Gonna Need It) violations?
- Checking "is this over-engineered?" at planning stage is more cost-effective than "simplify this" after implementation

After all 4 steps are complete, present the final results to the user and await approval before proceeding.
