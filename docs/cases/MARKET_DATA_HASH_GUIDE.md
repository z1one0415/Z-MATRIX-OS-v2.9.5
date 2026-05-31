# Market Data Hash Guide

## Why
Every REAL_READ_ONLY data file must carry a source_hash
to prove it wasn't tampered with after import.

## How
```bash
PYTHONPATH=. python3 scripts/cases/generate_market_data_source_hash.py \
  data/research_db/market_data/processed/core12_daily_price_bar.csv
```

Output:
```
sha256: abc123def456...
rows: 245
file: data/research_db/market_data/processed/core12_daily_price_bar.csv
```

Copy the sha256 value into the CSV's `source_hash` column.

## Rules
- Hash is calculated from the CSV content (excluding the source_hash column itself)
- Same content = same hash
- If source_hash in CSV differs from computed hash → validation fails
