import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v07.json")
def test_exists(): assert WL.exists()
def test_domain(): d=json.loads(WL.read_text()); assert d["selection_policy"]["allowed_domains"]==["COUNCIL"]
def test_no_verdict(): d=json.loads(WL.read_text()); p=d["selection_policy"]; assert p["investment_verdict_allowed"] is False and p["trade_signal_allowed"] is False and p["portfolio_allowed"] is False
def test_prefix(): d=json.loads(WL.read_text())
 for sid in d["selected_skills"]: assert sid.startswith("COUNCIL.")
