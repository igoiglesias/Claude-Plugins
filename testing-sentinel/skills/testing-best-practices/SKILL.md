---
name: testing-best-practices
description: Comprehensive testing knowledge base drawn from SQLite, Linux Kernel, Chromium, NASA/JPL, curl, PostgreSQL, and Redis. PROACTIVELY activate when Claude detects tasks involving writing tests, setting up test frameworks, configuring CI/CD pipelines, reviewing test quality, discussing code coverage, fixing flaky tests, creating fuzz targets, implementing failure injection, choosing test tools, designing test architectures, or any conversation about software quality, test strategy, or regression prevention.
version: 1.0.0
---

# Testing Best Practices — World-Class Reference Guide

This skill provides Claude with comprehensive testing knowledge distilled from the most reliable software projects ever built. Use this knowledge to guide all testing-related decisions.

## Reference Projects Quick Facts

| Project | Key Metric | Signature Technique |
|---------|-----------|-------------------|
| **SQLite** | 590:1 test-to-code ratio, 100% MC/DC | OOM/crash/I/O failure injection, mutation testing |
| **Linux Kernel** | 8,400+ bugs found by syzbot | Syzkaller fuzzing, KASAN/KMSAN/KCSAN sanitizers |
| **Chromium** | 30,000 VMs fuzzing, >90% per-file coverage | ClusterFuzz, Commit Queue gates, LUCI CI |
| **NASA/JPL** | 5+ static analyzers on all flight code | "Power of 10" rules, zero-warning policy |
| **curl** | 970K tests/day, 161 CI configs | Torture tests (sequential failure), custom test servers |
| **PostgreSQL** | Patches without tests = WIP | Isolation tests, Buildfarm, SQLsmith fuzzer |
| **Redis** | Fuzz-first philosophy | Client-server test architecture |

## Principles (Apply These Always)

### 1. Multiple Independent Verification Methods
No single test type finds all bugs. Use unit + integration + E2E + fuzz + static analysis together. SQLite uses 4 independent test harnesses. NASA uses 5+ static analyzers in parallel.

### 2. Failure Injection > Happy-Path Testing
Systematically test what happens when things go wrong. OOM, I/O errors, network failures, crashes, and compound failures catch the most critical bugs. Redis's creator says fuzz tests found almost all bugs, not unit/regression tests.

### 3. Tests Must Gate the Process
Tests that don't block merges degrade over time. Chromium's Commit Queue blocks every merge. PostgreSQL treats patches without tests as WIP. Make tests mandatory, not advisory.

### 4. Coverage Is a Compass, Not a Destination
Track per-file coverage (Chromium: >90%) and watch for decreases in PRs. Don't worship the global number — a project at 85% can have a critical module at 20%. Use coverage to find blind spots, then decide if they matter.

### 5. Every Bug Fix Ships With a Regression Test
Write a test that fails before the fix and passes after. Reference the bug. Commit both together. This is non-negotiable in PostgreSQL, Chromium, and curl.

### 6. Fuzz Testing Is Mandatory for External Input
Any code that processes external input (parsers, validators, deserializers, protocol handlers) must be fuzzed. The tooling is mature, free (OSS-Fuzz), and the bugs are real.

## Test Types Reference

### Unit Tests
- **Purpose**: Verify individual functions/methods in isolation.
- **Pattern**: AAA (Arrange, Act, Assert). One concern per test.
- **Naming**: `test_<action>_<condition>_<expected_result>`.
- **NASA rule**: At least 2 assertions per function.
- **Speed**: Should run in milliseconds. If a "unit test" takes seconds, it's an integration test.

### Integration Tests
- **Purpose**: Verify how modules work together (DB, API, queues).
- **Use real dependencies when feasible**, mocks when necessary.
- **Test the contract** between components, not internals.
- **Clean up**: Truncate tables, delete temp files, reset queues after each test.

### End-to-End (E2E) Tests
- **Purpose**: Verify complete user workflows.
- **Focus on critical paths** (login, checkout, data export).
- **Use deterministic data and environments**. Flaky E2E tests erode trust.
- **Run in production-like environments**.

