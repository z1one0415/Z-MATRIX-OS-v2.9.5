# Case Expansion V4.2 — User Market Data Import Pack

> Status: READY | Date: 2026-05-31

## What this pack provides

This pack tells you exactly what CSV files to prepare,
where to put them, what fields are required, and how to
validate them before entering V5.

## Quick Start

### Step 1: Read required CSV list
See: [Core 12 Required CSV File List](CORE_12_REQUIRED_CSV_FILE_LIST.md)

### Step 2: Prepare 4 CSV files
```
data/research_db/market_data/processed/
├── core12_daily_price_bar.csv         # 12 tickers × N days
├── core12_adjustment_factor.csv       # adjustment factors
├── benchmark_csi300_price.csv         # CSI300 benchmark
└── trading_calendar.csv               # SSE/SZSE/STAR calendar
```

### Step 3: Generate source_hash
```bash
PYTHONPATH=. python3 scripts/cases/generate_market_data_source_hash.py \
  data/research_db/market_data/processed/core12_daily_price_bar.csv
```
See: [Hash Guide](MARKET_DATA_HASH_GUIDE.md)

### Step 4: Validate
```bash
PYTHONPATH=. python3 scripts/cases/validate_user_market_data_import_pack.py
```

### Step 5: Check V5 entry
```bash
PYTHONPATH=. python3 scripts/cases/check_v5_entry_gate.py
```

## CSV Templates

Available at: `data/research_db/market_data/templates/`
- `daily_price_bar_template.csv`
- `adjustment_factor_template.csv`
- `benchmark_price_template.csv`
- `trading_calendar_template.csv`

## Rules

- source_type must NOT be SYNTHETIC
- source_hash must NOT be empty
- Missing fields must NOT be default-filled with 0
- raw/staging/vendor must NOT contain committed real data
- No BUY/SELL / Alpha claims / Broker / RealTrade

## Current State

- V5 entry: BLOCKED (waiting for user CSV files)
- Production/Broker/Runtime/RealTrade: BLOCKED
