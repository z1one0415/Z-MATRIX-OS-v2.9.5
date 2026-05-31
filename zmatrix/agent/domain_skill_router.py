from __future__ import annotations
from .skill_domain_registry import get_skill_domain; from .skill_result_envelope import build_skill_blocked
def route_skill_by_domain(sid,env,ctx):
 if get_skill_domain(sid)=="ZG16":
  from zmatrix.research_db.zg16_skill_router import route_zg16_skill
  return route_zg16_skill(sid,env,ctx)
 return build_skill_blocked(sid,f"Domain router not implemented for {get_skill_domain(sid)}")
