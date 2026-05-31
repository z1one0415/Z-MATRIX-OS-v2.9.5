# V5 Entry Criteria

V5 (Real Return / Benchmark Alpha Calculation) requires:

| Gate | Requirement | Current |
|------|-------------|---------|
| daily_price_real_read_only | 12/12 | 0 ❌ |
| adjustment_factor_ready | 12/12 | 0 ❌ |
| benchmark_real_read_only | true | false ❌ |
| calendar_real_read_only | true | false ❌ |
| ready_for_real_return | 12/12 | 0 ❌ |
| ready_for_alpha_claim | 0 (still blocked) | 0 ✅ |

## How to pass

1. Prepare 4 CSV files per the [Core 12 CSV File List](CORE_12_REQUIRED_CSV_FILE_LIST.md)
2. Place them in `data/research_db/market_data/processed/`
3. Generate source_hash for each file
4. Run: `PYTHONPATH=. python3 scripts/cases/check_v5_entry_gate.py`
5. When all gates = true, V5 is unlocked

## Still NOT allowed in V5

- Alpha claims (ready_for_alpha_claim stays false)
- BUY/SELL instructions
- Broker/Runtime/RealTrade (stay BLOCKED)
- Council investment verdicts
