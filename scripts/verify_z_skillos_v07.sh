#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.7 Council ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v06.sh
bash scripts/verify_z_skillos_v05.sh
bash scripts/verify_z_skillos_v04.sh
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ v0.7 Registry + Council Runtime ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v07.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
for x in s:
 for k in['production_allowed','external_api_used','trade_allowed','verdict_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed']:
  assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required')
print(f'registry PASS: {len(s)} skills')
from zmatrix.agent.domain_skill_router import route_skill_by_domain
for sid in['COUNCIL.GET_COUNCIL_SCHEMA','COUNCIL.GET_EXPERT_ROLE_REGISTRY','COUNCIL.BUILD_EXPERT_REVIEW_DRAFT','COUNCIL.BUILD_DISAGREEMENT_MATRIX_DRAFT','COUNCIL.BUILD_RISK_REVIEW_DRAFT','COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY','COUNCIL.GET_COUNCIL_READINESS']:
 r=route_skill_by_domain(sid,{},{'council_output':''})
 assert r['status']in{'EXECUTED','DRAFT_CREATED'},sid
 o=r.get('output',{})
 for k in['trade_allowed','verdict_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','researchdb_main_write','memory_main_write','final_decision']:
  assert o[k] is False,f'{sid}:{k}'
bad=route_skill_by_domain('COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY',{},{'council_output':'BUY 卖出'})
assert bad['output']['valid'] is False
print('council runtime PASS')
"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
 [ ! -f "$f" ] && continue; base=$(basename "$f")
 [ "$base" = "data_source_attribution_ledger.csv" ] && continue
 [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "═══ Z-SkillOS v0.7 PASS ═══"
