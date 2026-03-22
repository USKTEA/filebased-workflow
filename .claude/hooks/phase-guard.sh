#!/usr/bin/env bash
#
# Phase Guard - PreToolUse hook for Write|Edit|Bash
#
# Reads the current phase from .planning/{ticket}/current-phase and blocks
# file modifications that are not allowed for the current phase.
#
# Exit codes:
#   0 - allow the tool call
#   2 - block the tool call (message sent to stderr)
#
# Limitations:
#   - Bash tool: only checks for common file-write patterns (>, tee, cp, mv, dd)
#     Not exhaustive — determined agents may find other ways to write files.

set -uo pipefail

# Read tool input from stdin
INPUT=$(cat)

# Determine tool type from input
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"tool_name"[[:space:]]*:[[:space:]]*"//;s/"$//' || echo "")

# For Bash tool: extract command and check for file-write patterns
if [[ "$TOOL_NAME" == "Bash" ]]; then
  COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"//;s/"$//' || echo "")
  # If no obvious file-write pattern, allow
  if ! echo "$COMMAND" | grep -qE '(>|tee |cat .* >|cp |mv |dd |install |sed -i|curl -o|curl .* -o|wget -O|wget .* -O)'; then
    exit 0
  fi
  # Bash file-write detected — fall through to phase check below
  # Use the command itself as a proxy (can't extract exact target reliably)
  FILE_PATH=""
  IS_BASH_WRITE=true
else
  IS_BASH_WRITE=false
  # Extract file_path from JSON (no jq dependency)
  FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"//;s/"$//' || echo "")
fi

# If no file_path found and not a Bash write, allow (safety fallback)
if [[ -z "$FILE_PATH" ]] && [[ "$IS_BASH_WRITE" != "true" ]]; then
  exit 0
fi

# Get project root (where .claude/ lives)
PROJECT_ROOT=$(cd "$(dirname "$0")/../.." && pwd)

# Get current branch and extract ticket number (PL-XXXXX)
BRANCH=$(git -C "$PROJECT_ROOT" branch --show-current 2>/dev/null || echo "")
TICKET=$(echo "$BRANCH" | grep -o 'PL-[0-9]*' | head -1 || echo "")

# If no ticket found, allow (not in a workflow branch)
if [[ -z "$TICKET" ]]; then
  exit 0
fi

# Read current phase
PHASE_FILE="$PROJECT_ROOT/.planning/$TICKET/current-phase"
CURRENT_PHASE=""
if [[ -f "$PHASE_FILE" ]]; then
  CURRENT_PHASE=$(tr -cd '0-9' < "$PHASE_FILE" 2>/dev/null || echo "")
fi

# If phase file doesn't exist, is empty, or invalid, allow everything
if [[ -z "$CURRENT_PHASE" ]] || ! [[ "$CURRENT_PHASE" =~ ^[1-6]$ ]]; then
  exit 0
fi

# For Bash write commands, apply phase-aware rules
if [[ "$IS_BASH_WRITE" == "true" ]]; then
  # Self-protection: block Bash writes targeting hooks regardless of phase
  if echo "$COMMAND" | grep -qE '\.claude/hooks'; then
    echo "Phase ${CURRENT_PHASE}: Bash modification of '.claude/hooks/**' is blocked during workflow. Deactivate workflow first." >&2
    exit 2
  fi
  case "$CURRENT_PHASE" in
    4) exit 0 ;;  # Everything allowed
    3)
      # Phase 3: only allow if command references src/test paths
      if echo "$COMMAND" | grep -qE 'src/test'; then
        exit 0
      fi
      echo "Phase 3 (ATDD): Bash file-write only allowed for src/test/** paths. Use Write/Edit tool instead." >&2
      exit 2
      ;;
    *)
      echo "Phase ${CURRENT_PHASE}: Bash file-write pattern detected. Direct file writing is restricted in Phase ${CURRENT_PHASE}. Use Write/Edit tool or /advance-phase to transition." >&2
      exit 2
      ;;
  esac
fi

# Resolve symlinks to prevent symlink bypass (portable: works on macOS and Linux)
FILE_PATH=$(perl -MCwd -e 'print Cwd::abs_path(shift)' "$FILE_PATH" 2>/dev/null || readlink -f "$FILE_PATH" 2>/dev/null || echo "$FILE_PATH")

# Normalize file path to be relative to project root for matching
REL_PATH="${FILE_PATH#$PROJECT_ROOT/}"

# Always allow .planning/** modifications
if [[ "$REL_PATH" == .planning/* ]]; then
  exit 0
fi

# Block .claude/hooks/** modifications (prevent self-modification of enforcement)
if [[ "$REL_PATH" == .claude/hooks/* ]]; then
  echo "Phase ${CURRENT_PHASE}: '.claude/hooks/**' modifications are blocked during workflow. Deactivate workflow first." >&2
  exit 2
fi

# Allow other .claude/** modifications (commands, templates, etc.)
if [[ "$REL_PATH" == .claude/* ]]; then
  exit 0
fi

# Phase-specific path rules
case "$CURRENT_PHASE" in
  1|2|5|6)
    # Only .planning/** and .claude/** allowed (already handled above)
    echo "Phase ${CURRENT_PHASE}: '${REL_PATH}' is blocked. Only .planning/** files can be modified in this Phase. Use /advance-phase to transition." >&2
    exit 2
    ;;
  3)
    # .planning/** (handled above) + **/src/test/** allowed
    if [[ "$REL_PATH" == */src/test/* ]] || [[ "$REL_PATH" == src/test/* ]]; then
      exit 0
    fi
    echo "Phase 3 (ATDD): '${REL_PATH}' is blocked. Only .planning/** and **/src/test/** files can be modified in this Phase. Use /advance-phase to transition." >&2
    exit 2
    ;;
  4)
    # Everything allowed
    exit 0
    ;;
esac

# Fallback: allow
exit 0
