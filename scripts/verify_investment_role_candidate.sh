#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.8-dev Investment Role Verification Gate ═══"
echo ""; echo "== Compile all =="; python3 -m compileall zmatrix tests scripts pipelines; echo "✅ compileall PASS"

for t in \
  test_chain_force_10x5 test_sector_stage test_financial_health_gate \
  test_b_matrix_contract test_d_matrix_contract test_stock_role_classifier \
  test_account_constitution test_portfolio_exposure test_z8_position_control \
  test_pre_trade_checklist test_g17_human_veto test_investment_role_workflow \
  test_brd_architecture_integration test_brd_conflict_audit; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done

echo ""; echo "== Architecture integration =="
for t in test_shared_skill_registry test_pipeline_registry test_gate_registry \
  test_workflow_dag test_architecture_enforcement test_cross_pipeline_conflict_audit \
  test_system_controller_mvp; do
  python3 "tests/${t}.py"
done

echo ""; echo "== Git check =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
 git diff --check; [ -z "$(git status --short)" ] && echo "✅ working tree clean" || { echo "❌ dirty"; git status --short; exit 1; }
else echo "(non-git workspace, skip)"; fi
echo ""; echo "═══ Investment Role Verification PASS ═══"
