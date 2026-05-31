# Case Expansion V4 — Read-only Market Data Gate

> commit: $(git rev-parse --short HEAD)
> status: CASE_EXPANSION_V4_INFRASTRUCTURE_READY_BLOCKED_MISSING_MARKET_DATA

## Summary

| Metric | Value |
|--------|:-----:|
| Core 12 cases | 12 |
| Price REAL_READ_ONLY | 0 |
| Price FIXTURE | 1 (600519) |
| Price MISSING | 11 |
| Benchmark REAL | 0 |
| Calendar REAL | 0 |
| Return Ready | 1 (600519 with fixture) |
| Alpha Ready | 0 |

## V4 Infrastructure

- ✅ Market Data Contract (v4.0)
- ✅ CSV Import Templates (4 types)
- ✅ Schema Validator (SYNTHETIC blocked, hash required)
- ✅ Core 12 Data Loader + Readiness Checker
- ✅ Real Return Readiness Gate
- ✅ Raw/staging/vendor protected (no real data committed)

## Blocking Factor

**No real market data has been provided.** All 12 cases lack REAL_READ_ONLY price data. 
To advance, place CSV files in:
```
data/research_db/market_data/processed/
```
Using templates from:
```
data/research_db/market_data/templates/
```

## Safety

- buy_sell_instruction_count: 0
- Production: BLOCKED
- Broker/Runtime: BLOCKED
- Real Trade: BLOCKED
