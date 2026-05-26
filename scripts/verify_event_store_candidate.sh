#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.11-dev EventStore Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_event_ids test_event_schema test_event_store_local test_event_lineage \
  test_event_query_export test_event_adapters test_event_store_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Workspace alignment verify =="
bash scripts/verify_workspace_alignment_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "== System controller MVP =="
python3 tests/test_system_controller_mvp.py
echo ""; echo "═══ EventStore Verification PASS ═══"
