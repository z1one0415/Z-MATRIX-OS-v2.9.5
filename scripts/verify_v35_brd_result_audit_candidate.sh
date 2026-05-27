#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5 BRD Result Audit Verification ═══"
echo ""; echo "== Compile =="; PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines; echo "✅ compileall PASS"
for t in test_brd_result_audit_distribution test_b_matrix_explainer test_active_outcome_validator test_brd_result_audit_report; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Backward =="; bash scripts/verify_v35_brd_5y_strategy_validation_candidate.sh
echo ""; echo "== Audit Smoke =="; PYTHONPATH=. python3 scripts/run_v35_brd_result_audit.py
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"; echo ""; echo "═══ v3.5 BRD Result Audit PASS ═══"
