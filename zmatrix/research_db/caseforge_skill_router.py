from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def route_skill(sid,env,ctx):
    if sid=="CASEFORGE.GET_CASE_DRAFT_SCHEMA": return build_skill_success(sid,{"schema":{"case_id":"str","ticker":"str"}})
    if sid=="CASEFORGE.VALIDATE_CASE_DRAFT":
        d=ctx.get("draft",{}); ms=[k for k in ["ticker","hypothesis"] if not d.get(k)]
        return build_skill_success(sid,{"valid":not ms,"missing":ms})
    if sid=="CASEFORGE.BUILD_INTAKE_DRAFT": return build_skill_draft(sid,{"intake":"DRAFT_ONLY","main_write":False})
    if sid=="CASEFORGE.BUILD_CASE_REVIEW_SUMMARY_DRAFT": return build_skill_draft(sid,{"summary":"DRAFT_ONLY","main_write":False})
    return build_skill_blocked(sid,"Unknown CASEFORGE skill")
