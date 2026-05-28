#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.6 Closeout Regime Separability Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
for t in market_regime_builder sector_phase_builder breadth_liquidity_builder regime_feature_joiner regime_performance_profiler regime_separability_tester regime_candidate_miner regime_report_builder regime_separability_scoring_fix regime_candidate_miner_closeout regime_report_builder_closeout; do
    PYTHONPATH=. python3 tests/test_v356_${t}.py && echo "  ✅ $t"
done
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.6 Closeout Regime Separability PASS ═══"
