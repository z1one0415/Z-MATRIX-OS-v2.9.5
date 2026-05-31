from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def route_skill(sid,env,ctx):
    if sid=="AUTOCASE.GET_INTAKE_SCHEMA": return build_skill_success(sid,{"schema":{"source_system":"str","ticker":"str"}})
    if sid=="AUTOCASE.VALIDATE_INTAKE_DRAFT":
        d=ctx.get("intake_draft",{}); ms=[k for k in["source_system","draft_summary"] if not d.get(k)]
        return build_skill_success(sid,{"valid":not ms,"missing":ms,"main_write":False})
    if sid=="AUTOCASE.BUILD_CASE_CANDIDATE_DRAFT": return build_skill_draft(sid,{"status":"DRAFT_ONLY","main_write":False,"rdb_write":False})
    if sid=="AUTOCASE.GET_AUTOCASE_READINESS": return build_skill_success(sid,{"readiness":"CANDIDATE_DRAFT_READY","main_write":False})
    return build_skill_blocked(sid,"Unknown AUTOCASE skill")
