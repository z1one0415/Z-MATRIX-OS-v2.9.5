# ZC40 LIMIT BOARD FILLABILITY PROTOCOL V10

## Problem
A-share one-price limit-up boards are NOT tradable.
System may correctly identify positive catalyst but cannot execute.

## Detection
- One-price board: open=high=low=close AND pct_change >= 9.8%
- Consecutive limit-up: N consecutive days of limit-up
- Open board: limit-up opens (gap up but tradable)

## Fillability Status
- NOT_FILLABLE: one-price board, cannot enter
- WAIT_OPEN_BOARD: wait for board to open before entry
- OPEN_BOARD_CONFIRMATION_REQUIRED: board opened, needs confirmation
- CHASE_RISK: entered after multiple boards, high chase risk
- LIQUIDITY_TRAP: volume collapse after board open
- PAPER_ONLY_OBSERVE: observe only, no paper entry
- DATA_INSUFFICIENT: cannot determine

## Hard Rules
1. NOT_FILLABLE → BLOCK new entry
2. CHASE_RISK → WATCH_ONLY or paper-observe
3. Consecutive > 3 limit-up boards → integrate ZC35 residual_power
4. Board open without volume confirmation → WAIT
