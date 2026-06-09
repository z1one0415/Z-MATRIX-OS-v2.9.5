# Z9 Review Node Planning — DEGRADATION POLICY

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Degradation Overview

Degradation states control what Z9 can and cannot do. The default state is
DISABLED_DEFAULT_NOOP — Z9 produces no output unless explicitly activated.
Z9 reviews Z2 explanation quality ONLY. no_trade_result is always enforced.

## 2. Degradation States

| State | Action | Description |
|---|---|---|
| ALLOW_Z9_READONLY_REVIEW | Proceed | Normal readonly review allowed |
| ALLOW_Z9_DEGRADED_REVIEW | Proceed with warnings | Review with incomplete data |
| DENY_Z9_SOURCE_FORBIDDEN | Block | Input source not z9_review_snapshot_candidate |
| DENY_Z9_REAL_SOURCE_FORBIDDEN | Block | Real trade/broker data detected |
| DENY_Z9_OUTPUTS_UNSAFE | Block | Forbidden output fields would be emitted |
| DENY_Z9_TRADE_RESULT_FORBIDDEN | Block | trade_result data in input or output |
| DENY_Z9_EVIDENCE_INCOMPLETE | Block | Required evidence hashes missing |
| DENY_Z9_MEMORY_MUTATION_FORBIDDEN | Block | Memory write attempted |
| DENY_Z9_EXECUTION_FORBIDDEN | Block | Execution path detected |
| DISABLED_DEFAULT_NOOP | No-op | Default state, no review produced |

## 3. State Transitions

```
DISABLED_DEFAULT_NOOP (default)
  → ALLOW_Z9_READONLY_REVIEW (when valid snapshot received)
  → ALLOW_Z9_DEGRADED_REVIEW (when partial snapshot received)
  → DENY_* (when violation detected)

ALLOW_Z9_READONLY_REVIEW
  → produces review output
  → no trade_result ever

ALLOW_Z9_DEGRADED_REVIEW
  → produces partial review with gaps noted
  → degradation_reason_attribution explains

DENY_* states
  → immediate halt
  → failure_reason_candidate populated
  → no_trade_result = True
  → no further processing
```

## 4. Degradation Detection

Detection triggers:
- Input contains trade_result → DENY_Z9_TRADE_RESULT_FORBIDDEN
- Input contains broker_result → DENY_Z9_REAL_SOURCE_FORBIDDEN
- Input missing required hashes → DENY_Z9_EVIDENCE_INCOMPLETE
- Output would contain forbidden field → DENY_Z9_OUTPUTS_UNSAFE
- Memory write attempted → DENY_Z9_MEMORY_MUTATION_FORBIDDEN
- Execution path invoked → DENY_Z9_EXECUTION_FORBIDDEN
- Input is not z9_review_snapshot_candidate → DENY_Z9_SOURCE_FORBIDDEN

## 5. Degradation Response

When a DENY state is triggered:
1. Processing halts immediately
2. failure_reason_candidate is set to the DENY reason
3. review_label is set to EXPLANATION_REJECTED_UNSAFE_SOURCE
4. All no_* markers are True
5. z2_feedback_candidate is empty or contains only the rejection reason
6. Audit log records the DENY event
7. Z9 feedback is advisory and readonly

## 6. Recovery from Degradation

- DENY states are terminal for that review invocation
- A new z9_review_snapshot_candidate can trigger a fresh review
- No state persists between invocations (stateless)
- DISABLED_DEFAULT_NOOP is always the starting state
- No automatic retry or escalation

## 7. Degradation Testing

Future tests must cover:
- Each DENY state triggered correctly
- DISABLED_DEFAULT_NOOP produces no output
- ALLOW_Z9_READONLY_REVIEW produces valid output
- ALLOW_Z9_DEGRADED_REVIEW produces partial output with warnings
- Multiple DENY conditions simultaneously handled
- No execution path survives any degradation state
- trade_result in any position triggers DENY_Z9_TRADE_RESULT_FORBIDDEN
