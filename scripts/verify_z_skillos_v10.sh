#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.10.3 Workflow Hardened ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v09.sh
bash scripts/verify_z_skillos_v08.sh
bash scripts/verify_z_skillos_v07.sh
bash scripts/verify_z_skillos_v06.sh
bash scripts/verify_z_skillos_v05.sh
bash scripts/verify_z_skillos_v04.sh
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh

echo "═══ v0.10.3 Registry Safety ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v10.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
keys=['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_runtime_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','portfolio_decision_allowed','position_sizing_allowed','order_generation_allowed','target_price_allowed','workflow_execution_allowed','multi_domain_execution_allowed','portfolio_allowed']
for x in s:
 for k in keys: assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required')
print(f'registry PASS: {len(s)} skills')
"

echo "═══ v0.10.3 Workflow Runtime ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
keys=['external_api_used','production_allowed','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_runtime_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','portfolio_decision_allowed','position_sizing_allowed','order_generation_allowed','target_price_allowed','workflow_execution_allowed','multi_domain_execution_allowed','researchdb_main_write','memory_main_write']
ctx={'workflow_input':{}}
for sid in['WORKFLOW.GET_WORKFLOW_SCHEMA','WORKFLOW.GET_STAGE_TEMPLATE','WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT','WORKFLOW.BUILD_MULTI_DOMAIN_REVIEW_DRAFT','WORKFLOW.RUN_RESEARCH_DRY_CHAIN','WORKFLOW.VALIDATE_WORKFLOW_INPUT_DRY','WORKFLOW.GET_WORKFLOW_READINESS']:
 r=route_skill_by_domain(sid,{},ctx); o=r.get('output',{})
 assert r['status']in{'EXECUTED','DRAFT_CREATED'},sid
 for k in keys: assert o.get(k) is False,f'{sid}:{k}'
 if sid in['WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT','WORKFLOW.BUILD_MULTI_DOMAIN_REVIEW_DRAFT']: assert r['status']=='DRAFT_CREATED' and r['human_review_required']
 if sid=='WORKFLOW.RUN_RESEARCH_DRY_CHAIN': assert o.get('dry_run') and o.get('plan_only')
 if sid=='WORKFLOW.GET_WORKFLOW_READINESS':
  for k in['workflow_engine_enabled','workflow_execution_allowed','multi_domain_execution_allowed','external_api_used','production_allowed','broker_runtime_allowed','broker_order_allowed','real_trade_allowed','order_generation_allowed','portfolio_decision_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','position_sizing_allowed','target_price_allowed','researchdb_main_write','memory_main_write']:
   assert o.get(k) is False,f'readiness:{k}'
print('workflow runtime PASS')
"

echo "=== v10 Forbidden Scan ==="
python3 << 'INNEREOF'
from pathlib import Path
import re
import io
import tokenize
import subprocess

def strip_comments_and_strings(text):
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
        result = []
        for tok in tokens:
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            result.append(tok.string)
        return ''.join(result)
    except tokenize.TokenError:
        clean = text
        clean = re.sub(r'""".*?"""', '', clean, flags=re.DOTALL)
        clean = re.sub(r"'''.*?'''", '', clean, flags=re.DOTALL)
        clean = re.sub(r'#.*', '', clean)
        return clean

bkeys=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_runtime_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","portfolio_decision_allowed","position_sizing_allowed","order_generation_allowed","target_price_allowed","workflow_execution_allowed","multi_domain_execution_allowed"]
ckeys=["买"+"入","卖"+"出","持"+"有","目标"+"价","仓"+"位","下"+"单","调"+"仓","执"+"行","自动"+"运行"]
rkeys=["subprocess"+".run(","os"+".system("]
en_re=re.compile(r"\b(BUY|SELL|HOLD)\b")
parent="origin/v4.0-batch-0-final-hardgates-scope-lock"
result=subprocess.run(["git","diff","--name-only",f"{parent}...HEAD"],capture_output=True,text=True)
changed=set(line for line in result.stdout.split("\n") if line)
for f_str in changed:
    f=Path(f_str)
    if not f.exists():continue
    if f.suffix==".py":
        t=f.read_text("utf-8",errors="ignore")
        clean=strip_comments_and_strings(t)
        for k in bkeys:
            for pat in[f"{k}=True",f"{k} = True",chr(34)+k+chr(34)+": true",chr(34)+k+chr(34)+": True",chr(39)+k+chr(39)+": True"]:
                assert pat not in clean,f"{pat} in {f}"
        for tok in rkeys:assert tok not in clean,f"{tok} in {f}"
        assert not en_re.search(clean),f"English trade token in {f}"
        for tok in ckeys:assert tok not in clean,f"{tok} in {f}"
    elif f.suffix==".sh":
        if "verify_z_skillos" in f_str and f_str.endswith(".sh"):continue
        t=f.read_text("utf-8",errors="ignore")
        for k in bkeys:
            for pat in[f"{k}=True",f"{k} = True",chr(34)+k+chr(34)+": true",chr(34)+k+chr(34)+": True",chr(39)+k+chr(39)+": True"]:
                assert pat not in t,f"{pat} in {f}"
        for tok in rkeys:assert tok not in t,f"{tok} in {f}"
    elif f.suffix==".json":
        t=f.read_text("utf-8",errors="ignore")
        for k in bkeys:
            for pat in[chr(34)+k+chr(34)+": true",chr(34)+k+chr(34)+": True"]:
                assert pat not in t,f"{pat} in {f}"
print("forbidden scan PASS")
INNEREOF

echo "═══ Z-SkillOS v0.10.3 PASS ═══"
