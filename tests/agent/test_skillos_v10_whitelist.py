import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v10.json")
def test_exists(): assert WL.exists()
def test_domain(): d=json.loads(WL.read_text()); assert d["selection_policy"]["allowed_domains"]==["WORKFLOW"]
def test_no_exec(): d=json.loads(WL.read_text()); p=d["selection_policy"]; assert p["workflow_execution_allowed"] is False and p["multi_domain_execution_allowed"] is False
def test_count(): d=json.loads(WL.read_text()); assert len(d["selected_skills"])==7
