# Pack C.3 Blocking Risk Fix Plan

Audit: 2026-05-30T15:33:03.208800+00:00

## Scope
- 2 blocking P1 risks only
- Fix PLAN, not implementation
- No code changes in Pack C.3

## P1-001: account_truth
- **Finding**: Reconciliation tolerance may mask real errors
- **Fix Goal**: Account reconciliation must not false-PASS due to over-wide tolerance
- **Behavior Modes**: 5 acceptance criteria
- **Acceptance Criteria**:
  1. Amount difference > tolerance → ERROR status
  1. Amount difference <= tolerance → PASS but record difference
  1. Tolerance must NOT default to infinite
  1. Reconciliation report must output difference_abs, difference_pct, tolerance_used
  1. Known mismatch fixture triggers FAILED not PASS
- **Regression Tests**: 5
- **Deadline**: Pack C.4

## P1-004: replay
- **Finding**: Rolling replay fails without calendar
- **Fix Goal**: Rolling replay must FAIL_CLOSED when calendar is missing or malformed
- **Behavior Modes**: 5 acceptance criteria
- **Acceptance Criteria**:
  1. calendar=None → FAIL_CLOSED (not 0 slices, not COMPLETED)
  1. Malformed calendar → FAIL_CLOSED
  1. Valid calendar → normal rolling slices produced
  1. Audit closeout records calendar dependency
  1. No silent empty result on calendar failure
- **Regression Tests**: 5
- **Deadline**: Pack C.4

## Next
Pack C.4: Blocking Risk Fix Implementation (actual code + test changes)
Production/Broker/Runtime/RealTrade: BLOCKED