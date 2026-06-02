#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS Full System vFS.1 Verify ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
for vs in verify_z_skillos_v10 verify_z_skillos_v09 verify_z_skillos_v08 verify_z_skillos_v07 verify_z_skillos_v06 verify_z_skillos_v05 verify_z_skillos_v04 verify_z_skillos_v03 verify_z_skillos_v02 verify_z_skillos_v01 verify_zg16_full_stub_integration verify_z_agent_kernel; do
    echo "--- $vs ---"; bash "scripts/${vs}.sh"
done
echo "═══ Full Registry + Domain Audit ═══"
PYTHONPATH=. python3 << 'PYEOF'
import json; from pathlib import Path
from zmatrix.agent.skill_domain_registry import R as routers
skills=json.loads(Path("data/research_db/agent/registry/skill_registry.generated.json").read_text())
expected={"SYSTEM","ZG16","CASEFORGE","REPORT","COCKPIT","RESEARCHDB","DATAFORGE","AUTOCASE","MEMORY","GOVERNANCE","FACTOR","COUNCIL","ZC35","BMATRIX","DMATRIX","PORTFOLIO","WORKFLOW"}
concrete={d for d,p in routers.items() if p}
framework={d for d,p in routers.items() if not p}
assert concrete==expected,f"domain mismatch: {sorted(concrete^expected)}"
assert framework==set(),f"framework remains: {framework}"
assert len(skills)>=104,f"skills: {len(skills)}"
ids=[s["skill_id"] for s in skills]; assert len(ids)==len(set(ids)),"duplicate"
ro={"R0_READ":0,"R1_ANNOTATE":1,"R2_DRAFT":2,"R3":3,"R4":4,"R5":5,"R9":9}
skeys=["production_allowed","external_api_used","shadowbroker_deployed","trade_allowed","verdict_allowed","broker_runtime_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","portfolio_decision_allowed","position_sizing_allowed","order_generation_allowed","target_price_allowed","workflow_execution_allowed","multi_domain_execution_allowed","final_scoring_allowed","backtest_allowed"]
for s in skills:
 sid=s["skill_id"]; d=s.get("domain"); assert d in expected,f"{sid}:unknown domain {d}"
 assert routers.get(d),f"{sid}:empty router for {d}"
 rvl=s.get("risk_level","R0_READ"); assert ro.get(rvl,99)<=ro["R2_DRAFT"],f"{sid}:risk {rvl}"
 for k in skeys: assert s.get(k) is not True,f"{sid}:{k}=true"
 if s.get("write_layers"): assert s.get("requires_human_review"),f"{sid}:write no review"; assert s.get("proposal_required"),f"{sid}:write no proposal"
print(f"registry PASS: skills={len(skills)} concrete={len(concrete)} framework={len(framework)}")
PYEOF
echo "═══ Full Ledger + Forbidden ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
 [ ! -f "$f" ] && continue; base=$(basename "$f")
 [ "$base" = "data_source_attribution_ledger.csv" ] && continue
 [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
PYTHONPATH=. python3 << 'PYEOF'
from pathlib import Path
bkeys=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_runtime_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","portfolio_decision_allowed","position_sizing_allowed","order_generation_allowed","target_price_allowed","workflow_execution_allowed","multi_domain_execution_allowed","final_scoring_allowed","backtest_allowed"]
tkeys=["B"+"UY","S"+"ELL","H"+"OLD","买"+"入","卖"+"出","持"+"有","目标"+"价","仓"+"位","下"+"单","调"+"仓","执"+"行","自动"+"运行"]
rkeys=["subprocess"+".run(","os"+".system("]
skip={"scripts/verify_z_skillos_full_system.sh"}
for r in["zmatrix","scripts","tests/agent","data/research_db/agent/registry"]:
 p=Path(r)
 if not p.exists():continue
 for f in p.rglob("*"):
  if f.suffix not in{".py",".sh",".json"}:continue
  if str(f) in skip:continue
  t=f.read_text("utf-8",errors="ignore")
  for k in bkeys:
   for pat in[f"{k}=True",f"{k} = True",chr(34)+k+chr(34)+": true",chr(34)+k+chr(34)+": True",chr(39)+k+chr(39)+": True"]:
    assert pat not in t,f"{pat} in {f}"
  for tok in rkeys:assert tok not in t,f"{tok} in {f}"
  for tok in tkeys:assert tok not in t,f"{tok} in {f}"
print("forbidden PASS")
PYEOF

echo "═══ Full Documentation Section Gate ═══"
python3 << '"'"'PYEOF'"'"'
from pathlib import Path
requirements = {
    "docs/skillos/Z_SKILLOS_FULL_SYSTEM_CLOSEOUT.md": 18,
    "docs/skillos/Z_SKILLOS_FULL_SYSTEM_INTEGRATION_AUDIT.md": 18,
    "docs/skillos/Z_SKILLOS_MERGE_READINESS_FINAL.md": 7,
}
for path, minimum in requirements.items():
    text = Path(path).read_text("utf-8")
    count = sum(1 for line in text.splitlines() if line.startswith("## "))
    assert count >= minimum, f"{path}: section count {count} < {minimum}"
print("documentation section gate PASS")
PYEOF

echo "═══ Z-SkillOS Full System vFS.4 PASS ═══"
