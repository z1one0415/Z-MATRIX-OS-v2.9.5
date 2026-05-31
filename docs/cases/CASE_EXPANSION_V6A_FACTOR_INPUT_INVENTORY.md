# V6-A Factor Input Inventory

## Goal
Inventory every candidate factor: what inputs it needs, which inputs are ready, which are missing.

## Current Real Inputs
- Core 12 daily price: REAL_READ_ONLY
- CSI300 benchmark: REAL_READ_ONLY
- Trading calendar: REAL_READ_ONLY
- Volume/amount fields: included in daily price CSV

## Missing Inputs
- Financial statements (all types)
- Valuation data (market cap, PE, PB)
- Shares outstanding / float shares
- Industry universe data

## Factor Stats
- 30 factors inventoried
- 12 REAL_READY (price-only, can calculate history)
- 4 PARTIAL_READY (volume/amount, limited interpretation)
- 12 MISSING_INPUT (financial/valuation/shares)
- 2 SYNTHETIC_BLOCKED (legacy synthetic)

## V6-A Boundary
- V6-A does NOT prove Alpha
- V6-A only proves which factors have inputs
- CAN_CALCULATE_HISTORY_ONLY is the max permission
- CAN_VALIDATE_FACTOR is NOT granted yet
- Council stays BLOCKED
