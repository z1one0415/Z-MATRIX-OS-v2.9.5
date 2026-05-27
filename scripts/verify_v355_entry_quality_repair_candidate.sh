#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.5 Entry Quality Repair Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1
PYTHONPATH=. python3 tests/test_v355_entry_quality_scorer.py && echo "  ✅ entry_quality_scorer"
PYTHONPATH=. python3 tests/test_v355_archetype_classifier.py && echo "  ✅ archetype_classifier"
PYTHONPATH=. python3 tests/test_v355_candidate_rule_library.py && echo "  ✅ candidate_rule_library"
PYTHONPATH=. python3 tests/test_v355_entry_rule_replay.py && echo "  ✅ entry_rule_replay"
PYTHONPATH=. python3 tests/test_v355_entry_quality_repair_report.py && echo "  ✅ repair_report"
git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"
echo "═══ v3.5.5 Entry Quality Repair PASS ═══"
