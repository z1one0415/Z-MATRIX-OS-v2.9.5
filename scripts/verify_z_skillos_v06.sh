#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.6.2 Factor Final ═══"
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

echo "═══ v0.6.2 Registry Safety ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v06.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm,f'missing:{sid}'
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids)),'dup'
for x in s:
 sid=x['skill_id']
 for k in ['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed']:
  assert x.get(k) is not True,f'{sid}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required'),sid
for sid in wl['selected_skills']:
 x=sm[sid]
 for k in ['factor_calculation_allowed','backtest_allowed','ranking_allowed','trading_signal_allowed']:
  assert x.get(k) is not True,f'{sid}:{k}'
print(f'registry PASS: {len(s)} skills')
"

echo "═══ v0.6.2 Factor All-Skills Runtime ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
for sid in ['FACTOR.GET_FACTOR_REGISTRY','FACTOR.GET_FACTOR_SCHEMA','FACTOR.GET_FACTOR_METADATA_SUMMARY','FACTOR.VALIDATE_FACTOR_INPUT_DRY','FACTOR.GET_FACTOR_READINESS','FACTOR.BUILD_FACTOR_REVIEW_DRAFT']:
 r=route_skill_by_domain(sid,{},{'factor_input':{}})
 assert r['status'] in {'EXECUTED','DRAFT_CREATED'},f'{sid}:{r[\"status\"]}'
 o=r.get('output',{})
 assert o.get('factor_calculation_allowed') is False,f'{sid}:calc'
 assert o.get('backtest_allowed') is False,f'{sid}:bt'
 assert o.get('ranking_allowed') is False,f'{sid}:rank'
 assert o.get('trading_signal_allowed') is False,f'{sid}:signal'
 assert o.get('trade_allowed') is False,f'{sid}:trade'
 assert o.get('verdict_allowed') is False,f'{sid}:verdict'
 assert o.get('researchdb_main_write') is False,f'{sid}:rdb'
 assert o.get('memory_main_write') is False,f'{sid}:mem'
r=route_skill_by_domain('FACTOR.GET_FACTOR_READINESS',{},{})
o=r['output']; assert o['factor_engine_enabled'] is False and o['ranking_allowed'] is False
d=route_skill_by_domain('FACTOR.BUILD_FACTOR_REVIEW_DRAFT',{},{})
assert d['status']=='DRAFT_CREATED' and d['human_review_required']
print('factor all-skills PASS')
"

echo "═══ v0.6.2 Forbidden Scan (code + JSON) ═══"
PYTHONPATH=. python3 -c "
from pathlib import Path
bool_keys=['external_api_used','shadowbroker_deployed','production_allowed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','factor_calculation_allowed','backtest_allowed','ranking_allowed','trading_signal_allowed']
raw='subprocess'+'.run('+';os'+'.system('
roots=['zmatrix','scripts','tests/agent','data/research_db/agent/registry']
skip={'scripts/verify_z_skillos_v06.sh'}
for r in roots:
 p=Path(r)
 if not p.exists(): continue
 for f in p.rglob('*'):
  if f.suffix not in {'.py','.sh','.json'}: continue
  if str(f) in skip: continue
  t=f.read_text('utf-8',errors='ignore')
  for k in bool_keys:
   for pat in [f'{k}=True',f'{k} = True',f'\"{k}\": true',f\"'{k}': True\",f'\"{k}\": True']:
    assert pat not in t,f'{pat} in {f}'
  for tok in ['subprocess'+'.run(','os'+'.system(']:
   assert tok not in t,f'{tok} in {f}'
print('forbidden scan PASS')
"

for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "═══ Z-SkillOS v0.6.2 PASS ═══"
