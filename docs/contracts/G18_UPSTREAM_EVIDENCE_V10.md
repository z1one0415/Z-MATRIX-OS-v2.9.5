# G18 Upstream Evidence v1.0

## Sources
| Source | Adapter | Status | Trade? |
|--------|---------|--------|--------|
| G09 | targeted adapter | ✅ LIVE | No |
| G08 | narrative_adapter | placeholder | No |
| G11 | risk_adapter | placeholder | No |
| G14 | baseline_adapter | placeholder | No |
| Z16 | price_gate_adapter | placeholder | No |
| G17 | account_confirm_adapter | placeholder | No |

## Rules
- Aggregator never raises, never blocks G18
- Missing sources → written to missing_sources
- G11: STRONG_WARNING_ONLY, never hard veto
- Z16/G17: required=True, available=False, never real trade
- Evidence does NOT change action (only build_final_decision does)
