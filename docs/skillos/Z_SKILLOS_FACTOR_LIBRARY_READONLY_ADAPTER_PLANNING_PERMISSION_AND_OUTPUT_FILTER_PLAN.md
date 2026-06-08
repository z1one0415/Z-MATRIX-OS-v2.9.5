# Factor Library Read-Only Adapter Planning — Permission and Output Filter Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_PERMISSION_AND_OUTPUT_FILTER_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan permission tiers and output filtering for the factor read-only adapter. No execution tier.

### Permission Tiers
| Tier | Access | Example |
|:--:|:--|:--|
| T0 | Manifest & registry only | list_factors |
| T1 | + Family profile (read-only) | get_factor_profile |
| T2 | + Evidence & validation | get_factor_evidence, validation summary |
| T3 | + Guardrail details | guardrail profile, risk flags |
| — | EXECUTION (forbidden) | No tier allows execution |

### Output Filters (must remove)
| Field | Source | Removal Action |
|:--|:--|:--|
| alpha_claim | Factor output | Strip from response |
| position_weight | Factor output | Strip from response |
| buy_signal | Factor output | Strip from response |
| sell_signal | Factor output | Strip from response |
| expected_return_claim | Factor output | Strip from response |

### Blocked Downstream Consumers
| Consumer | Block reason |
|:--|:--|
| Z8_EXECUTION_RUNTIME | No execution |
| V3_TRADE_SANDBOX | No paper trading |
| BROKER | No broker access |
| REAL_TRADE | Level 5 BLOCKED |

### Degraded States for Denied Factors
DENY_FACTOR_NOT_FOUND → DENY_NOOP
DENY_FACTOR_NOT_VALIDATED → DENY_NOOP
DENY_PIT_FAILED → PLAN_ONLY (can plan, cannot execute)
DENY_COVERAGE_FAILED → PLAN_ONLY
DENY_FAMILY_OVERLAP → DENY_NOOP
DENY_GUARDRAIL_FAILED → DENY_NOOP
DENY_PROMOTION_NOT_ALLOWED → DENY_NOOP
DENY_EXECUTION_FORBIDDEN → DENY_NOOP

## Boundary: No implementation. Level 5 BLOCKED.

## Next: Test and Proof Plan.

> Factor Library | Planning | Permission/Output Filter | FUTURE_PLAN_ONLY | Level 5 BLOCKED