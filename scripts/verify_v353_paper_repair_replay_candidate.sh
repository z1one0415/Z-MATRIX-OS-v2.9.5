#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.3 Paper-Only Repair Replay Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
PYTHONPATH=. python3 tests/test_v353_invalidation_rule_extractor.py && echo "  ✅ invalidation_rule_extractor"
PYTHONPATH=. python3 tests/test_v353_invalidation_exit_simulator.py && echo "  ✅ invalidation_exit_simulator"
PYTHONPATH=. python3 tests/test_v353_baseline_repair_comparator.py && echo "  ✅ baseline_repair_comparator"
PYTHONPATH=. python3 tests/test_v353_repair_replay_report.py && echo "  ✅ repair_replay_report"
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.3 Paper-Only Repair Replay PASS ═══"
