# P1 Risk Triage Table

Audit: 2026-05-30T14:41:45.344790+00:00

| ID | Module | Finding | Decision | Blocking | Action |
|----|--------|------|----------|:--:|------|
| P1-001 | account_truth | Reconciliation tolerance may mask real e | MUST_FIX_BEFORE_PACK_D | 🔴 | Add strict reconciliation tests with known error i |
| P1-002 | market_data | Price-specific PIT tests missing | TEST_GAP_ONLY | 🟡 | Add 5+ price-specific PIT tests verifying as_of_da |
| P1-003 | outcome_engine | Return/alpha/cost not in P3-B scope by d | ACCEPTED_DESIGN_BOUNDARY | 🟡 | Document in architecture notes that P3-B is horizo |
| P1-004 | replay | Rolling replay fails without calendar | MUST_FIX_BEFORE_PACK_D | 🔴 | Add calendar=None guard in RollingDataset with exp |

## Summary
- MUST_FIX: 2 | TEST_GAP: 1 | ACCEPTED: 1
- Blocking Pack D: 2 | P0: 0 | P1 total: 4 | P2: 3

## Decision: 2 P1 blocking items. PACK_C2_PASS — proceed to Pack C.3 triage fix plan