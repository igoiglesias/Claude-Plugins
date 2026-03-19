---
description: Analyze the project's testing maturity level (1-4) and provide actionable recommendations based on world-class standards from SQLite, Chromium, NASA/JPL, and curl.
---

# Test Audit

## Purpose

Perform a comprehensive audit of the project's testing practices and assign a maturity level from 1 (Basic) to 4 (World-Class), with specific, prioritized recommendations for improvement.

## Instructions

1. **Discover the project structure:**
   - Identify the programming language(s) and framework(s) in use.
   - Locate test directories and test files (common patterns: `tests/`, `test/`, `__tests__/`, `*_test.go`, `*_test.py`, `*.test.ts`, `*.spec.ts`).
   - Identify CI/CD configuration files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `Makefile`, etc.).
   - Look for coverage configuration (`.coveragerc`, `jest.config.*`, `pyproject.toml [tool.coverage]`).
   - Check for static analysis config (`ruff.toml`, `.eslintrc`, `clippy.toml`, `.clang-tidy`, `sonar-project.properties`).
   - Check for fuzz testing targets or property-based tests.

2. **Analyze test quality:**
   - Count source files vs test files. Calculate the ratio.
   - Check if tests follow naming conventions (`test_<module>.py`, `<module>.test.ts`).
   - Look for test fixtures, factories, or builders (avoid hardcoded test data).
   - Check for regression tests (tests that reference bug IDs or issues).
   - Identify if tests cover error paths, not just happy paths.
   - Look for flaky test markers or quarantine mechanisms.

3. **Evaluate CI integration:**
   - Are tests gating (blocking merge) or advisory (run but don't block)?
   - Is coverage measured and reported?
   - Are static analyzers running in CI?
   - Is there any fuzz testing (continuous or scheduled)?
   - Are there performance benchmarks?

4. **Assign maturity level:**

   **Level 1 — Basic:**
   - Unit tests exist for some business logic.
   - Tests run in CI.
   - Tests must pass to merge.

   **Level 2 — Solid:**
   - Integration tests for DB/API/queue interactions.
   - Regression tests accompany bug fixes.
   - Coverage is measured and visible.
   - Static analysis runs in CI.
   - Test data is deterministic.

   **Level 3 — Strong:**
   - E2E tests for critical user journeys.
   - Fuzz testing on parsers/serializers/protocol handlers.
   - Multiple static analyzers.
   - Failure injection tests (OOM, I/O, network).
   - Performance benchmarks with regression detection.
   - Flaky test policy enforced.

   **Level 4 — World-Class:**
   - 100% branch or MC/DC coverage on critical paths.
   - Mutation testing validates test effectiveness.
   - Crash recovery testing.
   - Compound failure testing.
   - Cross-platform testing.
   - Pre-release soak testing.

5. **Generate the report** with this structure:
   - **Current Level**: X/4
   - **Score Breakdown** by category (coverage, CI, types of tests, tooling)
   - **Top 3 Priorities**: The highest-impact improvements to reach the next level
   - **Quick Wins**: Things that can be done in under 1 hour
   - **Strategic Improvements**: Larger investments for significant quality gains

## Arguments

$ARGUMENTS

If no arguments are provided, audit the entire project. If a specific module or directory is provided, focus the audit on that area.
