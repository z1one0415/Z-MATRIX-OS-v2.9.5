# Factor Lifecycle State Machine

## States

```
NOT_EXECUTED
    → SOURCE_READINESS_CHECK
    → SOURCE_BLOCKED
    → MATERIALIZATION_PENDING
    → MATERIALIZED
    → PIT_VALIDATED
    → COVERAGE_VALIDATED
    → MATURE
    → CANDIDATE_REVIEWED
    → FROZEN_CANDIDATE
    → FROZEN_MONITORING
    → PROMOTION_REVIEW
    → PROMOTED ← FORBIDDEN until F3.6+OOS+monitoring pass
    → REJECTED (terminal)
    → HYPOTHESIS_ONLY (terminal for planned-but-not-materialized)
```

## Transitions

| From | To | Gate |
|------|----|------|
| NOT_EXECUTED | SOURCE_READINESS_CHECK | source contract |
| SOURCE_READINESS_CHECK | MATERIALIZATION_PENDING | source ready |
| SOURCE_READINESS_CHECK | SOURCE_BLOCKED | source blocked |
| MATERIALIZATION_PENDING | MATERIALIZED | materialization executed |
| MATERIALIZED | PIT_VALIDATED | PIT pass |
| PIT_VALIDATED | COVERAGE_VALIDATED | coverage pass (U400/U450/U475) |
| COVERAGE_VALIDATED | MATURE | single-factor validation executed |
| MATURE | CANDIDATE_REVIEWED | candidate review pass |
| CANDIDATE_REVIEWED | FROZEN_CANDIDATE | freeze review pass |
| FROZEN_CANDIDATE | FROZEN_MONITORING | monitoring plan built |
| FROZEN_MONITORING | PROMOTION_REVIEW | OOS + monitoring pass |
| PROMOTION_REVIEW | PROMOTED | 🔴 FORBIDDEN (not available) |

## Forbidden States

- `PROMOTED` — Not allowed for any current factor
- `LIVE` — Not allowed
- `TRADE_READY` — Not allowed

## Pre-Interface State

Factors with `pre_interface_artifacts: true` have materialization/validation executed but have NOT been backfilled to interface v1. They are blocked from entering CANDIDATE_REVIEWED until backfilled.
