#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.2 Strategy Repair Lab Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
PYTHONPATH=. python3 tests/test_v352_return_unit_guard.py && echo "  ✅ return_unit_guard"
PYTHONPATH=. python3 tests/test_v352_pathology_classifier.py && echo "  ✅ pathology_classifier"
PYTHONPATH=. python3 tests/test_v352_segment_attributor.py && echo "  ✅ segment_attributor"
PYTHONPATH=. python3 tests/test_v352_repair_simulator.py && echo "  ✅ repair_simulator"
PYTHONPATH=. python3 tests/test_v352_repair_verdict.py && echo "  ✅ repair_verdict"
PYTHONPATH=. python3 tests/test_v352_repair_lab_report.py && echo "  ✅ repair_lab_report"
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.2 Strategy Repair Lab PASS ═══"
