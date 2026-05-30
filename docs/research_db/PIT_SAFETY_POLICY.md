# PIT Safety Policy

## Definition

PIT = Point-in-Time. Data that was knowable at a given trade_date.

## PIT Statuses

| Status | Meaning |
|--------|---------|
| PIT_SAFE | as_of_date <= trade_date |
| PIT_UNSAFE | as_of_date > trade_date, but not blocked |
| CURRENT_SNAPSHOT_ONLY | Current snapshot, not historical |
| UNKNOWN_PIT_STATUS | No as_of_date |
| BLOCKED_FOR_BACKTEST | as_of_date > trade_date, blocked |

## Rules

1. Current financial snapshots default to CURRENT_SNAPSHOT_ONLY.
2. No as_of_date → UNKNOWN_PIT_STATUS.
3. as_of_date > trade_date → BLOCKED_FOR_BACKTEST.
4. News/announcements must have event_time or publish_time.
5. Manual data must be marked manual_reconstructed=true.
6. PIT_UNSAFE data must not enter historical backtesting.
7. UNKNOWN_PIT_STATUS must not enter factor validation.
8. fallback_last_price_allowed is always false for T20/T60.
