#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.2 BRD Strategy Validation Verification ═══"
echo ""; echo "== Compile =="
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_brd_pit_feature_builder test_brd_classifier_adapter test_brd_paper_action_builder \
  test_brd_outcome_linker test_brd_single_day_strategy_replay test_brd_strategy_metrics \
  test_brd_strategy_validation_report test_brd_replay_policy; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.2 BRD Strategy Validation PASS ═══"
