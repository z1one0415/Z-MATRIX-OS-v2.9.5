# R-Matrix v2.0-cycle-four-king Contract

## Service Entry
```python
evaluate_r_matrix_cycle(ticker, prices=None, position=None,
    daily_prices=None, weekly_prices=None, biweekly_prices=None, five_day_prices=None)
```

## Return Fields
| Field | Type | Description |
|------|------|------|
| ticker | str | Stock code |
| version | "v2.0-cycle-four-king" | Contract version |
| status | PASS/DEGRADED/DATA_GAP/ERROR | Overall status |
| legacy_fallback | False | Must be False |
| r_score | float\|None | Resonance score 0-10 |
| r_resonance_status | str | CYCLE_RESONANCE_STRONG/ENTRY/RIDE/BOX/CONFLICT/BLOCKED |
| r_action_cap | str | Entry action ceiling |
| entry_action_cap | str | Entry intent |
| exit_alert | NONE/WATCH_HARVEST/HARVEST/FORCE_HARVEST | Exit signal |
| hard_blocks | list[str] | Blocking cycle problems |
| conflicts | list[str] | Cycle conflicts (not blocking) |
| kings | dict | Four king results |
| sell_decision | dict\|None | Position sell decision |
| data_lineage | dict | Bar counts per king |
| errors | list[str] | Error messages |
| warnings | list[str] | Warning messages |

## Status Rules
- daily_bars < 20 → DATA_GAP
- king_count < 2 → DATA_GAP  
- king_count 2-3 → DEGRADED
- errors non-empty → DEGRADED
- 4 kings + no errors → PASS
- legacy_fallback=True → DEGRADED (must not happen)

## Consumers
- G09: full universe scheduler → r_pool
- G14: monthly baseline consumer → r_score/r_version
- G18: targeted signal consumer → g09_signal_adapter
