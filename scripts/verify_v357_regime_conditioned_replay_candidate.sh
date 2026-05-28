#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.7 Closeout Anti-Overfit Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
for t in regime_policy_library replay_metrics regime_policy_replay baseline_comparator candidate_verdict replay_report_builder temporal_split_validator sector_split_validator stress_window_validator opportunity_loss_validator stability_verdict anti_overfit_report_builder candidate_verdict_closeout; do
    PYTHONPATH=. python3 tests/test_v357_${t}.py && echo "  ✅ $t"
done
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.7 Closeout Anti-Overfit PASS ═══"
