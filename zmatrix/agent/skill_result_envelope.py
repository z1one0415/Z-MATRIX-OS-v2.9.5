from __future__ import annotations
def _b(sid): return {"skill_id":sid,"status":"","quality_status":"","output":{},"blocked_reason":"","human_review_required":True,"proposal_required":False,"production_allowed":False,"external_api_used":False,"shadowbroker_deployed":False,"trade_allowed":False,"verdict_allowed":False,"token_estimate":0,"evidence_refs":[],"runtime_ledger_written":False,"researchdb_main_write":False}
def build_skill_success(sid,out=None,qs="OK"):
 r=_b(sid); r.update({"status":"EXECUTED","quality_status":qs,"output":out or {},"human_review_required":False}); return r
def build_skill_draft(sid,out=None,qs="DRAFT"):
 r=_b(sid); r.update({"status":"DRAFT_CREATED","quality_status":qs,"output":out or {},"human_review_required":True,"proposal_required":True}); return r
def build_skill_blocked(sid,reason):
 r=_b(sid); r.update({"status":"BLOCKED","quality_status":"REJECTED","blocked_reason":reason,"human_review_required":True}); return r
def normalize_skill_result(sid,result):
 r=_b(sid); r.update(result or {}); r["production_allowed"]=r["external_api_used"]=r["shadowbroker_deployed"]=r["trade_allowed"]=r["verdict_allowed"]=False; return r
def assert_safe_skill_result(r): return all(not r.get(k) for k in ["production_allowed","external_api_used","shadowbroker_deployed","trade_allowed","verdict_allowed","runtime_ledger_written","researchdb_main_write"])
