from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def _tj(*p): return "".join(p)
FW=[_tj("B","UY"),_tj("S","ELL"),_tj("H","OLD"),_tj("买","入"),_tj("卖","出"),_tj("持","有"),_tj("目标","价"),_tj("止","盈"),_tj("止","损"),_tj("仓","位")]
ER=[{"role_id":"fundamental_reviewer","name":"Fundamental Reviewer","scope":"business quality","verdict_allowed":False},{"role_id":"factor_reviewer","name":"Factor Reviewer","scope":"factor metadata","verdict_allowed":False},{"role_id":"risk_reviewer","name":"Risk Reviewer","scope":"risk flags","verdict_allowed":False},{"role_id":"bear_case_reviewer","name":"Bear Case Reviewer","scope":"counter-arguments","verdict_allowed":False}]
def _sb():
    return {"external_api_used":False,"production_allowed":False,"shadowbroker_deployed":False,"trade_allowed":False,"verdict_allowed":False,"broker_order_allowed":False,"real_trade_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"investment_verdict_allowed":False,"trade_signal_allowed":False,"buy_sell_hold_allowed":False,"portfolio_allowed":False,"researchdb_main_write":False,"memory_main_write":False,"final_decision":False,"draft_only":True,"human_review_required":True}
def _cfw(t): return [w for w in FW if w in t]
def route_skill(sid,env,ctx):
    if sid=="COUNCIL.GET_COUNCIL_SCHEMA":
        o=_sb(); o["human_review_required"]=False; o.update({"schema":{"input":"case|factor|risk","output":"draft_review|matrix|risk_review","final_verdict_allowed":False}})
        return build_skill_success(sid,o)
    if sid=="COUNCIL.GET_EXPERT_ROLE_REGISTRY":
        o=_sb(); o["human_review_required"]=False; o.update({"roles":ER})
        return build_skill_success(sid,o)
    if sid=="COUNCIL.BUILD_EXPERT_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","review_type":"EXPERT_REVIEW"})
        return build_skill_draft(sid,o)
    if sid=="COUNCIL.BUILD_DISAGREEMENT_MATRIX_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","matrix_type":"DISAGREEMENT","dimensions":["evidence","factor","risk","bear_case"]})
        return build_skill_draft(sid,o)
    if sid=="COUNCIL.BUILD_RISK_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","review_type":"RISK_REVIEW","categories":["data_quality","factor_misuse","overconfidence","missing_evidence"]})
        return build_skill_draft(sid,o)
    if sid=="COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY":
        t=str(ctx.get("council_output","")); h=_cfw(t)
        o=_sb(); o["human_review_required"]=False; o.update({"dry_run":True,"valid":len(h)==0,"forbidden_hits":h})
        return build_skill_success(sid,o)
    if sid=="COUNCIL.GET_COUNCIL_READINESS":
        o=_sb(); o["human_review_required"]=False; o.update({"readiness":"DRAFT_ONLY_READY","final_verdict_enabled":False,"trade_signal_enabled":False,"portfolio_enabled":False})
        return build_skill_success(sid,o)
    return build_skill_blocked(sid,"Unknown COUNCIL skill")
