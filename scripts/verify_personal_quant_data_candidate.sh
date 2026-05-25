#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.9-dev Personal Quant Data Verification Gate ═══"
echo ""; echo "== Compile all =="; python3 -m compileall zmatrix tests scripts pipelines; echo "✅ compileall PASS"
for t in test_data_fact_schemas test_paper_trade_ledger test_outcome_backfill_runner \
  test_portfolio_exposure_calculation test_backtest_metrics test_lightweight_backtest \
  test_monthly_review test_personal_quant_data_architecture \
  test_investment_role_workflow_data_requirements; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Investment role verify =="; bash scripts/verify_investment_role_candidate.sh
echo ""; echo "== Git check =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
 git diff --check; [ -z "$(git status --short)" ] && echo "✅ clean" || { echo "❌ dirty"; exit 1; }
else echo "(non-git, skip)"; fi
echo ""; echo "═══ Personal Quant Data Verification PASS ═══"
