#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.14-dev Prompt Middleware Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_prompt_patch_request test_prompt_middleware_renderer test_prompt_patch_audit \
  test_prompt_middleware_policy test_prompt_middleware_event_adapters test_prompt_middleware_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Approval verify =="
bash scripts/verify_approval_loop_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ Prompt Middleware Verification PASS ═══"
