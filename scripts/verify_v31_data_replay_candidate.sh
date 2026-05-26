#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.1 Data Replay + Outcome + Portfolio Verification ═══"
echo ""; echo "== Compile =="
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_historical_replay_brd_adapter test_historical_replay_universe test_historical_replay_engine \
  test_paper_outcome_schema test_paper_outcome_return_calculator test_paper_outcome_drawdown \
  test_paper_outcome_backfill_runner test_paper_outcome_event_adapter test_paper_outcome_policy \
  test_portfolio_exposure_report test_portfolio_exposure_policy; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.1 Verification PASS ═══"
