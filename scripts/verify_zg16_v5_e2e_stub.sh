#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 v5 E2E Stub Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zg16/
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_zg16_v4_skill_invocation.sh
bash scripts/verify_zg16_v3_query_bridge.sh
bash scripts/verify_zg16_v2_data_governance.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ Z-G16 v5 E2E Stub PASS ═══"