### Fuzz Tests
- **Purpose**: Find crashes, memory errors, and unexpected behavior with random/semi-random input.
- **Tools**: libFuzzer, AFL++, Hypothesis, fast-check, go-fuzz, Atheris.
- **Invariants**: Never crash, no memory errors, bounded output, consistent errors.
- **Run continuously** (not per-PR). 10 min minimum, ideally 24/7.
- **Structure-aware fuzzing** for protocols and file formats.

### Property-Based Tests
- **Purpose**: Verify properties that hold for ALL valid inputs.
- **Tools**: Hypothesis (Python), fast-check (JS/TS), proptest (Rust), rapid (Go).
- **Examples**: `parse(serialize(x)) == x`, `len(sort(x)) == len(x)`, `min(x) <= avg(x) <= max(x)`.

### Failure Injection Tests
- **OOM**: Make each allocation fail sequentially. Verify no corruption at each step.
- **I/O**: Mock filesystem to fail on read/write. Verify data integrity.
- **Network**: Simulate timeouts, resets, DNS failures. Verify retry and fallback logic.
- **Crash**: Kill process mid-operation. Verify consistent state on restart.
- **Compound**: Combine failures (OOM during crash recovery).

### Mutation Tests
- **Purpose**: Verify tests actually detect code changes.
- **Tools**: mutmut (Python), Stryker (JS), PITest (Java), cargo-mutants (Rust).
- **Target**: 80%+ mutation score on core business logic.
- **Run on critical modules**, not the entire codebase (it's slow).

### Static Analysis
- **Purpose**: Catch bugs without running code.
- **Use multiple tools** (NASA approach):
  - Linter (ruff, eslint, clippy)
  - Type checker (mypy, tsc --strict)
  - Security scanner (bandit, semgrep)
  - Deep analyzer (cppcheck, SonarQube)
- **Run in CI**. Zero-warning policy for new code.

### Performance Tests
- **Types**: Load, stress, soak, benchmark.
- **Establish baselines**. Automate regression detection.
- **Set performance budgets**. Fail the build if exceeded.
- **Chromium approach**: Continuous perf testing with automatic bisection.

## CI Pipeline Template

```
Stage 1 (< 2 min): Lint + Static Analysis + Type Check
  → Fail fast. If code doesn't parse, don't waste time testing it.

Stage 2 (< 5 min): Unit Tests + Coverage Report
  → Block merge on failure. Report per-file coverage in PR.

Stage 3 (< 15 min): Integration Tests
  → Block merge on failure. Use containers for dependencies.

Stage 4 (< 30 min): E2E Tests
  → Run on merge to main or as required by project risk level.

Stage 5 (Continuous): Fuzz Tests
  → Run 24/7 on dedicated infrastructure or nightly in CI.
  → Alert on new crashes. Auto-file bugs.

Stage 6 (Weekly): Mutation Tests + Performance Benchmarks
  → Track trends. Alert on significant regressions.
```

## Test Data Guidelines

- **Never use production data in tests.** Use factories/fixtures.
- **Use seeds for random data.** Log the seed so failures reproduce.
- **Isolate environments.** Each test run starts from a known state.
- **Custom test servers** (curl approach) beat mocks for protocol testing.

## Flaky Test Policy

- **Detection**: Track test pass/fail rate. Any test with <99% pass rate is flaky.
- **Quarantine**: Move to a separate test suite within 24 hours.
- **Fix or delete**: 1-week SLA. A flaky test is worse than no test.
- **Prevention**: No sleep/wait in tests, no external dependencies, no order coupling.

## Tools Quick Reference

| Category | Python | JS/TS | Go | Rust | C/C++ | Java | PHP |
|----------|--------|-------|-----|------|-------|------|-----|
| Unit | pytest | Jest/Vitest | testing | cargo test | GTest/Catch2 | JUnit | PHPUnit/Pest |
| Coverage | pytest-cov | c8/istanbul | go cover | tarpaulin | gcov/llvm-cov | JaCoCo | phpunit --coverage |
| Fuzz | Hypothesis/Atheris | fast-check | go fuzz | cargo-fuzz | libFuzzer/AFL++ | Jazzer | — |
| Mutation | mutmut | Stryker | — | cargo-mutants | mull | PITest | Infection |
| Static | ruff+mypy+bandit | eslint+tsc | go vet+staticcheck | clippy | clang-tidy+cppcheck | SpotBugs | PHPStan/Psalm |
| Load | Locust | k6/Artillery | — | — | — | Gatling | — |
