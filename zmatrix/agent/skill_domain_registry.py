from __future__ import annotations
PREFIX={"SYSTEM":"","RESEARCHDB":"","DATAFORGE":"","FACTOR":"","COUNCIL":"","REPORT":"","CASEFORGE":"","AUTOCASE":"","ZG16":"zmatrix.research_db.zg16_skill_router","ZC35":"","BMATRIX":"","DMATRIX":"","PORTFOLIO":"","GOVERNANCE":"","COCKPIT":"","MEMORY":"","WORKFLOW":""}
def get_skill_domain(sid): return sid.split(".",1)[0].upper() if "." in sid else "UNKNOWN"
def has_domain_router(sid): return get_skill_domain(sid) in PREFIX
