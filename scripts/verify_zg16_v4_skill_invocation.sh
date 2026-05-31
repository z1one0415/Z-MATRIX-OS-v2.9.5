#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 v4 Skill Invocation Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zg16/
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_zg16_v3_query_bridge.sh
echo "═══ Z-G16 v4 Skill Invocation PASS ═══"
