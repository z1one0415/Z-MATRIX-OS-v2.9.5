import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v09.json")
def test_exists(): assert WL.exists()
def test_domain(): d=json.loads(WL.read_text()); assert d["selection_policy"]["allowed_domains"]==["PORTFOLIO"]
def test_no_trade(): d=json.loads(WL.read_text()); p=d["selection_policy"]; assert p["portfolio_decision_allowed"] is False and p["order_generation_allowed"] is False and p["buy_sell_hold_allowed"] is False
def test_count(): d=json.loads(WL.read_text()); assert len(d["selected_skills"])==6
