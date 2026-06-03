#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.9.1 Portfolio Hardened ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v08.sh
bash scripts/verify_z_skillos_v07.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh

echo "═══ v0.9.1 Registry Safety ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v09.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm,f'missing:{sid}'
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
keys=['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','portfolio_decision_allowed','position_sizing_allowed','order_generation_allowed','target_price_allowed']
for x in s:
 for k in keys: assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required')
print(f'registry PASS: {len(s)} skills')
"

echo "═══ v0.9.1 Portfolio Runtime ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
keys=['external_api_used','production_allowed','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','portfolio_decision_allowed','position_sizing_allowed','order_generation_allowed','target_price_allowed','researchdb_main_write','memory_main_write']
ctx={'portfolio_input':{}}
for sid in['PORTFOLIO.GET_SCHEMA','PORTFOLIO.GET_RISK_BUDGET_TEMPLATE','PORTFOLIO.GET_EXPOSURE_TEMPLATE','PORTFOLIO.VALIDATE_PORTFOLIO_INPUT_DRY','PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT','PORTFOLIO.GET_PORTFOLIO_READINESS']:
 r=route_skill_by_domain(sid,{},ctx); o=r.get('output',{})
 assert r['status']in{'EXECUTED','DRAFT_CREATED'},sid
 for k in keys: assert o.get(k) is False,f'{sid}:{k}'
 if sid.endswith('BUILD_PORTFOLIO_REVIEW_DRAFT'): assert r['status']=='DRAFT_CREATED' and r['human_review_required']
 if sid.endswith('GET_PORTFOLIO_READINESS'):
  for k in['portfolio_engine_enabled','portfolio_allowed','portfolio_decision_allowed','order_generation_allowed','position_sizing_allowed','target_price_allowed','trade_signal_allowed','buy_sell_hold_allowed','broker_order_allowed','real_trade_allowed']:
   assert o.get(k) is False,f'{sid}:{k}'
print('portfolio runtime PASS')
"

echo "═══ v0.9.1 Forbidden Scan ═══"
PYTHONPATH=. python3 -c "
from pathlib import Path
bkeys=['external_api_used','shadowbroker_deployed','production_allowed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','portfolio_decision_allowed','position_sizing_allowed','order_generation_allowed','target_price_allowed']
tkeys=['B'+'UY','S'+'ELL','H'+'OLD','买'+'入','卖'+'出','持'+'有','目标'+'价','仓'+'位','下'+'单','调'+'仓']
rkeys=['subprocess'+'.run(','os'+'.system(']
skip={'scripts/verify_z_skillos_v09.sh'}
for r in['zmatrix','scripts','tests/agent','data/research_db/agent/registry']:
 p=Path(r)
 if not p.exists(): continue
 for f in p.rglob('*'):
  if f.suffix not in{'.py','.sh','.json'}: continue
  if str(f) in skip: continue
  t=f.read_text('utf-8',errors='ignore')
  for k in bkeys:
   for pat in[f'{k}=True',f'{k} = True',chr(34)+k+chr(34)+': true',chr(34)+k+chr(34)+': True',chr(39)+k+chr(39)+': True']:
    assert pat not in t,f'{pat} in {f}'
  for tok in rkeys: assert tok not in t,f'{tok} in {f}'
  for tok in tkeys: assert tok not in t,f'{tok} in {f}'
print('forbidden scan PASS')
"

for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
 [ ! -f "$f" ] && continue; base=$(basename "$f")
 [ "$base" = "data_source_attribution_ledger.csv" ] && continue
 [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "═══ Z-SkillOS v0.9.1 PASS ═══"
