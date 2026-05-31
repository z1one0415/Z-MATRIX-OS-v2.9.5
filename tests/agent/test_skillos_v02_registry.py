import json; from pathlib import Path
G=Path("data/research_db/agent/registry/skill_registry.generated.json"); W=Path("data/research_db/agent/registry/skill_selection_whitelist_v02.json")
def _s(): return json.loads(G.read_text())
def test_wl_in_generated():
    s={x["skill_id"] for x in _s()}; wl=json.loads(W.read_text())["selected_skills"]
    for sid in wl: assert sid in s
def test_count(): assert len(_s())>=34
def test_safe():
    for x in _s(): assert x.get("production_allowed") is False
def test_write_review():
    for x in _s():
        if x.get("write_layers"): assert x["requires_human_review"] and x["proposal_required"]
