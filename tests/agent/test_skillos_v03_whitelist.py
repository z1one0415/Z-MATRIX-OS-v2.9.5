import json; from pathlib import Path
WL=Path("data/research_db/agent/registry/skill_selection_whitelist_v03.json")
def test_exists(): assert WL.exists()
def test_domains(): d=json.loads(WL.read_text()); assert set(d["selection_policy"]["allowed_domains"])=={"RESEARCHDB","DATAFORGE"}
def test_no_auto(): d=json.loads(WL.read_text()); assert d["selection_policy"]["candidate_auto_enable"] is False
def test_max_r1(): d=json.loads(WL.read_text()); assert d["selection_policy"]["max_risk_level"]=="R1_ANNOTATE"
