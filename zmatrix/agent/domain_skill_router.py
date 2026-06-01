from __future__ import annotations
import importlib
from .skill_domain_registry import get_skill_domain, get_domain_router_path
from .skill_result_envelope import build_skill_blocked
def route_skill_by_domain(sid,env,ctx):
    rp=get_domain_router_path(sid)
    if not rp: return build_skill_blocked(sid,f"No router for {get_skill_domain(sid)}")
    m=importlib.import_module(rp)
    fn=getattr(m,"route_skill",None)
    if not fn: return build_skill_blocked(sid,f"Missing route_skill in {rp}")
    return fn(sid,env,ctx)
