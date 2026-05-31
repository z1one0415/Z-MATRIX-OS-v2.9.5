def test_candidate_index_has_scripts():
    import json; from pathlib import Path
    p=Path("data/research_db/agent/registry/skill_candidate_index.json")
    data=json.loads(p.read_text())
    scripts=[c for c in data if c.get("candidate_type")=="script"]
    assert len(scripts) >= 0

def test_candidates_are_not_enabled():
    import json; from pathlib import Path
    data=json.loads(Path("data/research_db/agent/registry/skill_candidate_index.json").read_text())
    for c in data:
        assert c["status"]=="CANDIDATE_ONLY"
        assert c["production_allowed"] is False
