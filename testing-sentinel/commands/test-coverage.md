---
description: Identify untested code paths, coverage gaps, and dead code. Suggest targeted tests for the most critical uncovered areas, following Chromium's >90% per-file approach.
---

# Test Coverage

## Purpose

Analyze the project's test coverage to find blind spots — untested functions, uncovered branches, error paths without tests — and generate targeted tests for the most impactful gaps.

## Instructions

1. **Determine coverage tooling:**
   - Detect the language and appropriate coverage tool:
     - Python: `pytest-cov` / `coverage.py`
     - JS/TS: `c8` / `istanbul` / `nyc`
     - Go: `go test -cover`
     - C/C++: `gcov` / `llvm-cov`
     - Rust: `cargo-tarpaulin` / `llvm-cov`
     - Java: `JaCoCo`
     - PHP: `phpunit --coverage-*`
   - Check if coverage is already configured in the project.

2. **If coverage data exists:**
   - Parse existing coverage reports (`.coverage`, `coverage/lcov.info`, `coverage.xml`).
   - Identify files with lowest coverage.
   - Identify critical modules (business logic, security, data access) that are under-covered.
   - Find untested functions and uncovered branches.

3. **If no coverage data exists:**
   - Generate the configuration needed to run coverage.
   - Provide the exact commands to generate a coverage report.
   - Explain how to integrate coverage into CI.

4. **Analyze gaps by priority:**

   **Critical (must test):**
   - Security-related code (authentication, authorization, input validation, encryption).
   - Data persistence (database writes, file operations, cache management).
   - Payment or financial logic.
   - Error handling and recovery paths.

   **High (should test):**
   - Core business logic.
   - API endpoint handlers.
   - Data transformation and serialization.
   - Configuration parsing.

   **Medium (nice to test):**
   - Utility functions.
   - Logging and monitoring.
   - UI formatting.

   **Low (consider deleting instead):**
   - Dead code that is never called.
   - Deprecated functions awaiting removal.

5. **Generate targeted tests** for the top 5 most critical uncovered areas.

6. **Provide coverage integration for CI:**
   - Add coverage measurement to the CI pipeline.
   - Set up per-file minimum thresholds (Chromium approach: >90% per file).
   - Configure coverage decrease detection on PRs.
   - Show how to add a coverage badge to README.

## Arguments

$ARGUMENTS

Examples:
- `/test-coverage` — Full project coverage analysis.
- `/test-coverage src/auth/` — Focus on the auth module.
- `/test-coverage --setup` — Set up coverage tooling from scratch.
- `/test-coverage --ci` — Generate CI coverage integration only.
