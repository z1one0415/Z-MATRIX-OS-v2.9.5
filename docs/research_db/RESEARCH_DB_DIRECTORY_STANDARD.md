# ResearchDB Directory Standard

## Root

```
data/research_db/
```

## Subdirectories

| Directory | Purpose | Phase |
|------|------|:--:|
| account/ | Account truth, trades, positions, capital curve | Phase 1 |
| universe/ | Security master, industry, chain, benchmark mapping | Phase 2 |
| market/ | Daily prices, indices, benchmark, limit/suspension | Phase 3 |
| finance/ | Financial snapshots, valuation, B-Matrix | Phase 7 |
| signal/ | Manual decisions, thesis, human actions | Phase 1 |
| outcome/ | Signal/trade/watchlist outcomes, benchmark alpha | Phase 3 |
| factor/ | Factor registry, IC/RankIC, promotion | Phase 4 |
| event/ | Catalyst events, scheduled calendar, decay | Phase 6 |
| caseforge/ | AutoCase events, cases, decisions, outcomes | Phase 5 |
| knowledge/ | Industries, chains, company profiles, methodology | Phase 8 |

## File Naming

- Normalized data: `*_ledger.csv` or `*.parquet`
- Reports: `*_report.md`
- Staging: `staging/imported_*_raw.csv`
- Raw: `raw/` (gitignored)

## .gitignore Rules

```
data/research_db/account/raw/
data/research_db/*/staging/
*.xlsx
*.xls
```
