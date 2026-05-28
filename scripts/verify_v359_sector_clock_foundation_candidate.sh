#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.9 Sector Clock Foundation Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
for t in sector_mapping_discovery sector_index_discovery synthetic_sector_basket sector_phase_builder stock_sector_joiner matrix_clock_metadata data_decay_penalty foundation_report_builder; do
    PYTHONPATH=. python3 tests/test_v359_${t}.py && echo "  ✅ $t"
done
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.9 Sector Clock Foundation PASS ═══"
