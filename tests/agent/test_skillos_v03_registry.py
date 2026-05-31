import json; from pathlib import Path
G=Path("data/research_db/agent/registry/skill_registry.generated.json"); W=Path("data/research_db/agent/registry/skill_selection_whitelist_v03.json")
def test_wl_registered():
    s={x["skill_id"] for x in json.loads(G.read_text())}; wl=json.loads(W.read_text())["selected_skills"]
    for sid in wl: assert sid in s
def test_count(): assert len(json.loads(G.read_text())) >= 46
def test_no_write(): 
    wl=set(json.loads(W.read_text())["selected_skills"])
    for s in json.loads(G.read_text()):
        if s["skill_id"] in wl: assert s.get("write_layers")==[] and s.get("production_allowed") is False
