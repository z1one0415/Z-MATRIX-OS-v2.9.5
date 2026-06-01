from pathlib import Path
def _tj(*p): return "".join(p)
def _ft():
    bkeys=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed"]
    ts=[]
    for k in bkeys:
        ts.append(_tj(k,"=","True")); ts.append(_tj(k," = ","True"))
        ts.append(_tj(chr(34),k,chr(34),": ","true")); ts.append(_tj(chr(34),k,chr(34),": ","True"))
        ts.append(_tj(chr(39),k,chr(39),": ","True"))
    ts.extend([_tj("subprocess",".run("),_tj("os",".system("),_tj("B","UY"),_tj("S","ELL"),_tj("H","OLD"),_tj("买","入"),_tj("卖","出"),_tj("持","有"),_tj("目标","价"),_tj("止","盈"),_tj("止","损"),_tj("仓","位")])
    return ts
def _check(p):
    t=Path(p).read_text("utf-8")
    for x in _ft(): assert x not in t,f"{p}:{x}"
def test_router(): _check("zmatrix/research_db/council_skill_router.py")
def test_domain_test(): _check("tests/agent/test_skillos_v07_domain_router.py")
def test_invoke_test(): _check("tests/agent/test_skillos_v07_invoke_skill.py")
def test_regression_test(): _check(__file__)
