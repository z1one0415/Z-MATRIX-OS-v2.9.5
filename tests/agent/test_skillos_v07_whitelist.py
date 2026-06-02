import json
from pathlib import Path
WL = Path("data/research_db/agent/registry/skill_selection_whitelist_v07.json")
def test_exists():
    assert WL.exists()
def test_domain():
    data = json.loads(WL.read_text())
    assert data["selection_policy"]["allowed_domains"] == ["COUNCIL"]
def test_no_verdict():
    data = json.loads(WL.read_text())
    p = data["selection_policy"]
    assert p["investment_verdict_allowed"] is False
def test_prefix():
    data = json.loads(WL.read_text())
    for sid in data["selected_skills"]:
        assert sid.startswith("COUNCIL.")
