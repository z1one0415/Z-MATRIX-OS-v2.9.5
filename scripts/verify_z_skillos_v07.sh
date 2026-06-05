#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.7.4 Council Final ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ v0.7.4 Registry + Council Runtime ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v07.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
for x in s:
 for k in['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed']:
  assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required')
print(f'registry PASS: {len(s)} skills')
from zmatrix.agent.domain_skill_router import route_skill_by_domain
keys=['external_api_used','production_allowed','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','researchdb_main_write','memory_main_write','final_decision']
for sid in['COUNCIL.GET_COUNCIL_SCHEMA','COUNCIL.GET_EXPERT_ROLE_REGISTRY','COUNCIL.BUILD_EXPERT_REVIEW_DRAFT','COUNCIL.BUILD_DISAGREEMENT_MATRIX_DRAFT','COUNCIL.BUILD_RISK_REVIEW_DRAFT','COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY','COUNCIL.GET_COUNCIL_READINESS']:
 r=route_skill_by_domain(sid,{},{'council_output':''})
 assert r['status']in{'EXECUTED','DRAFT_CREATED'},sid; o=r.get('output',{})
 for k in keys: assert o[k] is False,f'{sid}:{k}'
ft='B'+'UY'+' '+'卖'+'出'; bad=route_skill_by_domain('COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY',{},{'council_output':ft})
assert bad['output']['valid'] is False
print('council runtime PASS')
"
echo "=== v07 Forbidden Scan ==="
python3 << 'INNEREOF'
from pathlib import Path
import re
bkeys=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed"]
en_re=re.compile(r"\b(BUY|SELL|HOLD)\b")
ckeys=["买"+"入","卖"+"出","持"+"有","目标"+"价","止"+"盈","止"+"损","仓"+"位"]
rkeys=["subprocess"+".run(","os"+".system("]
for r in["zmatrix","scripts","tests/agent","data/research_db/agent/registry"]:
    p=Path(r)
    if not p.exists():continue
    for f in p.rglob("*"):
        if f.suffix not in{".py",".sh",".json"}:continue
        skip={"scripts/verify_z_skillos_v07.sh","zmatrix/investment/account_constitution.py","zmatrix/hermes_kernel/prompt_patch_preview.py","zmatrix/hermes_kernel/prompt_patch_audit.py","zmatrix/hermes_kernel/prompt_patch_request.py","zmatrix/research_council/reviewers.py","zmatrix/research_council/council.py"}
        if str(f) in skip:continue
        t=f.read_text("utf-8",errors="ignore")
        for k in bkeys:
            for pat in[f"{k}=True",f"{k} = True",chr(34)+k+chr(34)+": true",chr(34)+k+chr(34)+": True",chr(39)+k+chr(39)+": True"]:
                assert pat not in t,f"{pat} in {f}"
        for tok in rkeys:assert tok not in t,f"{tok} in {f}"
        assert not en_re.search(t),f"English trade token in {f}"
        for tok in ckeys:assert tok not in t,f"{tok} in {f}"
print("forbidden scan PASS")
INNEREOF
echo "═══ Z-SkillOS v0.7.4 PASS ═══"
