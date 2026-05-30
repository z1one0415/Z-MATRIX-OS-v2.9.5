# CORE Module Risk Register

| Module | Finding | Level | Triage | Blocking |
|--------|------|:--:|------|:--:|
| account_truth | Reconciliation tolerance may mask real errors | P1_HIGH | MUST_FIX_BEFORE_PACK_D | 🔴 |
| market_data | Price-specific PIT tests missing | P1_HIGH | TEST_GAP_ONLY |  |
| outcome_engine | Return/alpha/cost not in P3-B scope by design | P1_HIGH | ACCEPTED_DESIGN_BOUNDARY |  |
| replay | Rolling replay fails without calendar | P1_HIGH | MUST_FIX_BEFORE_PACK_D | 🔴 |
| master_data | Chain taxonomy 1-level depth only | P2_MEDIUM | NOT_TRIAGED |  |
| attribution | Double-counting risk in composite attribution | P2_MEDIUM | NOT_TRIAGED |  |
| council | Simple scoring weights, no calibration | P2_MEDIUM | NOT_TRIAGED |  |

## P0:0 | P1:4 | P2:3 | Blocking:2