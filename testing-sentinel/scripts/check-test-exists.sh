#!/bin/bash
# =============================================================================
# check-test-exists.sh
# PostToolUse hook — Warns when source files are created/edited without
# corresponding test files. Inspired by PostgreSQL's culture where patches
# without tests are considered work-in-progress.
# =============================================================================

set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# If no file path found, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# ---------------------------------------------------------------------------
# Determine if this is a source file (not a test, config, or docs file)
# ---------------------------------------------------------------------------

# Skip test files themselves
if echo "$FILE_PATH" | grep -qiE '(test_|_test\.|\.test\.|\.spec\.|tests/|__tests__/|test/.*test)'; then
    exit 0
fi

# Skip non-source files (configs, docs, assets, migrations, etc.)
if echo "$FILE_PATH" | grep -qiE '\.(md|txt|json|yaml|yml|toml|ini|cfg|lock|svg|png|jpg|gif|css|html|sql|sh|dockerfile)$'; then
    exit 0
fi

# Skip common non-source directories
if echo "$FILE_PATH" | grep -qiE '(migrations/|fixtures/|static/|templates/|assets/|docs/|\.github/|\.claude/|node_modules/|vendor/|dist/|build/)'; then
    exit 0
fi

# Only check recognized source file extensions
if ! echo "$FILE_PATH" | grep -qiE '\.(py|js|ts|tsx|jsx|go|rs|c|cpp|cc|h|hpp|java|php|rb|ex|exs)$'; then
    exit 0
fi

# ---------------------------------------------------------------------------
# Look for a corresponding test file
# ---------------------------------------------------------------------------

BASENAME=$(basename "$FILE_PATH")
DIRNAME=$(dirname "$FILE_PATH")
FILENAME="${BASENAME%.*}"
EXTENSION="${BASENAME##*.}"

# Track if we found any test file
FOUND_TEST=false

# Generate possible test file patterns based on language conventions
case "$EXTENSION" in
    py)
        TEST_PATTERNS=("test_${FILENAME}.py" "${FILENAME}_test.py")
        TEST_DIRS=("tests" "test" "tests/unit" "tests/integration")
        ;;
    js|ts|jsx|tsx)
        TEST_PATTERNS=("${FILENAME}.test.${EXTENSION}" "${FILENAME}.spec.${EXTENSION}" "${FILENAME}.test.js" "${FILENAME}.spec.js")
        TEST_DIRS=("__tests__" "tests" "test" "spec")
        ;;
    go)
        TEST_PATTERNS=("${FILENAME}_test.go")
        TEST_DIRS=(".")  # Go tests live next to source
        ;;
    rs)
        # Rust tests are often inline, but also in tests/ directory
        TEST_PATTERNS=("${FILENAME}.rs")
        TEST_DIRS=("tests")
        ;;
    java)
        TEST_PATTERNS=("${FILENAME}Test.java" "${FILENAME}Tests.java")
        TEST_DIRS=("src/test" "test")
        ;;
    php)
        TEST_PATTERNS=("${FILENAME}Test.php" "${FILENAME}_test.php")
        TEST_DIRS=("tests" "test" "tests/Unit" "tests/Feature")
        ;;
    c|cpp|cc|h|hpp)
        TEST_PATTERNS=("test_${FILENAME}.c" "test_${FILENAME}.cpp" "${FILENAME}_test.c" "${FILENAME}_test.cpp")
        TEST_DIRS=("tests" "test" "t")
        ;;
    rb)
        TEST_PATTERNS=("${FILENAME}_test.rb" "${FILENAME}_spec.rb" "test_${FILENAME}.rb")
        TEST_DIRS=("test" "spec" "tests")
        ;;
    *)
        exit 0
        ;;
esac

# Search for test files in the project
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

for pattern in "${TEST_PATTERNS[@]}"; do
    if find "$PROJECT_DIR" -name "$pattern" -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/.git/*" 2>/dev/null | grep -q .; then
        FOUND_TEST=true
        break
    fi
done

# Also check for Go inline tests and Rust inline tests
if [ "$FOUND_TEST" = false ]; then
    case "$EXTENSION" in
        go)
            # Go: check if there's a _test.go file in the same directory
            SAME_DIR_TEST="${DIRNAME}/${FILENAME}_test.go"
            if [ -f "$PROJECT_DIR/$SAME_DIR_TEST" ]; then
                FOUND_TEST=true
            fi
            ;;
        rs)
            # Rust: check for #[cfg(test)] mod tests in the same file
            if [ -f "$PROJECT_DIR/$FILE_PATH" ] && grep -q '#\[cfg(test)\]' "$PROJECT_DIR/$FILE_PATH" 2>/dev/null; then
                FOUND_TEST=true
            fi
            ;;
    esac
fi

# ---------------------------------------------------------------------------
# Output result
# ---------------------------------------------------------------------------

if [ "$FOUND_TEST" = false ]; then
    # Output as JSON context for Claude (shown in verbose mode)
    cat <<EOF
{
  "message": "⚠️  No test file found for '${FILE_PATH}'. Consider creating tests following the project's conventions. Every source file should have corresponding tests (PostgreSQL/Chromium standard: patches without tests = work-in-progress).",
  "file": "${FILE_PATH}",
  "suggested_tests": ["${TEST_PATTERNS[0]}"],
  "test_dirs_checked": $(printf '%s\n' "${TEST_DIRS[@]}" | jq -R . | jq -s .)
}
EOF
fi

# Always exit 0 (non-blocking warning, not a gate)
exit 0
