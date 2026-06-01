#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.5.1 ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v04.sh
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ v0.5.1 Registry Safety ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v05.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm,f'missing:{sid}'
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
for x in s:
 for k in ['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed']:
  assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required'),x['skill_id']
print(f'registry PASS: {len(s)} skills')
"
echo "═══ Governance Router Runtime Check ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
r=route_skill_by_domain('GOVERNANCE.RUN_SKILLOS_VERIFY_DRY',{},{})
assert r['output']['subprocess_execution'] is False,'subprocess check fail'
s=route_skill_by_domain('GOVERNANCE.GET_FORBIDDEN_SCAN_STATUS',{},{})
assert 'hit_count' in s['output'],'missing hit_count'
assert 'ok' in s['output'],'missing ok'
assert s['output']['subprocess_execution'] is False
d=route_skill_by_domain('GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT',{},{})
assert d['status']=='DRAFT_CREATED','audit not draft'
assert d['human_review_required'] is True
assert d['researchdb_main_write'] is False
print('governance router runtime PASS')
"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "═══ Z-SkillOS v0.5.1 PASS ═══"
