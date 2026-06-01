from pathlib import Path
def test_governance_router_no_embedded_forbidden_tokens():
    text=Path("zmatrix/research_db/governance_skill_router.py").read_text()
    for tok in ["external_api_used=True","shadowbroker_deployed=True","production_allowed=True","trade_allowed=True","verdict_allowed=True","broker_order_allowed=True","real_trade_allowed=True","auto_buy_allowed=True","auto_sell_allowed=True","subprocess.run(","os.system("]:
        assert tok not in text,f"governance router embeds: {tok}"
