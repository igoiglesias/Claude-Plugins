#!/bin/bash
# =============================================================================
# detect-test-context.sh
# UserPromptSubmit hook — Detects when the user's prompt involves testing
# and injects contextual reminders about best practices. Also creates a
# session marker file for the Stop hook to track session duration.
# =============================================================================

set -euo pipefail

INPUT=$(cat)

# Create session start marker (used by test-summary.sh)
touch /tmp/.testing-sentinel-session-start 2>/dev/null || true

# Extract the user's prompt
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)

if [ -z "$PROMPT" ]; then
    exit 0
fi

# ---------------------------------------------------------------------------
# Detect testing-related prompts
# ---------------------------------------------------------------------------

PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Check for testing-related keywords
IS_TEST_RELATED=false
CONTEXT_TYPE=""

if echo "$PROMPT_LOWER" | grep -qE '(write|create|add|generate|scaffold).*(test|spec|fuzz)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="test_creation"
elif echo "$PROMPT_LOWER" | grep -qE '(fix|debug|repair|resolve).*(bug|issue|error|crash|fail)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="bug_fix"
elif echo "$PROMPT_LOWER" | grep -qE '(coverage|untested|missing test|test gap)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="coverage_analysis"
elif echo "$PROMPT_LOWER" | grep -qE '(ci|cd|pipeline|github action|gitlab ci|jenkins).*(test)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="ci_setup"
elif echo "$PROMPT_LOWER" | grep -qE '(fuzz|property.based|hypothesis|chaos|failure injection|fault injection)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="advanced_testing"
elif echo "$PROMPT_LOWER" | grep -qE '(flaky|intermittent|random fail|unstable test)'; then
    IS_TEST_RELATED=true
    CONTEXT_TYPE="flaky_tests"
fi

# ---------------------------------------------------------------------------
# Inject context based on detected type
# ---------------------------------------------------------------------------

if [ "$IS_TEST_RELATED" = false ]; then
    exit 0
fi

case "$CONTEXT_TYPE" in
    test_creation)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] When writing tests, follow these principles: (1) Use AAA pattern (Arrange, Act, Assert). (2) One logical concern per test. (3) Descriptive names: test_<action>_<condition>_<expected>. (4) At least 2 assertions per test (NASA Power of 10). (5) Cover happy path + edge cases + error paths. (6) Use fixtures/factories, never hardcoded magic values. (7) Tests must be independent — no shared mutable state."
}
EOF
        ;;
    bug_fix)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] When fixing bugs, ALWAYS include a regression test: (1) Write a test that reproduces the bug FIRST. (2) Verify it fails before the fix. (3) Fix the bug. (4) Verify the test passes. (5) Reference the bug in the test docstring. This is non-negotiable in PostgreSQL, Chromium, and curl — every bug fix ships with a test."
}
EOF
        ;;
    coverage_analysis)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] For coverage analysis, follow Chromium's approach: (1) Measure per-file, not just globally. (2) Target >90% on critical files. (3) Track coverage trends — a decrease in a PR is a red flag. (4) Prioritize: security code > business logic > data access > utilities. (5) Coverage measures execution, not correctness — complement with mutation testing."
}
EOF
        ;;
    ci_setup)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] For CI/CD test pipelines: (1) Tests MUST gate merges — advisory tests degrade over time. (2) Pipeline order: lint/static-analysis (< 2min) → unit tests (< 5min) → integration (< 15min) → E2E (< 30min). (3) Fail fast — if lint fails, skip tests. (4) Run fuzz tests continuously or nightly, not per-PR. (5) Auto-retry flakes once, then quarantine. (6) Report per-file coverage in PR comments."
}
EOF
        ;;
    advanced_testing)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] For advanced testing techniques: (1) Fuzz testing is mandatory for code that processes external input — SQLite runs 1B mutations/day. (2) Define invariants: never crash, no memory errors, bounded output, consistent errors. (3) Failure injection: use SQLite's OOM pattern (sequential allocation failure loops). (4) Compound failures: test OOM during crash recovery. (5) OSS-Fuzz is free for open-source projects. (6) Property-based testing (Hypothesis/fast-check) complements fuzzing."
}
EOF
        ;;
    flaky_tests)
        cat <<'EOF'
{
  "additionalContext": "[Testing Sentinel] For flaky tests: (1) Track pass/fail rates — any test below 99% is flaky. (2) Quarantine within 24 hours — move to a separate suite. (3) Fix or DELETE within 1 week. A flaky test is worse than no test. (4) Common causes: timing/sleep dependencies, shared state, external services, test order coupling. (5) Prevention: no sleep() in tests, no shared mutable state, mock external services, use random ports (curl pattern)."
}
EOF
        ;;
esac

exit 0
