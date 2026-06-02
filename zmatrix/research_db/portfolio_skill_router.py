from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def _sb():
    return {"external_api_used":False,"production_allowed":False,"shadowbroker_deployed":False,"trade_allowed":False,"verdict_allowed":False,"broker_order_allowed":False,"real_trade_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"investment_verdict_allowed":False,"trade_signal_allowed":False,"buy_sell_hold_allowed":False,"portfolio_decision_allowed":False,"position_sizing_allowed":False,"order_generation_allowed":False,"target_price_allowed":False,"final_scoring_allowed":False,"backtest_allowed":False,"researchdb_main_write":False,"memory_main_write":False}
def route_skill(sid,env,ctx):
    if sid=="PORTFOLIO.GET_SCHEMA":
        o=_sb(); o["human_review_required"]=False; o.update({"schema":{"positions":"list","risk_budget":"object","exposure":"object"},"portfolio_decision_allowed":False,"order_generation_allowed":False})
        return build_skill_success(sid,o)
    if sid=="PORTFOLIO.GET_RISK_BUDGET_TEMPLATE":
        o=_sb(); o["human_review_required"]=False; o.update({"template":{"categories":["equity","fixed_income","cash","hedge"],"budget_type":"REVIEW_ONLY"},"portfolio_decision_allowed":False})
        return build_skill_success(sid,o)
    if sid=="PORTFOLIO.GET_EXPOSURE_TEMPLATE":
        o=_sb(); o["human_review_required"]=False; o.update({"template":{"dimensions":["sector","market_cap","factor_loading"],"exposure_type":"REVIEW_ONLY"},"portfolio_decision_allowed":False})
        return build_skill_success(sid,o)
    if sid=="PORTFOLIO.VALIDATE_PORTFOLIO_INPUT_DRY":
        inp=ctx.get("portfolio_input",{}); ms=[k for k in["positions","risk_budget"] if not inp.get(k)]
        o=_sb(); o["human_review_required"]=False; o.update({"dry_run":True,"valid":not ms,"missing":ms,"portfolio_decision_allowed":False,"order_generation_allowed":False})
        return build_skill_success(sid,o)
    if sid=="PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","review_type":"PORTFOLIO_REVIEW","portfolio_decision_allowed":False,"order_generation_allowed":False})
        return build_skill_draft(sid,o)
    if sid=="PORTFOLIO.GET_PORTFOLIO_READINESS":
        o=_sb(); o["human_review_required"]=False; o.update({"readiness":"REVIEW_DRAFT_ONLY_READY","portfolio_engine_enabled":False,"portfolio_decision_allowed":False,"order_generation_allowed":False,"position_sizing_allowed":False,"target_price_allowed":False})
        return build_skill_success(sid,o)
    return build_skill_blocked(sid,"Unknown PORTFOLIO skill")
