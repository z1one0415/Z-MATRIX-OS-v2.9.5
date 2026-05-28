#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.8 Regime Observation + Pool Resilience Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
for t in temporal_instability_attributor pool_resilience_deep_dive sector_data_auditor matrix_clock_metadata_auditor zg18_conflict_observer o3_paper_fallback_study observation_report_builder; do
    PYTHONPATH=. python3 tests/test_v358_${t}.py && echo "  ✅ $t"
done
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.8 Regime Observation + Pool Resilience PASS ═══"
