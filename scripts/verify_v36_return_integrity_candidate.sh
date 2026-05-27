#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v3.5.1 Return Integrity Verification ═══"

PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1

PYTHONPATH=. python3 tests/test_v36_robust_metrics.py
echo "  ✅ robust_metrics"

PYTHONPATH=. python3 tests/test_v36_strategy_verdict.py
echo "  ✅ strategy_verdict"

PYTHONPATH=. python3 tests/test_v36_return_sanity_guard.py
echo "  ✅ return_sanity_guard"

PYTHONPATH=. python3 tests/test_v36_return_integrity_report.py
echo "  ✅ return_integrity_report"

git diff --check

if git ls-files runtime_reports | grep .; then
    echo "❌ runtime_reports must not be tracked"
    exit 1
fi
echo "  ✅ runtime_reports not tracked"

echo "═══ v3.5.1 Return Integrity PASS ═══"
