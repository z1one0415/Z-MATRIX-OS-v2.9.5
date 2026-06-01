import json; from pathlib import Path
G=Path("data/research_db/agent/registry/skill_registry.generated.json"); W=Path("data/research_db/agent/registry/skill_selection_whitelist_v05.json")
def test_wl_registered():
    s={x["skill_id"] for x in json.loads(G.read_text())}; wl=json.loads(W.read_text())["selected_skills"]
    for sid in wl: assert sid in s
def test_count(): assert len(json.loads(G.read_text())) >= 63
def test_draft_review():
    for s in json.loads(G.read_text()):
        if s["skill_id"] in {"GOVERNANCE.BUILD_VERIFY_REPORT_DRAFT","GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT"}:
            assert s["requires_human_review"] and s["proposal_required"] and s["write_layers"]==["drafts"]
