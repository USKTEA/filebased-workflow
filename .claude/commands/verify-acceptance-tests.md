# Acceptance Test Verifier

Run acceptance tests, analyze failing tests, and iteratively fix implementation code or test code to achieve full passage.

## Input

$ARGUMENTS

If the argument above is empty, run all tests for the relevant module.
If an argument is provided, use it as a filter for a specific test class or method.

## Prerequisites

1. Confirm branch name and ticket/module information with `git branch --show-current`
2. Identify the target module

## Step 1: Run Tests (Red)

Run the project's test command for acceptance tests. Collect all test results and classify failing tests:

| Category              | Description                                          | Fix Target        |
|-----------------------|------------------------------------------------------|-------------------|
| Missing implementation| Feature not yet implemented                          | Implementation code|
| Assertion error       | Test expected value does not match actual            | Test code         |
| Type/compile error    | Test fails to compile due to interface changes       | Test code         |
| Logic error           | Implementation exists but behavior differs from spec | Implementation code|
| Test environment issue| Test data, containers, etc.                          | Test code         |
| Spec ambiguity        | Spec interpretation is unclear                       | Ask user          |

## Step 2: Iterative Fix (Green)

Fix failing tests one at a time. For each fix cycle:

1. **Start with the simplest failures** (compile → assertion → logic → missing implementation)
2. Apply the fix
3. Run that test alone to confirm it passes
4. Once it passes, re-run all tests to check for regressions
5. Address any regressions immediately

### Fix Principles

- **Prefer fixing implementation code**: If the test accurately reflects the spec, fix the implementation
- **Minimize test code changes**: Only adjust roughly written assertions and TODO sections
- **No spec changes**: If the spec is ambiguous, ask the user rather than interpreting arbitrarily
- **One at a time**: Do not fix multiple failures simultaneously
- **Maximum 10 iterations**: If not resolved within 10 attempts, report remaining failures and stop

## Step 3: Refactor (Refactor)

After all tests pass:

1. Remove duplication in test code (move common setup to shared fixtures)
2. Clean up fixture helpers
3. Remove unnecessary `// TODO` comments
4. Run all tests once more to confirm they still pass after refactoring

## Step 4: Final Report

```
## Acceptance Test Verification Complete

### Execution Results
- Total: N scenarios
- Passed: N (100%)

### Fix History
| # | Type             | File            | Change                    |
|---|------------------|-----------------|---------------------------|
| 1 | Test fix         | ...Test         | Updated assertion         |
| 2 | Implementation fix | ...Service    | Added missing method      |

### Coverage vs Spec
| Requirement ID | Scenario      | Result    |
|----------------|---------------|-----------|
| FR-1           | Scenario name | ✅ Passed |

### Findings
- (Spec ambiguities, edge cases, etc. discovered during testing)
```

Also record findings in `findings.md`.

## Notes

- When modifying implementation code, be careful not to break existing tests
- If there are ambiguous parts in the spec, **always ask the user**. Do not interpret arbitrarily
