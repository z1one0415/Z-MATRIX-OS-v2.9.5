from __future__ import annotations
R={"SYSTEM":"zmatrix.agent.system_skill_router","RESEARCHDB":"zmatrix.research_db.researchdb_skill_router","DATAFORGE":"zmatrix.research_db.dataforge_skill_router","FACTOR":"zmatrix.research_db.factor_skill_router","COUNCIL":"zmatrix.research_db.council_skill_router","REPORT":"zmatrix.research_db.report_skill_router","CASEFORGE":"zmatrix.research_db.caseforge_skill_router","AUTOCASE":"zmatrix.research_db.autocase_skill_router","ZG16":"zmatrix.research_db.zg16_skill_router","ZC35":"zmatrix.research_db.zc35_skill_router","BMATRIX":"zmatrix.research_db.bmatrix_skill_router","DMATRIX":"zmatrix.research_db.dmatrix_skill_router","PORTFOLIO":"zmatrix.research_db.portfolio_skill_router","GOVERNANCE":"zmatrix.research_db.governance_skill_router","COCKPIT":"zmatrix.research_db.cockpit_skill_router","MEMORY":"zmatrix.research_db.memory_skill_router","WORKFLOW":""}
def get_skill_domain(sid): return sid.split(".",1)[0].upper() if "." in sid else "UNKNOWN"
def is_domain_registered(sid): return get_skill_domain(sid) in R
def get_domain_router_path(sid): return R.get(get_skill_domain(sid),"")
def has_domain_router(sid): return bool(get_domain_router_path(sid))
def list_domain_router_status(): return {d:{"registered":True,"router_implemented":bool(p)} for d,p in R.items()}
