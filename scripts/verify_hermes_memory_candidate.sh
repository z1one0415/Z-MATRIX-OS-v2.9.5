#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.12-dev Hermes Memory Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_core_memory test_working_context test_learned_heuristics \
  test_prompt_patch_preview test_memory_candidate_preview test_calibration_event_preview \
  test_hermes_memory_kernel test_hermes_event_adapters test_hermes_memory_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== EventStore verify =="
bash scripts/verify_event_store_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ Hermes Memory Verification PASS ═══"
