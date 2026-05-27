#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.4 Invalidation Anatomy Lab Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
PYTHONPATH=. python3 tests/test_v354_invalidation_event_builder.py && echo "  ✅ invalidation_event_builder"
PYTHONPATH=. python3 tests/test_v354_post_invalidation_path_labeler.py && echo "  ✅ post_invalidation_path_labeler"
PYTHONPATH=. python3 tests/test_v354_pre_trigger_features.py && echo "  ✅ pre_trigger_features"
PYTHONPATH=. python3 tests/test_v354_trigger_day_features.py && echo "  ✅ trigger_day_features"
PYTHONPATH=. python3 tests/test_v354_recovery_profile.py && echo "  ✅ recovery_profile"
PYTHONPATH=. python3 tests/test_v354_separability_tester.py && echo "  ✅ separability_tester"
PYTHONPATH=. python3 tests/test_v354_rule_candidate_miner.py && echo "  ✅ rule_candidate_miner"
PYTHONPATH=. python3 tests/test_v354_anatomy_report.py && echo "  ✅ anatomy_report"
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.4 Invalidation Anatomy Lab PASS ═══"
