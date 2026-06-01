from __future__ import annotations
import json; from pathlib import Path
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
VS=["scripts/verify_z_skillos_v05.sh","scripts/verify_z_skillos_v04.sh","scripts/verify_z_skillos_v03.sh","scripts/verify_z_skillos_v02.sh","scripts/verify_z_skillos_v01.sh","scripts/verify_zg16_full_stub_integration.sh","scripts/verify_z_agent_kernel.sh"]
REG=Path("data/research_db/agent/registry/skill_registry.generated.json")
FORBIDDEN_BOOL_KEYS=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed"]
FORBIDDEN_RAW=["subprocess"+".run(","os"+".system("]
def _lr():
    if not REG.exists(): return []
    return json.loads(REG.read_text())
def _ls():
    files=[]; ae=True
    for pat in ["data/research_db/agent/ledgers/*.jsonl","data/research_db/governance/*.jsonl"]:
        for p in Path(".").glob(pat):
            if p.name=="data_source_attribution_ledger.csv": continue
            sz=p.stat().st_size; files.append({"path":str(p),"size":sz,"empty":sz==0})
            if sz: ae=False
    return {"all_empty":ae,"files":files}
def _rs():
    s=_lr(); ids=[x.get("skill_id") for x in s]; dup=len(ids)!=len(set(ids)); wv=[]; sv=[]
    for x in s:
        sid=x.get("skill_id","")
        if x.get("write_layers"):
            if x.get("requires_human_review") is not True or x.get("proposal_required") is not True: wv.append(sid)
        for k in ["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed"]:
            if x.get(k) is True: sv.append(f"{sid}:{k}")
    return {"count":len(s),"duplicate":dup,"write_violations":wv,"safety_violations":sv,"ok":not dup and not wv and not sv}
def _fs():
    roots=["zmatrix","scripts","tests/agent","data/research_db/agent/registry"]; hits=[]
    for r in roots:
        rp=Path(r)
        if not rp.exists(): continue
        for p in rp.rglob("*"):
            if p.suffix not in {".py",".sh",".json"}: continue
            text=p.read_text("utf-8",errors="ignore")
            for key in FORBIDDEN_BOOL_KEYS:
                for pat in [f"{key}=True",f"{key} = True",chr(34)+key+chr(34)+": true",chr(34)+key+chr(34)+": True"]:
                    if pat in text: hits.append({"path":str(p),"token":pat}); break
                else: continue
                break
            for tok in FORBIDDEN_RAW:
                if tok in text: hits.append({"path":str(p),"token":tok}); break
    return {"dry_run":True,"scanned_roots":roots,"hit_count":len(hits),"hits":hits[:50],"ok":len(hits)==0,"subprocess_execution":False}
def route_skill(sid,env,ctx):
    if sid=="GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": return build_skill_success(sid,{"scripts":[{"path":p,"exists":Path(p).exists()} for p in VS],"subprocess_execution":False})
    if sid=="GOVERNANCE.GET_LEDGER_STATUS": return build_skill_success(sid,_ls())
    if sid=="GOVERNANCE.GET_FORBIDDEN_SCAN_STATUS": return build_skill_success(sid,_fs())
    if sid=="GOVERNANCE.GET_SKILLOS_RELEASE_READINESS":
        l=_ls(); r=_rs(); f=_fs(); ready=l["all_empty"] and r["ok"] and f["ok"]
        return build_skill_success(sid,{"ready":ready,"ledger_ok":l["all_empty"],"registry_ok":r["ok"],"forbidden_ok":f["ok"],"subprocess_execution":False})
    if sid=="GOVERNANCE.VALIDATE_SKILL_REGISTRY_DRY": return build_skill_success(sid,{"dry":True,"registry":_rs(),"researchdb_main_write":False,"subprocess_execution":False})
    if sid=="GOVERNANCE.RUN_SKILLOS_VERIFY_DRY": return build_skill_success(sid,{"dry":True,"subprocess_execution":False,"plan":VS,"note":"Plan only. No shell execution."})
    if sid=="GOVERNANCE.BUILD_VERIFY_REPORT_DRAFT": return build_skill_draft(sid,{"report":"DRAFT_ONLY","ledger":_ls(),"registry":_rs(),"researchdb_main_write":False,"subprocess_execution":False})
    if sid=="GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT": return build_skill_draft(sid,{"audit":"DRAFT_ONLY","release":"HUMAN_REVIEW","researchdb_main_write":False,"subprocess_execution":False})
    if sid=="GOVERNANCE.GET_GOVERNANCE_READINESS": return build_skill_success(sid,{"ready":"GOVERNANCE_ROUTER_READY","subprocess_execution":False,"external_api_used":False})
    return build_skill_blocked(sid,"Unknown GOVERNANCE skill")
