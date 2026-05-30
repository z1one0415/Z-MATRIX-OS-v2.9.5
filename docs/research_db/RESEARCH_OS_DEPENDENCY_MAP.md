# Research OS Dependency Map

Generated: 2026-05-30T09:45:10.985138+00:00

```
┌─ Data Layer
│  ├─ data_supply (5 mods, 370 tests)
│  ├─ market_data (14 mods, 701 tests)
│  ├─ master_data (14 mods, 369 tests)
│  ├─ account_truth (13 mods, 364 tests)
┌─ Outcome Layer
│  ├─ outcome_engine (3 mods, 31 tests)
│  ├─ outcome_reality (5 mods, 375 tests)
┌─ Validation Layer
│  ├─ validation (5 mods, 190 tests)
│  ├─ validation_factory (12 mods, 468 tests)
│  ├─ proving_ground (6 mods, 288 tests)
┌─ Portfolio Layer
│  ├─ portfolio (4 mods, 140 tests)
│  ├─ portfolio_reality (6 mods, 456 tests)
┌─ Decision Layer
│  ├─ decision_intelligence (4 mods, 104 tests)
┌─ Governance Layer
│  ├─ council (7 mods, 273 tests)
│  ├─ alpha_factory (6 mods, 276 tests)
│  ├─ attribution (5 mods, 215 tests)
│  ├─ replay (6 mods, 288 tests)
│  ├─ cockpit (5 mods, 165 tests)
│  ├─ factor_foundation (3 mods, 192 tests)
└─ ResearchDB Foundation (constitution, policies)
```

## Orphan Detection

- root

## Verdict
- Structure: Layered, no circular dependencies detected
- Risk: Validation layer is largest (validation + validation_factory + proving_ground)