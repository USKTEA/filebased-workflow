# Phase 3: Acceptance Test Generator (ATDD)

Generate acceptance test code based on the scenarios in spec.md.

## Input

$ARGUMENTS

If the argument above is empty, locate and use `.planning/{ticket}/{branch}/spec.md`.
If an argument is provided, use the spec file at that path.

## Prerequisites

1. Confirm branch name and ticket number with `git branch --show-current`
2. Verify `.planning/{ticket}/current-phase` is `3`

## Developer Acceptance Criteria (MUST — before AI generates tests)

Before AI writes any test code, ask the developer:

> **"이 기능의 인수 조건을 자연어로 3개 이상 작성해주세요. 정상 케이스와 실패 케이스 각각 1개 이상 포함해주세요."**

Example response:
- "Role 삭제하면 해당 roleId가 Manager의 roleIds에서 제거되어야 한다"
- "이미 삭제된 Role을 다시 삭제하면 에러 없이 무시되어야 한다"
- "존재하지 않는 roleId로 삭제하면 404가 나와야 한다"

Record the developer's criteria in `findings.md` → `## Delta Log` section (항목: "인수 조건"). After AI generates tests, compare: did the developer's criteria cover what the spec says? Were there gaps?

**Purpose**: Ensures the developer actively thinks about "what proves this feature works" before AI generates test code. Without this, the developer only reviews AI-generated tests passively.

## Spec Extraction

3. Read spec.md and extract the following:
   - **User Scenarios**: User stories in "As [user], I [action], So [benefit]" format
   - **Acceptance Criteria**: Acceptance conditions in Given/When/Then format
   - **Functional Requirements**: Numbered functional requirements such as FR-1, FR-2
   - **Constraints**: Constraints such as CON-1, CON-2
   - **Edge Cases**: Edge case scenarios such as EC-1, EC-2 (from Edge Cases & Non-Functional Constraints section)
   - **API Specification**: API endpoint definitions (if present)

## Test Code Guidelines

Follow the project's existing test patterns. Key principles:

### Test Structure
- Group related scenarios in nested test classes/groups
- Use descriptive names that reflect the scenario
- Follow BDD pattern: Given/When/Then comments from spec.md verbatim

### Test Double Policy

| Category | Mock Allowed? | Example |
|----------|--------------|---------|
| Business logic (Service, Repository) | **NO** — use real instances | Real service + real DB |
| Infrastructure - Auth/Security | Yes | Mock auth service |
| Infrastructure - External API | Yes | Mock external client |
| Infrastructure - Audit/Logging | Yes | Mock audit logger |
| Event publisher (for verification) | Yes | Mock + verify |

**Rationale**: Business logic must be tested end-to-end with real dependencies to catch integration bugs. Non-business infrastructure may be mocked because they are orthogonal to the behavior under test.

### Parameterized Boundary Tests
When multiple boundary values test the same behavior, use parameterized tests instead of separate test methods.

### Edge Case Tests
Edge cases from EC-n items generate a separate test group.

## Systematic Scenario Derivation (Specification-Based Testing)

Before writing test code, derive scenarios systematically:

### Step 1: Identify partitions
For each FR/CON/EC, identify equivalence partitions — groups of inputs treated the same way.

### Step 2: Analyze boundaries
For each partition, identify boundary values (on-point, off-point, in-point).

### Step 3: Devise test cases
Combine partitions and boundaries. Prioritize: each partition in at least one test, boundaries always tested.

### Step 4: Augment with creativity
After systematic derivation, add experience-based tests:
- "What if this operation runs twice?" (idempotency)
- "What if the referenced entity was already deleted?" (ordering)
- "What if different types share the same ID?" (collision)

## Test Quality Principles

1. **Strong assertions**: Assert the exact expected state, not just non-null
2. **One reason to fail**: Each test fails for exactly one reason
3. **Cohesive and independent**: Self-contained with own fixtures
4. **Behavior-breaking tests**: Break when behavior changes, not implementation details
5. **No flakiness**: Deterministic tests only
6. **Decomposed expected values**: Explain calculation instead of magic numbers

### Test Smells to Avoid
- Unclear assertions (too broad)
- Overly generic fixtures (shared setup hiding test requirements)
- Sensitive assertions (implementation details)
- Fixture over-specification (irrelevant field values visible)

## Generation Rules

1. **Scenario mapping**: Each Acceptance Criteria → one test group + test method. Copy spec text verbatim into Given/When/Then comments
2. **Functional requirement coverage**: Every FR-n covered by at least one test
3. **Constraint reflection**: CON-n items → negative tests (expect exceptions/errors)
4. **Edge case coverage**: EC-n items → edge case tests in separate group
5. **API tests**: If API spec present, write tests with real HTTP calls (not mocked)
6. **Naming convention**: Test names in English (descriptive, not numbered). Native language descriptions in display names/annotations only
7. **Rough implementation**: Initially clear in intent, mark details with `// TODO: finalize after implementation`
8. **Data independence**: Initialize test data in setup; each test independently runnable

## Coverage Report

After generation is complete, output the following:

```
## Acceptance Test Coverage Report

### Mapping Table
| Requirement ID | Test Scenario        | Category  | Dimension     | Status     |
|----------------|----------------------|-----------|---------------|------------|
| FR-1           | Scenario name        | Happy     | -             | ✅ Created |
| CON-1          | Negative test        | Negative  | -             | ✅ Created |
| EC-1           | Edge case scenario   | Edge      | 동시성/멱등성 | ✅ Created |

### SC Coverage
| SC ID  | Covered By        | Status     |
|--------|-------------------|------------|
| SC-1   | FR-1, EC-2        | ✅ Covered |

### Compile Status
- Compilable tests: N개 (기존 코드 대상)
- Expected Red (unresolved reference): N개 (신규 코드 대상)
- Unexpected errors: N개 ← 0이어야 함

### Next Steps
1. Review the generated tests
2. Verify with `/verify-acceptance-tests` (after implementation)
```

## Phase Gate

### Pre-flight Compile Check

Before presenting results, run the project's compile/build command and classify results:

| Category | Meaning | Expected? |
|----------|---------|-----------|
| **Compiles** | Tests against existing code compile successfully | Yes (existing code) |
| **Unresolved reference** | Class/method does not exist yet | Yes (new feature - expected Red) |
| **Other compile error** | Wrong import, syntax error, type mismatch | No - fix before proceeding |

If "Unexpected errors" > 0, fix them before presenting to user.

### Approval

Present the coverage report + compile status to the user and wait for approval.
**Do not proceed to the next Phase before approval.**

## Notes

- Do not guess behavior not specified in the spec
- Write black-box tests that do not depend on implementation details
- The initially generated tests are a "rough draft" and are expected to be refined alongside the implementation
