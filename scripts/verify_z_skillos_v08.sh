#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.8.1 Matrix Hardened ═══"
if [[ "${Z_SKILLOS_FLAT_VERIFY:-0}" != "1" ]]; then
    python3 -m compileall -q zmatrix tests scripts
    PYTHONPATH=. python3 -m pytest -q tests/agent/
    PYTHONPATH=. python3 -m pytest -q tests/research_db/
    PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
    PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
    PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
    bash scripts/verify_z_skillos_v07.sh
    bash scripts/verify_zg16_full_stub_integration.sh
    bash scripts/verify_z_agent_kernel.sh
else
    echo "flat mode: shared compile/test/registry and inherited chain handled by caller"
fi

echo "═══ v0.8.1 Registry Safety ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v08.json').read_text())
sm={x['skill_id']:x for x in s}
for sid in wl['selected_skills']: assert sid in sm,f'missing:{sid}'
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids))
for x in s:
 for k in['production_allowed','external_api_used','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','final_scoring_allowed','backtest_allowed']:
  assert x.get(k) is not True,f'{x[\"skill_id\"]}:{k}'
 if x.get('write_layers'): assert x.get('requires_human_review') and x.get('proposal_required')
print(f'registry PASS: {len(s)} skills')
"

echo "═══ v0.8.1 Matrix Runtime ═══"
PYTHONPATH=. python3 -c "
from zmatrix.agent.domain_skill_router import route_skill_by_domain
keys=['external_api_used','production_allowed','shadowbroker_deployed','trade_allowed','verdict_allowed','broker_order_allowed','real_trade_allowed','auto_buy_allowed','auto_sell_allowed','investment_verdict_allowed','trade_signal_allowed','buy_sell_hold_allowed','portfolio_allowed','final_scoring_allowed','backtest_allowed','researchdb_main_write','memory_main_write']
ctx={'zc35_input':{},'score_input':{},'stage_input':{}}
for sid in['ZC35.GET_SCHEMA','ZC35.GET_CHECKLIST','ZC35.VALIDATE_INPUT_DRY','ZC35.BUILD_REVIEW_DRAFT','ZC35.GET_READINESS','BMATRIX.GET_SCHEMA','BMATRIX.GET_SCORECARD_TEMPLATE','BMATRIX.VALIDATE_SCORE_INPUT_DRY','BMATRIX.BUILD_REVIEW_DRAFT','BMATRIX.GET_READINESS','DMATRIX.GET_SCHEMA','DMATRIX.GET_LIFECYCLE_STAGE_TEMPLATE','DMATRIX.VALIDATE_STAGE_INPUT_DRY','DMATRIX.BUILD_REVIEW_DRAFT','DMATRIX.GET_READINESS']:
 r=route_skill_by_domain(sid,{},ctx)
 assert r['status']in{'EXECUTED','DRAFT_CREATED'},sid; o=r.get('output',{})
 for k in keys: assert o.get(k) is False,f'{sid}:{k}'
 if sid.endswith('BUILD_REVIEW_DRAFT'): assert r['status']=='DRAFT_CREATED' and r['human_review_required']
 if sid.endswith('GET_READINESS'):
  for k in['matrix_engine_enabled','final_scoring_allowed','backtest_allowed','ranking_allowed','trade_signal_allowed','portfolio_allowed']:
   assert o.get(k) is False,f'{sid}:{k}'
print('matrix runtime PASS')
"

echo "=== v08 Forbidden Scan ==="
python3 << 'INNEREOF'
from pathlib import Path
import re
import io
import tokenize
import subprocess
import os

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

def resolve_scan_base():
    explicit = os.environ.get("Z_SKILLOS_SCAN_BASE_REF")
    candidates = [explicit] if explicit else []
    candidates.extend([
        "@{upstream}",
        "origin/v4.0-batch-0-final-hardgates-scope-lock-clean",
        "origin/v4.0-batch-0-final-hardgates-scope-lock",
    ])
    for ref in candidates:
        if not ref:
            continue
        probe = subprocess.run(["git", "rev-parse", "--verify", ref], capture_output=True, text=True)
        if probe.returncode == 0:
            return ref
    raise SystemExit("FAIL: unable to resolve SkillOS forbidden scan base")

bkeys=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","final_scoring_allowed","backtest_allowed"]
ckeys=["买"+"入","卖"+"出","持"+"有","目标"+"价","仓"+"位"]
rkeys=["subprocess"+".run(","os"+".system("]
en_re=re.compile(r"\b(BUY|SELL|HOLD)\b")
parent=resolve_scan_base()
result=subprocess.run(["git","diff","--diff-filter=ACMR","--name-only",f"{parent}...HEAD"],capture_output=True,text=True,check=True)
changed=set(result.stdout.splitlines())
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

echo "═══ Z-SkillOS v0.8.1 PASS ═══"
