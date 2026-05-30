# Research OS Golden Path — 贵州茅台 (600519)

## Executive Summary
This document traces one complete research cycle through the Research OS V3 pipeline.
Target: Kweichow Moutai (600519.SH)

## Pipeline Stages

### Stage 1: IDEA (Research Session)
```
ResearchSession(session_id='MT-001', ticker='600519', benchmark_id='CSI300')
```

### Stage 2: DATA (Master Data + Market)
```
SecurityMasterRegistry → get_by_ticker('600519') → listing_status=LISTED, board=MAIN
IndustryTaxonomy → get_industry('600519') → sw_l1=食品饮料
PriceBarStore → get_bars('600519', '2024-01-02', '2024-06-28') → 120 bars
```

### Stage 3: FACTOR (Factor Foundation)
```
FactorMetricsEngine → compute_ic(price_momentum, forward_returns) → IC=0.045
FactorValidator → validate → passed=True (IC>=0.02, coverage>=0.3)
```

### Stage 4: OUTCOME (Horizon Engine)
```
OutcomeHorizonEngine → evaluate_horizon('600519', '2024-01-02', 'T20') → READY
T20 exit_date: 2024-01-30, T60: blocked (INSUFFICIENT_FORWARD_DAYS)
```

### Stage 5: ATTRIBUTION
```
AttributionEngine → decompose → market_contribution=0.02, selection_alpha=0.03
Net return: gross=0.10, cost_drag=0.003, net=0.097
```

### Stage 6: REPLAY
```
ReplayDataset → slice_by_date('2024-01-02', '2024-06-28', ['600519'])
WalkForwardCertifier → certify → PASS, cert_grade=A, overfit_score=0.12
```

### Stage 7: COUNCIL
```
12-Seat Council → aggregate → PASS (8 pass, 2 conditional, 2 fail + minority opinions)
Devil Advocate → challenges: [Low coverage in Bear regime]
```

### Stage 8: DECISION
```
PredictionMarket → consensus=UP (forecaster_count=5, agreement=0.80)
DecisionLedger → record('D1', '600519', 'BUY', thesis='T1', reason='IC=0.045, selection_alpha=0.03')
```

### Stage 9: MEMORY
```
MemoryBank → store('M1', 'MT-001', 'THESIS', content, result='WINNER')
LessonExtractor → extract → category=FACTOR_EDGE, cause='IC=0.045'
PatternLibrary → register pattern 'Momentum Edge in Consumer Staples'
```

## Golden Path Audit Hash
> `GOLDEN_PATH_MT_001: a3f8c2d1e4b5f6a7`