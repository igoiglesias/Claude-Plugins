---
description: Generate comprehensive test files for specified modules with proper structure, naming conventions, and patterns following best practices from SQLite and NASA/JPL.
---

# Test Scaffold

## Purpose

Create well-structured test files for specified source modules, following the project's existing conventions or establishing new ones based on best practices.

## Instructions

1. **Identify the target:**
   - Parse `$ARGUMENTS` to determine which module(s), file(s), or directory to generate tests for.
   - If no argument is given, ask which module needs tests.

2. **Detect project conventions:**
   - Identify the test framework in use (pytest, Jest, Go testing, JUnit, etc.).
   - Find existing test files and match their structure (directory layout, naming, import patterns).
   - Check for shared fixtures or conftest files.
   - Detect if the project uses factories, builders, or raw fixtures.

3. **Generate test files following these principles:**

   **Structure:**
   - Mirror the source directory structure: `src/auth/login.py` → `tests/unit/auth/test_login.py`.
   - Separate unit, integration, and e2e tests into different directories when the project supports it.
   - Use descriptive names: `test_<action>_<condition>_<expected_result>`.

   **Content — For each public function/method, generate:**
   - **Happy path test**: Normal expected input → expected output.
   - **Edge case tests**: Empty input, None/null, boundary values (0, -1, MAX_INT), unicode strings.
   - **Error path tests**: Invalid input, permission errors, resource not found.
   - **At least 2 assertions per test function** (NASA/JPL "Power of 10" principle).

   **Patterns:**
   - Use AAA pattern: Arrange, Act, Assert.
   - One logical assertion per test (multiple related asserts are OK).
   - Independent tests — no shared mutable state.
   - Use fixtures/factories for test data, never hardcoded magic values.
   - Include docstrings explaining what each test verifies and why.

   **Markers/Tags:**
   - Mark slow tests (`@pytest.mark.slow`, `describe.skip`, etc.).
   - Mark tests by type (unit, integration, e2e).
   - Mark smoke tests for quick validation.

4. **Include test utilities if needed:**
   - Factories or builders for complex test data.
   - Custom assertions for domain-specific validations.
   - Fixtures for common setup/teardown.

5. **Output summary:**
   - List all files created.
   - Count of tests generated per category (happy path, edge case, error).
   - Suggested next steps (run the tests, check coverage, add integration tests).

## Arguments

$ARGUMENTS

Examples:
- `/test-scaffold src/auth/` — Generate tests for all modules in the auth directory.
- `/test-scaffold src/payments/checkout.py` — Generate tests for the checkout module.
- `/test-scaffold --integration src/api/` — Focus on integration tests for the API layer.
