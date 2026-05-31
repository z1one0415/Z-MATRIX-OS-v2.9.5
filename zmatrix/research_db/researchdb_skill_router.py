from __future__ import annotations
import json; from pathlib import Path
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_blocked
REG=Path("data/research_db/agent/registry/skill_registry.generated.json"); CAND=Path("data/research_db/agent/registry/skill_candidate_index.json")
def _j(p,d): return json.loads(p.read_text()) if p.exists() else d
def route_skill(sid,env,ctx):
    s=_j(REG,[]); c=_j(CAND,[])
    if sid=="RESEARCHDB.GET_LAYER_STATUS": return build_skill_success(sid,{"layers":["account","market_data","event_physical","caseforge"],"main_write":False})
    if sid=="RESEARCHDB.GET_DATASET_REGISTRY": return build_skill_success(sid,{"datasets":["skill_registry.generated.json","candidate_index"],"external_api":False})
    if sid=="RESEARCHDB.GET_CASE_INDEX_SUMMARY": return build_skill_success(sid,{"case_index":"STUB","main_write":False})
    if sid=="RESEARCHDB.GET_SOURCE_HEALTH_SUMMARY": return build_skill_success(sid,{"source_health":"READ_ONLY","gov_write":False})
    if sid=="RESEARCHDB.GET_SKILL_REGISTRY_VIEW":
        ds={}
        for x in s: d=x.get("domain","?"); ds[d]=ds.get(d,0)+1
        return build_skill_success(sid,{"count":len(s),"candidates":len(c),"domains":ds})
    if sid=="RESEARCHDB.GET_RESEARCHDB_READINESS": return build_skill_success(sid,{"readiness":"READ_ONLY_READY","main_write":False,"memory_write":False})
    return build_skill_blocked(sid,"Unknown RESEARCHDB skill")
