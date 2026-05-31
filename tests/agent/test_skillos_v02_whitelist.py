import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v02.json")
def test_exists(): assert WL.exists()
def test_no_auto(): d=json.loads(WL.read_text()); assert d["selection_policy"]["candidate_auto_enable"] is False
def test_domains(): d=json.loads(WL.read_text()); assert set(d["selection_policy"]["allowed_domains"])=={"SYSTEM","ZG16","CASEFORGE","REPORT","COCKPIT"}
def test_r2(): d=json.loads(WL.read_text()); assert d["selection_policy"]["max_risk_level"]=="R2_DRAFT"
