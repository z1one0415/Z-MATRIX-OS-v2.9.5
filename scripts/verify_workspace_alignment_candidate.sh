#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.10-dev Workspace Alignment Verification Gate ═══"
echo ""; echo "== Compile all =="; python3 -m compileall zmatrix tests scripts pipelines; echo "✅ compileall PASS"
for t in test_workspace_layout test_pipeline_census test_hermes_adapter_registry \
  test_script_index test_research_asset_index; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Personal quant data verify =="; bash scripts/verify_personal_quant_data_candidate.sh
echo ""; echo "== Git check =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
 git diff --check; [ -z "$(git status --short)" ] && echo "✅ clean" || { echo "❌ dirty"; exit 1; }
else echo "(non-git, skip)"; fi
echo ""; echo "═══ Workspace Alignment Verification PASS ═══"
