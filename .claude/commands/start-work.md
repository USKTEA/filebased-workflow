# Phase 1: Planning & Verification

Starting work on the $ARGUMENTS ticket.

## Prerequisites

1. Extract the ticket number from `$ARGUMENTS` (e.g., `PL-12345`)
2. Write `1` to `.planning/{ticket}/current-phase`
3. Verify the `.planning/{ticket}/{branch}/` directory exists, create it if not

## Phase 1: 6-Step Spec-Driven Planning

### Step 1: Spec Draft

#### 1-1. Developer's Independent Design (MUST — before AI analysis)

Before AI explores the codebase, ask the developer **3 design judgment questions** derived from the ticket.

**Question generation rules:**
- Specific to THIS ticket (not generic)
- Binary or small-choice (A vs B, not open-ended "어떻게 접근하시겠어요?")
- About design DECISIONS, not implementation details

**Derive questions from the ticket's domain:**

| Ticket Domain | Example Questions |
|---------------|-------------------|
| Data mutation | Affected collections, sync vs async, transaction scope |
| API design | Endpoint granularity, auth model, versioning strategy |
| Refactoring | Scope boundary, backward compatibility, migration path |
| Integration | Failure handling, retry strategy, timeout policy |

Record the developer's answers in `findings.md` → `## Delta Log` section. If the developer says "모르겠다", record that too — it is itself a data point.

**Purpose**: Prevents "anchoring bias" where the developer's judgment is overwritten by AI's first suggestion. The delta between the developer's initial design and the final implementation is a measurable growth signal.

#### 1-2. AI Codebase Analysis

- Explore the codebase and analyze the architecture related to the ticket
- Read the ticket requirements and create an initial spec.md draft
- Save spec.md to `.planning/{ticket}/{branch}/spec.md` immediately
- This draft covers Happy Path only — edge cases will be added in Step 2

**Save the draft to file before proceeding. This prevents context loss during long interviews.**

### Step 2: Reverse Interview

AI conducts a reverse interview to uncover edge cases the ticket doesn't mention.

#### 2-1. Domain Context (MUST — before asking constraint questions)

Confirm what the domain model read from code means in business terms.
AI presents its understanding first ("I understand X as..."), and the developer corrects.

- What each core entity means in business terms
- Why entity relationships are designed that way
- Business rules that cannot be inferred from code alone

**Never start technical questions without domain context.** Without understanding the domain, constraint questions are meaningless.

#### 2-2. Business Logic Validation (MUST — alongside constraint questions)

Find contradictions, omissions, and anomalies in the spec draft's business logic.

- Is the cascade relationship business-justified?
- When the same operation applies to multiple entity types, verify whether scope boundaries differ due to data structure differences
- Are there ordering contradictions when different entities share the same reference?
- Are out-of-scope items truly safe to exclude?
- Is cross-module cascade allowed?

#### 2-3. Constraint Dimension Selection

Analyze the ticket and select relevant constraint dimensions from:

| Dimension | Select When |
|-----------|-------------|
| Concurrency / Idempotency | State-changing APIs, payments, create/update where duplicate requests are possible |
| Failure Isolation | External API calls, inter-service communication, async messaging |
| State Consistency | DB transactions + external event publishing, cache invalidation happening together |
| Volume / Load | List queries, batch processing, data accumulation expected |
| Security / Auth | Token-based authentication, permission branching |

Present the selected dimensions and reasoning to the developer:
> "This feature primarily involves **Concurrency/Idempotency** and **Failure Isolation**. Reason: [rationale]"

#### 2-4. Interview Execution

For each selected dimension, ask **3~5 focused questions** sequentially:

- Ask one batch of questions at a time (not all at once)
- Wait for the developer's answer before proceeding
- Questions should be specific and actionable, not abstract

#### 2-5. Spec Update

After each interview round:
1. Update spec.md's `Edge Cases & Non-Functional Constraints` section
2. Check the relevant constraint dimension checkboxes
3. Add EC-n items in Given/When/Then format
4. Save to file immediately

#### 2-6. Interview Completion

The interview ends when:
- All selected dimensions have been covered
- The developer says the spec is sufficient
- No more unknown unknowns remain

**After the interview, present the updated spec.md summary to the user and wait for approval.**

### Step 3: Plan Creation

Based on the finalized spec.md (including edge cases):
- Design the implementation approach
- Identify affected modules and files
- Document the execution plan in plan.md
- **Present the plan to the user and wait for approval**

### Step 4: Plan Review

Review whether the plan is correct:
- Are all requirements (FR + CON + EC) reflected without omissions?
- Is it consistent with existing codebase patterns?
- Have all affected modules been identified?

### Step 5: Meta-Review (Review of the Review)

Review whether the review itself is accurate:
- A self-reflection step to mitigate AI confirmation bias
- "Is there anything the review missed?"

### Step 6: Over-engineering Check

Review whether the plan is excessive:
- Are there unnecessary abstractions?
- Are there YAGNI (You Aren't Gonna Need It) violations?
- Are edge case mitigations proportional to actual risk?

## Phase Gate

After all 6 steps are complete, present the final results to the user and wait for approval.
**Do not proceed to the next Phase before approval.**
After user approval, guide them to `/advance-phase`.