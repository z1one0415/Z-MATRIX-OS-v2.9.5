#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.4 PIT B/R/D Matrix Precompute Verification ═══"
echo ""; echo "== Compile =="; PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_brd_matrix_pit_builders test_brd_input_bundle_builder test_brd_matrix_pit_policy \
  test_real_brd_connector test_brd_classifier_connection test_brd_connection_validator \
  test_brd_strategy_connected_report; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Real Data Smoke =="; PYTHONPATH=. python3 scripts/run_v34_pit_brd_matrix_smoke.py
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.4 PIT Matrix Precompute PASS ═══"
