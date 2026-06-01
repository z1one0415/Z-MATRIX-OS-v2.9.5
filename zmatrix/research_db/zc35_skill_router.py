from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def _sb():
    return {"external_api_used":False,"production_allowed":False,"shadowbroker_deployed":False,"trade_allowed":False,"verdict_allowed":False,"broker_order_allowed":False,"real_trade_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"investment_verdict_allowed":False,"trade_signal_allowed":False,"buy_sell_hold_allowed":False,"portfolio_allowed":False,"final_scoring_allowed":False,"backtest_allowed":False,"researchdb_main_write":False,"memory_main_write":False}
def route_skill(sid,env,ctx):
    if sid=="ZC35.GET_SCHEMA":
        o=_sb(); o["human_review_required"]=False; o.update({"schema":{"catalyst_id":"str","lifecycle_stage":"str","residual_power":"float"},"final_scoring":False})
        return build_skill_success(sid,o)
    if sid=="ZC35.GET_CHECKLIST":
        o=_sb(); o["human_review_required"]=False; o.update({"checklist":["catalyst_identified","lifecycle_stage_known","residual_power_estimated","sell_on_news_flag_set"],"final_scoring":False})
        return build_skill_success(sid,o)
    if sid=="ZC35.VALIDATE_INPUT_DRY":
        inp=ctx.get("zc35_input",{}); ms=[k for k in["catalyst_id","lifecycle_stage"] if not inp.get(k)]
        o=_sb(); o["human_review_required"]=False; o.update({"dry_run":True,"valid":not ms,"missing":ms})
        return build_skill_success(sid,o)
    if sid=="ZC35.BUILD_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","review_type":"ZC35_CATALYST_REVIEW"})
        return build_skill_draft(sid,o)
    if sid=="ZC35.GET_READINESS":
        o=_sb(); o["human_review_required"]=False; o.update({"readiness":"READ_ONLY_READY","final_scoring":False,"backtest":False})
        return build_skill_success(sid,o)
    return build_skill_blocked(sid,"Unknown ZC35 skill")
