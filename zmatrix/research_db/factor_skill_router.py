from __future__ import annotations
from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked
FR=[{"factor_id":"QUALITY_PLACEHOLDER","category":"quality","status":"METADATA_ONLY","calculation_enabled":False,"requires_real_data":True},{"factor_id":"MOMENTUM_PLACEHOLDER","category":"momentum","status":"METADATA_ONLY","calculation_enabled":False,"requires_real_data":True},{"factor_id":"VALUATION_PLACEHOLDER","category":"valuation","status":"METADATA_ONLY","calculation_enabled":False,"requires_real_data":True}]
FS={"factor_id":"string","category":"quality|momentum|valuation|risk|liquidity|event","input_requirements":"list","calculation_enabled":"boolean","backtest_enabled":"boolean","trading_signal_allowed":"boolean"}
def _sb():
    return {"external_api_used":False,"production_allowed":False,"trade_allowed":False,"verdict_allowed":False,"broker_order_allowed":False,"real_trade_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"factor_calculation_allowed":False,"backtest_allowed":False,"ranking_allowed":False,"trading_signal_allowed":False,"factor_engine_enabled":False,"calculation_enabled":False,"backtest_enabled":False,"ranking_enabled":False,"signal_enabled":False,"researchdb_main_write":False,"memory_main_write":False}
def route_skill(sid,env,ctx):
    if sid=="FACTOR.GET_FACTOR_REGISTRY":
        o=_sb(); o.update({"registry_status":"METADATA_ONLY","factors":FR}); return build_skill_success(sid,o)
    if sid=="FACTOR.GET_FACTOR_SCHEMA":
        o=_sb(); o.update({"schema":FS}); return build_skill_success(sid,o)
    if sid=="FACTOR.GET_FACTOR_METADATA_SUMMARY":
        cats={}
        for f in FR: cats[f["category"]]=cats.get(f["category"],0)+1
        o=_sb(); o.update({"factor_count":len(FR),"categories":cats}); return build_skill_success(sid,o)
    if sid=="FACTOR.VALIDATE_FACTOR_INPUT_DRY":
        p=ctx.get("factor_input",{}); ms=[k for k in["factor_id","category"] if not p.get(k)]
        o=_sb(); o.update({"dry_run":True,"valid":not ms,"missing":ms,"calculation_executed":False,"backtest_executed":False,"ranking_executed":False}); return build_skill_success(sid,o)
    if sid=="FACTOR.GET_FACTOR_READINESS":
        o=_sb(); o.update({"readiness":"READ_ONLY_READY"}); return build_skill_success(sid,o)
    if sid=="FACTOR.BUILD_FACTOR_REVIEW_DRAFT":
        o=_sb(); o.update({"draft_status":"DRAFT_ONLY","title":"Factor Metadata Review"}); return build_skill_draft(sid,o)
    return build_skill_blocked(sid,"Unknown FACTOR skill")
