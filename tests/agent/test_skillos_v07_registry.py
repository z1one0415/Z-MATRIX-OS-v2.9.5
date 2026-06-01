import json
from pathlib import Path

GEN = Path("data/research_db/agent/registry/skill_registry.generated.json")
WL = Path("data/research_db/agent/registry/skill_selection_whitelist_v07.json")

def _skills():
    return json.loads(GEN.read_text())

def test_wl_registered():
    skills = {s["skill_id"] for s in _skills()}
    selected = json.loads(WL.read_text())["selected_skills"]
    for sid in selected:
        assert sid in skills

def test_count():
    assert len(_skills()) >= 76

def test_draft_review():
    for s in _skills():
        if s["skill_id"].startswith("COUNCIL.BUILD_"):
            assert s["requires_human_review"] is True
            assert s["proposal_required"] is True
