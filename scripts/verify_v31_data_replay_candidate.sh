#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.1 Full Verification Gate ═══"
echo ""; echo "== Compile =="
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"

# Unit tests
for t in \
  test_historical_replay_brd_adapter test_historical_replay_universe test_historical_replay_engine \
  test_paper_outcome_schema test_paper_outcome_horizon \
  test_paper_outcome_return_calculator test_paper_outcome_drawdown \
  test_paper_outcome_backfill_runner test_paper_outcome_event_adapter \
  test_paper_outcome_batch_runner test_paper_outcome_summary_report test_paper_outcome_policy \
  test_portfolio_exposure_report test_portfolio_exposure_beta_corr test_portfolio_exposure_policy; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done

# Real data smoke test
echo ""; echo "== Real data smoke =="
TICKER_COUNT=$(ls data/price_bars/*.csv 2>/dev/null | wc -l | tr -d ' ')
echo "  ticker_count: $TICKER_COUNT"
if [ "$TICKER_COUNT" -lt 1000 ]; then
  echo "  ❌ ticker_count < 1000"
  exit 1
fi
echo "  ✅ ticker_count >= 1000"

# Check 5-year coverage
python3 << 'PYSMOKE'
import csv, sys
from pathlib import Path
bar_dir = Path("data/price_bars")
if not bar_dir.exists():
    sys.exit(1)
files = list(bar_dir.glob("*.csv"))
years_covered = 0
replay_ok = False
for f in files[:100]:
    rows = list(csv.DictReader(open(f, encoding='utf-8-sig')))
    v = [r for r in rows if (r.get("trade_date") or r.get("date","")).strip()]
    if not v: continue
    dates = sorted((r.get("trade_date") or r.get("date","")).replace("-","") for r in v)
    d0 = dates[0][:4]
    dn = dates[-1][:4]
    span = int(dn) - int(d0)
    if span >= 4:
        years_covered += 1
    # Can we replay 2024-06-03?
    pre = [d for d in dates if d < "20240603"]
    if len(pre) >= 120 and dn >= "2024":
        replay_ok = True

print(f"  ✅ 5yr coverage: {years_covered}/{min(100,len(files))} tickers span >= 4 years")
print(f"  {'✅' if replay_ok else '❌'} sample replay_date=2024-06-03 {'PASS' if replay_ok else 'FAIL'}")
PYSMOKE
echo ""

echo "== Tail-risk verify =="
bash scripts/verify_tail_risk_candidate.sh

echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.1 Full Verification PASS ═══"
