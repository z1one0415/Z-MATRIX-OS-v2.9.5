#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.6 Factor ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v05.sh
bash scripts/verify_z_skillos_v04.sh
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ v0.6 Router Runtime ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
r=route_skill_by_domain('FACTOR.GET_FACTOR_REGISTRY',{},{})
assert r['output']['factor_calculation_allowed'] is False
assert r['output']['trading_signal_allowed'] is False
v=route_skill_by_domain('FACTOR.VALIDATE_FACTOR_INPUT_DRY',{},{'factor_input':{}})
assert v['output']['calculation_executed'] is False
assert v['output']['backtest_executed'] is False
d=route_skill_by_domain('FACTOR.BUILD_FACTOR_REVIEW_DRAFT',{},{})
assert d['status']=='DRAFT_CREATED' and d['output']['trading_signal_allowed'] is False
print('factor router PASS')
"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "═══ Z-SkillOS v0.6 PASS ═══"
