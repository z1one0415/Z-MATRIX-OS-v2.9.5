# Case Expansion V4 — Market Data Contract

> Schema: v4.0 | Status: READY

## Source Status Enum

| Status | Meaning |
|--------|---------|
| REAL_READ_ONLY | Verified real data with hash/date |
| PUBLIC_READ_ONLY | Public market data |
| LOCAL_USER_PROVIDED | User CSV in processed/ |
| FIXTURE | Test fixture only |
| SYNTHETIC | Generated — invalid for investment |
| MISSING | Not available |
| BLOCKED | Access blocked |

## Required Fields

### daily_price_bar
ticker, trade_date, open, high, low, close, volume, amount, source_name, source_type, source_file, source_hash, as_of_date, adjusted

### adjustment_factor
ticker, trade_date, adjust_factor, factor_type, source_name, source_type, source_file, source_hash, as_of_date

## Hard Rules

1. REAL_READ_ONLY must have source_hash
2. REAL_READ_ONLY must have as_of_date
3. Missing fields must not be default-filled with 0
4. Missing prices must not be forward-filled
5. Missing adjustment_factor must not default to 1.0 unless EXPLICITLY_NOT_REQUIRED
6. raw/staging/vendor directories must not contain committed real data
7. source_type must not be SYNTHETIC for market data

## Templates

Available at `data/research_db/market_data/templates/`
