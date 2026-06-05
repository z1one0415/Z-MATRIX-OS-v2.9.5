import json; from pathlib import Path
G=Path("data/research_db/agent/registry/skill_registry.generated.json"); W=Path("data/research_db/agent/registry/skill_selection_whitelist_v09.json")
def test_wl_registered():
    s={x["skill_id"] for x in json.loads(G.read_text())}
    for sid in json.loads(W.read_text())["selected_skills"]: assert sid in s
def test_count(): assert len(json.loads(G.read_text())) >= 97
def test_draft():
    for s in json.loads(G.read_text()):
        if s["skill_id"]=="PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT": assert s["requires_human_review"] and s["proposal_required"]
