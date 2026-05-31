from __future__ import annotations
_ROUTER_IMPL={"SYSTEM":"","RESEARCHDB":"","DATAFORGE":"","FACTOR":"","COUNCIL":"","REPORT":"","CASEFORGE":"","AUTOCASE":"","ZG16":"zmatrix.research_db.zg16_skill_router","ZC35":"","BMATRIX":"","DMATRIX":"","PORTFOLIO":"","GOVERNANCE":"","COCKPIT":"","MEMORY":"","WORKFLOW":""}
def get_skill_domain(sid): return sid.split(".",1)[0].upper() if "." in sid else "UNKNOWN"
def is_domain_registered(sid): return get_skill_domain(sid) in _ROUTER_IMPL
def has_domain_router(sid): return bool(_ROUTER_IMPL.get(get_skill_domain(sid),""))
