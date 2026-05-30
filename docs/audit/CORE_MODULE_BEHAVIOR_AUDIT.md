# CORE Module Behavior Audit

Audit: 2026-05-30T14:28:05.987209+00:00

## account_truth
- **purpose**: Reconstruct 5-year trading truth
- **input**: Trade CSV/Position CSV
- **output**: Capital curve, PnL ledger
- **key_logic**: FIFO cost basis, reconciliation
- **boundary_test**: ✅ has entry validation
- **fail_closed**: ✅ ERROR quality blocks analysis
- **hash**: ✅ via import_audit
- **risk**: P1: reconciliation false pass on tolerance

## master_data
- **purpose**: Security master + industry/chain mapping
- **input**: CSV fixtures
- **output**: SecurityMaster, mapping lookup
- **key_logic**: Ticker identity resolution, chain mapping
- **boundary_test**: ✅ duplicate/confidence checks
- **fail_closed**: ✅ missing mapping returns None
- **hash**: ✅ integrity checker
- **risk**: P2: chain taxonomy limited to 1 level

## market_data
- **purpose**: Price bars, trading calendar, benchmarks
- **input**: Price CSV, calendar CSV
- **output**: DailyPriceBar, TradingCalendar
- **key_logic**: T20/T60 strict forward days
- **boundary_test**: ✅ insufficient days blocked
- **fail_closed**: ✅ fallback_last_price_allowed=False
- **hash**: —
- **risk**: P0: PIT future leakage in price data

## outcome_engine
- **purpose**: Signal outcome horizon readiness
- **input**: Signal date + calendar
- **output**: T20/T60 readiness result
- **key_logic**: Strict forward trading day counting
- **boundary_test**: ✅ suspension/missing bar blocked
- **fail_closed**: ✅ INSUFFICIENT_FORWARD_DAYS
- **hash**: —
- **risk**: P1: no alpha/return in P3-B scope

## attribution
- **purpose**: Return decomposition
- **input**: Gross return + benchmark returns
- **output**: Market/Industry/Selection alpha
- **key_logic**: Brinson-style attribution
- **boundary_test**: ✅ total_attributed sum check
- **fail_closed**: —
- **hash**: ✅ attribution_packet
- **risk**: P2: double-counting risk in composite

## replay
- **purpose**: Experiment reproducibility
- **input**: Dataset slices
- **output**: ReplayResult + hash
- **key_logic**: Deterministic hash chain
- **boundary_test**: ✅ same input → same hash
- **fail_closed**: ✅ chain_verify fails on mismatch
- **hash**: ✅ replay_hash
- **risk**: P1: rolling replay without calendar

## council
- **purpose**: 12-seat multi-reviewer consensus
- **input**: ReviewContext
- **output**: CouncilDecision + minority report
- **key_logic**: Independent review aggregation
- **boundary_test**: ✅ devil advocate mandatory
- **fail_closed**: ✅ empty results → INSUFFICIENT_EVIDENCE
- **hash**: ✅ council_packet
- **risk**: P2: simple scoring weights, no calibration
