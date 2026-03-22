#!/usr/bin/env bash
#
# Completion Check - Stop hook
#
# Warns if there are incomplete phases in tasks.md when the agent tries to stop.
# Does NOT block (always exits 0) - just provides a reminder.

set -uo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/../.." && pwd)

# Get current branch and extract ticket number
BRANCH=$(git -C "$PROJECT_ROOT" branch --show-current 2>/dev/null || echo "")
TICKET=$(echo "$BRANCH" | grep -o 'PL-[0-9]*' | head -1 || echo "")

if [[ -z "$TICKET" ]]; then
  exit 0
fi

# Find tasks.md - check multiple possible locations
TASKS_FILE=""
for dir in "$PROJECT_ROOT/.planning/$TICKET"/*/; do
  if [[ -f "${dir}tasks.md" ]]; then
    TASKS_FILE="${dir}tasks.md"
    break
  fi
done

if [[ -z "$TASKS_FILE" ]] || [[ ! -f "$TASKS_FILE" ]]; then
  exit 0
fi

# Check for incomplete phases (🔄 or ⏸️ that are not yet ✅)
INCOMPLETE=$(grep -c '🔄\|⏸️' "$TASKS_FILE" 2>/dev/null || echo 0)
COMPLETE=$(grep -c '✅' "$TASKS_FILE" 2>/dev/null || echo 0)

# Ensure values are single integers
INCOMPLETE=$(echo "$INCOMPLETE" | head -1 | tr -d '[:space:]')
COMPLETE=$(echo "$COMPLETE" | head -1 | tr -d '[:space:]')

if [[ "$INCOMPLETE" -gt 0 ]] 2>/dev/null; then
  echo "Warning: tasks.md has ${INCOMPLETE} incomplete Phase(s) (complete: ${COMPLETE}). Please verify work is finished." >&2
fi

# Always allow stop (just warn)
exit 0
