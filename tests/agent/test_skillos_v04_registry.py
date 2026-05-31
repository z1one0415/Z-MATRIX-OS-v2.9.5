import json; from pathlib import Path
G=Path("data/research_db/agent/registry/skill_registry.generated.json"); W=Path("data/research_db/agent/registry/skill_selection_whitelist_v04.json")
def test_wl(): 
    s={x["skill_id"] for x in json.loads(G.read_text())}; wl=json.loads(W.read_text())["selected_skills"]
    for sid in wl: assert sid in s
def test_write_review():
    wl=set(json.loads(W.read_text())["selected_skills"])
    for s in json.loads(G.read_text()):
        if s["skill_id"] in wl and s.get("write_layers"): assert s["requires_human_review"] and s["proposal_required"]
def test_no_main():
    for s in json.loads(G.read_text()): assert s.get("production_allowed") is False
