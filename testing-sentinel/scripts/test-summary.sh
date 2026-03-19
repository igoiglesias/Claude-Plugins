#!/bin/bash
# =============================================================================
# test-summary.sh
# Stop hook — Summarizes test-related actions performed during the session
# and flags any source files that were modified without corresponding test
# updates. Provides a quick quality check before the developer moves on.
# =============================================================================

set -euo pipefail

INPUT=$(cat)

# Extract session info
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# ---------------------------------------------------------------------------
# Scan for recently modified files (last 30 minutes as a proxy for session)
# ---------------------------------------------------------------------------

SOURCE_EXTS="py|js|ts|tsx|jsx|go|rs|c|cpp|cc|java|php|rb"
TEST_PATTERNS="test_|_test\.|\.test\.|\.spec\.|_test\.go|Test\.java|_spec\.rb"

# Find recently modified source files (not tests)
MODIFIED_SOURCES=()
while IFS= read -r file; do
    if [ -n "$file" ]; then
        MODIFIED_SOURCES+=("$file")
    fi
done < <(find "$PROJECT_DIR" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/vendor/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -newer /tmp/.testing-sentinel-session-start 2>/dev/null \
    -type f \
    -regextype posix-extended \
    -regex ".*\.($SOURCE_EXTS)$" 2>/dev/null | \
    grep -viE "$TEST_PATTERNS" 2>/dev/null || true)

# Find recently modified test files
MODIFIED_TESTS=()
while IFS= read -r file; do
    if [ -n "$file" ]; then
        MODIFIED_TESTS+=("$file")
    fi
done < <(find "$PROJECT_DIR" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/vendor/*" \
    -newer /tmp/.testing-sentinel-session-start 2>/dev/null \
    -type f \
    -regextype posix-extended \
    -regex ".*\.($SOURCE_EXTS)$" 2>/dev/null | \
    grep -iE "$TEST_PATTERNS" 2>/dev/null || true)

# ---------------------------------------------------------------------------
# Build summary
# ---------------------------------------------------------------------------

SOURCE_COUNT=${#MODIFIED_SOURCES[@]}
TEST_COUNT=${#MODIFIED_TESTS[@]}

# Find source files without corresponding test modifications
UNTESTED_SOURCES=()
for src in "${MODIFIED_SOURCES[@]}"; do
    BASENAME=$(basename "$src")
    FILENAME="${BASENAME%.*}"

    # Check if any test file mentions this module name
    HAS_TEST=false
    for test_file in "${MODIFIED_TESTS[@]}"; do
        if echo "$test_file" | grep -qi "$FILENAME"; then
            HAS_TEST=true
            break
        fi
    done

    if [ "$HAS_TEST" = false ]; then
        UNTESTED_SOURCES+=("$src")
    fi
done

UNTESTED_COUNT=${#UNTESTED_SOURCES[@]}

# ---------------------------------------------------------------------------
# Output summary as context for Claude
# ---------------------------------------------------------------------------

if [ "$SOURCE_COUNT" -eq 0 ] && [ "$TEST_COUNT" -eq 0 ]; then
    # No code changes detected — no summary needed
    exit 0
fi

# Build the untested files JSON array
UNTESTED_JSON="[]"
if [ "$UNTESTED_COUNT" -gt 0 ]; then
    UNTESTED_JSON=$(printf '%s\n' "${UNTESTED_SOURCES[@]}" | jq -R . | jq -s .)
fi

cat <<EOF
{
  "testing_sentinel_summary": {
    "source_files_modified": $SOURCE_COUNT,
    "test_files_modified": $TEST_COUNT,
    "source_files_without_test_updates": $UNTESTED_COUNT,
    "untested_files": $UNTESTED_JSON,
    "recommendation": $(
      if [ "$UNTESTED_COUNT" -eq 0 ]; then
        echo '"✅ All modified source files have corresponding test updates."'
      elif [ "$UNTESTED_COUNT" -le 2 ]; then
        echo '"⚠️  Some source files were modified without test updates. Consider adding tests before committing."'
      else
        echo '"🚨 Multiple source files lack test coverage for recent changes. Strongly recommend adding tests before this code ships."'
      fi
    )
  }
}
EOF

exit 0
