---
description: Create fuzz testing targets for parsers, serializers, protocol handlers, and input-processing code. Inspired by SQLite's dbsqlfuzz (1B mutations/day), Chromium's ClusterFuzz, and Google's OSS-Fuzz.
---

# Test Fuzz

## Purpose

Generate fuzz testing targets and property-based tests for code that processes external input — parsers, deserializers, validators, protocol handlers, file readers, API endpoints.

## Instructions

1. **Identify fuzz candidates in `$ARGUMENTS` or by scanning the project:**
   - Functions that parse or deserialize data (JSON, XML, CSV, YAML, binary formats).
   - Functions that validate user input (emails, URLs, dates, IDs).
   - Protocol handlers (HTTP, WebSocket, MQTT, custom protocols).
   - File readers and importers.
   - Query builders or template renderers.
   - Any function where the input comes from outside the trust boundary.

2. **Select the right fuzzing approach for the language:**

   **Python:**
   - Use **Hypothesis** for property-based testing (preferred for most cases).
   - Use **Atheris** for coverage-guided fuzzing (for C extensions or complex parsers).
   - Generate `@given()` decorators with appropriate strategies.
   - Define invariants that should always hold regardless of input.

   ```python
   from hypothesis import given, strategies as st, settings

   @settings(max_examples=1000)
   @given(st.text())
   def test_parse_email_never_crashes(raw_input):
       try:
           result = parse_email(raw_input)
       except ValidationError:
           pass  # expected for invalid input
       # invariant: function should never crash with unhandled exception
   ```

   **JavaScript/TypeScript:**
   - Use **fast-check** for property-based testing.
   - Generate `fc.assert(fc.property(...))` patterns.

   **Go:**
   - Use built-in `go test -fuzz` (Go 1.18+).
   - Generate `FuzzXxx(f *testing.F)` functions with seed corpus.

   **C/C++:**
   - Generate **libFuzzer** harnesses (`LLVMFuzzerTestOneInput`).
   - Include sanitizer flags in build instructions (ASan, MSan, UBSan).
   - Provide a seed corpus directory.

   **Rust:**
   - Use `cargo-fuzz` with `libfuzzer-sys`.
   - Generate `fuzz_target!` macros.

3. **For each target, generate:**
   - The fuzz test file itself.
   - A seed corpus (3-5 representative valid inputs + 2-3 edge cases).
   - Build/run instructions.
   - CI integration snippet (GitHub Actions / GitLab CI).
   - OSS-Fuzz integration instructions if the project is open-source.

4. **Define invariants to check during fuzzing:**
   - **Never crash**: No unhandled exceptions, no segfaults, no panics.
   - **No memory errors**: No leaks, no buffer overflows (if applicable).
   - **Idempotency**: `parse(serialize(parse(input))) == parse(input)`.
   - **Bounded output**: Output size should be proportional to input size.
   - **Consistent errors**: Invalid input should produce specific error types, not random failures.

5. **Include a torture test pattern** (inspired by curl):
   - For functions that allocate memory, generate a loop that makes each successive allocation fail.
   - Verify no corruption, leaks, or inconsistent state on any failure path.

## Arguments

$ARGUMENTS

Examples:
- `/test-fuzz src/parsers/json_parser.py` — Generate fuzz targets for the JSON parser.
- `/test-fuzz` — Scan the project and identify all fuzz-worthy candidates.
- `/test-fuzz --oss-fuzz` — Generate targets compatible with Google's OSS-Fuzz.
