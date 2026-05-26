#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5 BRD 5Y Strategy Validation Verification ═══"
echo ""; echo "== Compile =="; PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines; echo "✅ compileall PASS"
for t in test_v35_metrics_aggregator test_v35_role_phase_breakdown test_v35_failure_analyzer test_v35_validation_policy test_v35_final_report; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Backward =="; bash scripts/verify_v34_pit_brd_matrix_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"; echo ""; echo "═══ v3.5 5Y Strategy Validation PASS ═══"
