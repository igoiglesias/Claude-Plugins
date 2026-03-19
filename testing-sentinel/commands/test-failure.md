---
description: Create failure injection tests that verify your code handles crashes, OOM, I/O errors, and network failures gracefully. Inspired by SQLite's OOM/crash/I/O testing and curl's torture tests.
---

# Test Failure

## Purpose

Generate failure injection tests that systematically verify your code handles error conditions correctly — out-of-memory, I/O failures, network timeouts, corrupt data, and crash recovery.

## Instructions

1. **Identify failure injection candidates from `$ARGUMENTS` or by scanning:**
   - Functions that allocate significant resources (memory, file handles, connections).
   - Database operations (transactions, migrations, bulk inserts).
   - File operations (read, write, create, delete).
   - Network operations (API calls, WebSocket connections, email sending).
   - State-changing operations that should be atomic (transfers, order processing).
   - Long-running operations that could be interrupted.

2. **Generate tests for each failure category:**

   **OOM / Resource Exhaustion (SQLite pattern):**
   - Mock the allocator/resource to fail after N operations.
   - Loop through every possible N until the operation completes.
   - Verify: no corruption, no leaked resources, clean state after each failure.

   ```python
   def test_process_data_handles_oom_at_every_allocation():
       for fail_at in range(1, 100):
           mock_allocator.fail_after(fail_at)
           try:
               result = process_data(large_input)
           except MemoryError:
               assert system.is_consistent(), f"Corruption after OOM at allocation {fail_at}"
               assert no_resources_leaked(), f"Leak after OOM at allocation {fail_at}"
           else:
               break  # operation completed successfully
   ```

   **I/O Error Testing:**
   - Mock file system to fail on read/write/flush/close.
   - Test: partial writes, corrupt reads, permission denied, disk full.
   - Verify: data integrity, proper cleanup, meaningful error messages.

   **Network Failure Testing:**
   - Simulate: connection timeout, connection reset, DNS failure, slow responses.
   - Test retry logic, circuit breakers, fallback mechanisms.
   - Verify: no data loss, proper timeout handling, graceful degradation.

   **Crash Recovery Testing (SQLite pattern):**
   - Start an operation, simulate a crash at random points.
   - Restart and verify: data is consistent (either fully committed or fully rolled back).
   - For databases: use `PRAGMA integrity_check` equivalent.
   - For file systems: verify no partially-written files corrupt state on restart.

   **Compound Failure Testing (SQLite's advanced pattern):**
   - Combine multiple failure modes: OOM during crash recovery, I/O error during retry.
   - These catch the most subtle bugs that only appear under cascading failures.

   ```python
   def test_recovery_handles_oom_during_crash_replay():
       # First: simulate a crash during a write
       simulate_crash_during(write_operation, crash_at_step=3)
       
       # Then: during recovery, simulate OOM
       for fail_at in range(1, 50):
           mock_allocator.fail_after(fail_at)
           try:
               recovery_result = recover_from_crash()
           except MemoryError:
               assert database.integrity_check(), f"Corruption after OOM during recovery"
           else:
               assert recovery_result.is_consistent()
               break
   ```

3. **Generate test utilities:**
   - A mock allocator/resource manager that can be configured to fail at specific points.
   - A mock file system layer for I/O error injection.
   - A mock HTTP client for network failure simulation.
   - Helpers for verifying system consistency after failures.

4. **Include CI integration:**
   - These tests are typically slower — tag them appropriately.
   - Run in CI on merge to main or nightly, not on every PR (unless the project requires it).
   - Provide timeout configuration (failure injection loops can run long).

5. **Output:**
   - Test files organized by failure category.
   - Test utility modules for mocking failures.
   - CI configuration snippet.
   - Explanation of each failure scenario and what it catches.

## Arguments

$ARGUMENTS

Examples:
- `/test-failure src/database/transactions.py` — Generate failure tests for database transactions.
- `/test-failure --oom src/parsers/` — Focus on OOM testing for parsers.
- `/test-failure --network src/api/client.py` — Network failure tests for an API client.
- `/test-failure` — Scan the project and identify top failure injection candidates.
