from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_draft, build_skill_blocked
def route_skill(sid,env,ctx):
    if sid=="REPORT.RENDER_SKILLOS_STATUS_DRAFT": return build_skill_draft(sid,{"title":"SkillOS Status Draft","status":"DRAFT_ONLY"})
    if sid=="REPORT.RENDER_ZG16_STUB_SUMMARY_DRAFT": return build_skill_draft(sid,{"title":"ZG16 Stub Summary","status":"DRAFT_ONLY"})
    if sid=="REPORT.RENDER_CASEFORGE_REVIEW_DRAFT": return build_skill_draft(sid,{"title":"CaseForge Review Draft","status":"DRAFT_ONLY"})
    return build_skill_blocked(sid,"Unknown REPORT skill")
