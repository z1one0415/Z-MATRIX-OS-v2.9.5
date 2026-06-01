from pathlib import Path
def _tj(*p): return "".join(p)
def _ft():
    ks=["external_api_used","shadowbroker_deployed","production_allowed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed"]
    ts=[]
    for k in ks:
        ts.append(_tj(k,"=","True"))
        ts.append(_tj(k," = ","True"))
        ts.append(_tj(chr(34),k,chr(34),": ","true"))
        ts.append(_tj(chr(34),k,chr(34),": ","True"))
        ts.append(_tj(chr(39),k,chr(39),": ","True"))
    ts.append(_tj("subprocess",".run("))
    ts.append(_tj("os",".system("))
    return ts
def test_gov_no_embed():
    t=Path("zmatrix/research_db/governance_skill_router.py").read_text("utf-8")
    for x in _ft(): assert x not in t,f"gov embed:{x}"
def test_self_no_embed():
    t=Path(__file__).read_text("utf-8")
    for x in _ft(): assert x not in t,"self embed"
