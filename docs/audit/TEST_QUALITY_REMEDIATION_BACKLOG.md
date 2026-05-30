# Test Quality Remediation Backlog

## P0: Safety + Fail-Closed
1. Add fail-closed tests for PIT store future-blocking
2. Add safety tests for all output dataclasses (production_allowed=False)
3. Add hash chain integrity tests for all ledgers

## P1: Core Computation Logic
4. Add IC/RankIC edge case tests (constant series, None values)
5. Add Drawdown recovery detection tests
6. Add Capacity migration tests (1M→1B)

## P2: Reduce Existence Tests
7. Replace `test_x_exists` with behavioral assertions
8. Convert fixture-load tests to computation-verify tests

## P3: De-duplication
9. Identify and merge duplicate test patterns
10. Consolidate safety_flag tests into shared fixture
