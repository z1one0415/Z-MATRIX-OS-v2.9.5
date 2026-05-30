# CORE Module Risk Register

Audit: 2026-05-30

| Module | Finding | Level |
|--------|------|:--:|
| market_data | PIT price data protection EXISTS (verified in data_supply/pit_store). Risk: need price-specific PIT tests. | P1_HIGH |
| account_truth | Reconciliation tolerance may mask real errors | P1_HIGH |
| outcome_engine | Return/alpha/cost not in P3-B scope by design | P1_HIGH |
| replay | Rolling replay fails without calendar | P1_HIGH |
| master_data | Chain taxonomy 1-level depth only | P2_MEDIUM |
| attribution | Double-counting risk in composite attribution | P2_MEDIUM |
| council | Simple scoring weights, no calibration | P2_MEDIUM |

## Summary
- P0: 0 | P1: 4 | P2: 3