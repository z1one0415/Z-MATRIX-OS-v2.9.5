from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_blocked
from zmatrix.agent.skill_domain_registry import list_domain_router_status
def route_skill(sid,env,ctx):
    if sid=="COCKPIT.BUILD_SKILLOS_OVERVIEW": return build_skill_success(sid,{"panel":"SKILLOS_OVERVIEW","next":"Review v0.2 batch"})
    if sid=="COCKPIT.BUILD_ZG16_STATUS_PANEL": return build_skill_success(sid,{"panel":"ZG16","stub":True})
    if sid=="COCKPIT.BUILD_SKILL_DOMAIN_PANEL": return build_skill_success(sid,{"domains":list_domain_router_status()})
    if sid=="COCKPIT.GET_NEXT_HUMAN_ACTIONS": return build_skill_success(sid,{"actions":["Review routers","Do not auto-enable candidates"]})
    return build_skill_blocked(sid,"Unknown COCKPIT skill")
