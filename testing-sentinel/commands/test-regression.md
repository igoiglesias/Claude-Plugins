---
description: Generate a regression test from a bug description, issue number, or error trace. Follows the discipline of PostgreSQL and Chromium where every bug fix ships with a test.
---

# Test Regression

## Purpose

Create a regression test that reproduces a specific bug, to be committed alongside the fix. This ensures the exact bug never recurs — the core discipline of every well-tested project.

## Instructions

1. **Parse the bug information from `$ARGUMENTS`:**
   - A bug description in natural language.
   - An issue number or link.
   - A stack trace or error message.
   - A failing input example.

2. **Understand the bug:**
   - Identify the affected module/function.
   - Determine the root cause (or hypothesize if not yet fixed).
   - Identify the minimal input that triggers the bug.
   - Understand the expected vs actual behavior.

3. **Generate the regression test following this pattern:**

   ```python
   def test_issue_XXXX_<brief_description>():
       """
       Regression: <one-line description of the bug>.
       
       Root cause: <explanation of why it happened>.
       See: <issue link or reference>
       Fixed in: <commit hash or PR, to be filled after fix>
       """
       # Arrange: minimal setup to reproduce
       input_data = <the exact input that triggered the bug>
       
       # Act: call the function that was broken
       result = function_under_test(input_data)
       
       # Assert: verify the bug is fixed
       assert result == expected_value  # this used to <crash/return wrong value/hang>
   ```

4. **The regression test MUST:**
   - Reference the original bug (issue number, description, or error).
   - Use the minimal input that reproduces the bug.
   - Fail BEFORE the fix is applied (verify this if possible).
   - Pass AFTER the fix is applied.
   - Be placed in the appropriate test file (near related tests).
   - Include a clear docstring explaining what bug it prevents.

5. **If the bug involves edge cases, also generate:**
   - Boundary value tests around the fix.
   - A property-based test that would catch similar bugs (if applicable).
   - Negative tests ensuring the error is handled gracefully.

6. **Output:**
   - The test file with the regression test.
   - Instructions to verify the test fails before the fix.
   - Suggested location for the test file.

## Arguments

$ARGUMENTS

Examples:
- `/test-regression "Empty input causes division by zero in calculate_average()"` 
- `/test-regression #1234` — Generate from issue number (will search codebase for context).
- `/test-regression "TypeError: cannot unpack non-sequence NoneType at line 42 of parser.py"`
