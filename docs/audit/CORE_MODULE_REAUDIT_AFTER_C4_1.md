# Core Module Re-Audit After C.4.1

Audit: 2026-05-30T16:28:19.291849+00:00

| Module | Before | After | Fix Verified | Verdict |
|--------|--------|-------|------------|:--:|
| account_truth | P1_BLOCKING | P1_FIXED | reconcile_trade_amount + reconcile_equit | PASS |
| market_data | P1_HIGH | P1_NON_BLOCKING | TEST_GAP_ONLY — generic PIT blocking exi | PASS |
| outcome_engine | P1_HIGH | P1_NON_BLOCKING | ACCEPTED_DESIGN_BOUNDARY — P3-C handles  | PASS |
| replay | P1_BLOCKING | P1_FIXED | RollingDataset raises ValueError on cal= | PASS_WITH_WATCH |
| master_data | P2_MEDIUM | P2_MEDIUM | — | PASS |
| attribution | P2_MEDIUM | P2_MEDIUM | — | PASS |
| council | P2_MEDIUM | P2_MEDIUM | — | PASS |

## Summary
- P0: 0 | P1_BLOCKING: 0 | P1_FIXED: 2 | P1_NON_BLOCKING: 2 | P2: 3

## Watch Items
- replay: malformed calendar — runner try/except catches generic ValueError. Adequate for C.5 but recommend dedicated test in C.5.1.
- market_data: price-specific PIT tests pending — non-blocking backlog item.