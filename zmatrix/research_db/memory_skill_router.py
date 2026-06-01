from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def route_skill(sid,env,ctx):
    if sid=="MEMORY.GET_MEMORY_CANDIDATE_SCHEMA": return build_skill_success(sid,{"schema":{"id":"str","summary":"str"}})
    if sid=="MEMORY.VALIDATE_MEMORY_CANDIDATE":
        c=ctx.get("memory_candidate",{}); ms=[k for k in["candidate_summary","required_validation"] if not c.get(k)]
        return build_skill_success(sid,{"valid":not ms,"missing":ms,"main_write":False})
    if sid=="MEMORY.BUILD_MONTHLY_MEMORY_CANDIDATE_DRAFT": return build_skill_draft(sid,{"status":"CANDIDATE_ONLY","main_write":False,"rdb_write":False})
    if sid=="MEMORY.GET_MEMORY_READINESS": return build_skill_success(sid,{"readiness":"CANDIDATE_ONLY_READY","main_write":False})
    return build_skill_blocked(sid,"Unknown MEMORY skill")
