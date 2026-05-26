#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.1 Full Verification Gate ═══"
echo ""; echo "== Compile =="
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in \
  test_historical_replay_brd_adapter test_historical_replay_universe test_historical_replay_engine \
  test_paper_outcome_schema test_paper_outcome_horizon \
  test_paper_outcome_return_calculator test_paper_outcome_drawdown \
  test_paper_outcome_backfill_runner test_paper_outcome_event_adapter \
  test_paper_outcome_batch_runner test_paper_outcome_summary_report test_paper_outcome_policy \
  test_portfolio_exposure_report test_portfolio_exposure_beta_corr test_portfolio_exposure_policy; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Tail-risk verify =="
bash scripts/verify_tail_risk_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.1 Full Verification PASS ═══"
