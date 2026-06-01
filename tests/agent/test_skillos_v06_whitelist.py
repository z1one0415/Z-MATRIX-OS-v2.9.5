import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v06.json")
def test_exists(): assert WL.exists()
def test_domain(): d=json.loads(WL.read_text()); assert d["selection_policy"]["allowed_domains"]==["FACTOR"]
def test_no_calc(): d=json.loads(WL.read_text())
 assert d["selection_policy"]["factor_calculation_allowed"] is False
 assert d["selection_policy"]["backtest_allowed"] is False
 assert d["selection_policy"]["ranking_allowed"] is False
 assert d["selection_policy"]["trading_signal_allowed"] is False
def test_prefix(): d=json.loads(WL.read_text())
 for sid in d["selected_skills"]: assert sid.startswith("FACTOR.")
