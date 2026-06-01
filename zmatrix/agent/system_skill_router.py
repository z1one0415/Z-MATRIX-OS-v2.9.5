from __future__ import annotations
import json; from pathlib import Path
from .skill_result_envelope import build_skill_success, build_skill_blocked
from .skill_domain_registry import list_domain_router_status
REG=Path("data/research_db/agent/registry/skill_registry.generated.json")
CAND=Path("data/research_db/agent/registry/skill_candidate_index.json")
def _j(p): return json.loads(p.read_text()) if p.exists() else []
def route_skill(sid,env,ctx):
    skills=_j(REG); candidates=_j(CAND)
    if sid=="SYSTEM.GET_SKILLOS_STATUS": return build_skill_success(sid,{"status":"SKILLOS_ACTIVE","registered":len(skills),"candidates":len(candidates)})
    if sid=="SYSTEM.GET_SKILL_REGISTRY_SUMMARY":
        ds={}
        for s in skills: d=s["skill_id"].split(".")[0]; ds[d]=ds.get(d,0)+1
        return build_skill_success(sid,{"count":len(skills),"domains":ds})
    if sid=="SYSTEM.GET_SKILL_CANDIDATE_SUMMARY":
        ds={}
        for c in candidates: ds[c.get("domain","?")]=ds.get(c.get("domain","?"),0)+1
        return build_skill_success(sid,{"count":len(candidates),"domains":ds})
    if sid=="SYSTEM.GET_DOMAIN_ROUTER_STATUS": return build_skill_success(sid,list_domain_router_status())
    if sid=="SYSTEM.GET_VERIFY_CHAIN_STATUS": return build_skill_success(sid,{"chains":["v01","v02","zg16","zk"]})
    return build_skill_blocked(sid,"Unknown SYSTEM skill")
