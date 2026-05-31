#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 v3 Query Bridge Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zg16/
bash scripts/verify_zg16_v2_data_governance.sh
echo "═══ Z-G16 v3 Query Bridge PASS ═══"
