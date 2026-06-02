from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
def _sb():
    return {"external_api_used":False,"production_allowed":False,"shadowbroker_deployed":False,"trade_allowed":False,"verdict_allowed":False,"broker_order_allowed":False,"real_trade_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"investment_verdict_allowed":False,"trade_signal_allowed":False,"buy_sell_hold_allowed":False,"portfolio_allowed":False,"portfolio_decision_allowed":False,"order_generation_allowed":False,"workflow_execution_allowed":False,"multi_domain_execution_allowed":False,"broker_runtime_allowed":False,"position_sizing_allowed":False,"target_price_allowed":False,"researchdb_main_write":False,"memory_main_write":False}
def route_skill(sid,env,ctx):
    if sid=="WORKFLOW.GET_WORKFLOW_SCHEMA":
        o=_sb(); o["human_review_required"]=False; o.update({"schema":{"stages":["data","factor","review","draft"],"execution_allowed":False}})
        return build_skill_success(sid,o)
    if sid=="WORKFLOW.GET_STAGE_TEMPLATE":
        o=_sb(); o["human_review_required"]=False; o.update({"template":{"stages":4,"orchestration":"DRY_RUN_ONLY","execution_allowed":False}})
        return build_skill_success(sid,o)
    if sid=="WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","plan_type":"RESEARCH_PLAN"})
        return build_skill_draft(sid,o)
    if sid=="WORKFLOW.BUILD_MULTI_DOMAIN_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","review_type":"MULTI_DOMAIN_REVIEW","domains":["FACTOR","COUNCIL","ZG16"]})
        return build_skill_draft(sid,o)
    if sid=="WORKFLOW.RUN_RESEARCH_DRY_CHAIN":
        o=_sb(); o["human_review_required"]=False; o.update({"dry_run":True,"workflow_execution_allowed":False,"multi_domain_execution_allowed":False,"plan_only":True})
        return build_skill_success(sid,o)
    if sid=="WORKFLOW.VALIDATE_WORKFLOW_INPUT_DRY":
        inp=ctx.get("workflow_input",{}); ms=[k for k in["stage","domain"] if not inp.get(k)]
        o=_sb(); o["human_review_required"]=False; o.update({"dry_run":True,"valid":not ms,"missing":ms})
        return build_skill_success(sid,o)
    if sid=="WORKFLOW.GET_WORKFLOW_READINESS":
        o=_sb(); o["human_review_required"]=False; o.update({"readiness":"DRY_RUN_ONLY_READY","workflow_engine_enabled":False,"workflow_execution_allowed":False,"multi_domain_execution_allowed":False,"order_generation_allowed":False,"portfolio_decision_allowed":False,"portfolio_allowed":False})
        return build_skill_success(sid,o)
    return build_skill_blocked(sid,"Unknown WORKFLOW skill")
