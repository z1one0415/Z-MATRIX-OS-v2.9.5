import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v05.json")
def test_exists(): assert WL.exists()
def test_domain(): d=json.loads(WL.read_text()); assert d["selection_policy"]["allowed_domains"]==["GOVERNANCE"]
def test_r2(): d=json.loads(WL.read_text()); assert d["selection_policy"]["max_risk_level"]=="R2_DRAFT"
def test_prefix(): d=json.loads(WL.read_text())
 for sid in d["selected_skills"]: assert sid.startswith("GOVERNANCE.")
