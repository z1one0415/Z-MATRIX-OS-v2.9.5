import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v08.json")
def test_exists(): assert WL.exists()
def test_domains(): d=json.loads(WL.read_text()); assert set(d["selection_policy"]["allowed_domains"])=={"ZC35","BMATRIX","DMATRIX"}
def test_no_scoring(): d=json.loads(WL.read_text()); p=d["selection_policy"]; assert p["final_scoring_allowed"] is False and p["backtest_allowed"] is False
def test_count(): d=json.loads(WL.read_text()); assert len(d["selected_skills"])==15
