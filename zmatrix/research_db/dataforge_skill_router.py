from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_blocked
def route_skill(sid,env,ctx):
    if sid=="DATAFORGE.GET_SNAPSHOT_SCHEMA": return build_skill_success(sid,{"schema":{"snapshot_id":"str","as_of_date":"date"},"external_api":False})
    if sid=="DATAFORGE.VALIDATE_SNAPSHOT_DRY":
        sn=ctx.get("snapshot",{}); ms=[k for k in["snapshot_id","as_of_date"] if not sn.get(k)]
        return build_skill_success(sid,{"valid":not ms,"missing":ms,"dry_run":True,"main_write":False})
    if sid=="DATAFORGE.GET_DATA_QUALITY_SUMMARY": return build_skill_success(sid,{"quality":"READ_ONLY","external_api":False})
    if sid=="DATAFORGE.GET_ATTRIBUTION_SUMMARY": return build_skill_success(sid,{"attribution":"READ_ONLY","license_review":True,"external_api":False})
    if sid=="DATAFORGE.GET_REFRESH_TIER_STATUS": return build_skill_success(sid,{"tiers":{"FAST":"stub","SLOW":"stub","HEAVY":"stub"},"external_api":False})
    if sid=="DATAFORGE.GET_DATAFORGE_READINESS": return build_skill_success(sid,{"readiness":"READ_ONLY_READY","external_api":False,"production":False})
    return build_skill_blocked(sid,"Unknown DATAFORGE skill")
