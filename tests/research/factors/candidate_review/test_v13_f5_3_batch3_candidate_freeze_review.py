"""V13.F5.3 Batch3 Candidate Freeze Review Tests."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_3_candidate_freeze_review")
FILES = [
    "v13_f5_3_batch3_candidate_freeze_review_contract.json",
    "v13_f5_3_batch3_freeze_handoff_canonicalization.json",
    "v13_f5_3_batch3_freeze_evidence_provenance_audit.json",
    "v13_f5_3_batch3_freeze_scope_manifests.json",
    "v13_f5_3_batch3_watch_only_preservation.json",
    "v13_f5_3_batch3_freeze_guardrail_registry.json",
    "v13_f5_3_batch3_candidate_freeze_safety_audit.json",
    "v13_f5_3_batch3_candidate_freeze_closeout.json",
    "v13_f5_3_unified_candidate_registry_update.json",
]
def _l(n): return json.loads((D / n).read_text())

def test_dir_and_files():
    assert D.exists()
    for f in FILES: assert (D / f).exists(), f"Missing: {f}"

def test_contract():
    c = _l(FILES[0])
    assert c["freeze_review_scope"] == ["F21","F24","F30","F31"]
    assert c["candidate_freeze_allowed"] is True
    assert c["promotion_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["production"] == "BLOCKED"

def test_handoff():
    h = _l(FILES[1])
    assert h["status"] == "V13_F5_3_HANDOFF_CANONICALIZATION_PASS"
    assert h["freeze_review_scope"] == ["F21","F24","F30","F31"]

def test_evidence():
    e = _l(FILES[2])
    assert e["all_pass"] is True
    for fid in ["F21","F24","F30","F31"]:
        assert e["per_factor"][fid]["evidence_audit_pass"] is True

def test_freeze_manifests():
    m = _l(FILES[3])
    assert m["freeze_manifests"]["F21"]["freeze_status"] == "FROZEN_TACTICAL_CANDIDATE"
    assert m["freeze_manifests"]["F24"]["freeze_status"] == "FROZEN_TACTICAL_CANDIDATE"
    assert m["freeze_manifests"]["F30"]["freeze_status"] == "FROZEN_TACTICAL_CANDIDATE"
    assert m["freeze_manifests"]["F31"]["freeze_status"] == "FROZEN_REGIME_SPECIFIC_CANDIDATE"

def test_watch_only():
    w = _l(FILES[4])
    assert w["watch_only_preserved"] == ["F22","F26","F27","F34"]
    assert w["watch_only_not_frozen"] is True

def test_guardrails():
    g = _l(FILES[5])
    for fid in ["F21","F24","F30","F31"]:
        assert "TRUE_OOS_REQUIRED" in g["guardrails"][fid]
    assert g["promotion_blocked_until_oos"] is True

def test_safety():
    s = _l(FILES[6])
    assert s["violation_count"] == 0
    assert s["checks"]["watch_only_not_frozen"] is True
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["production_blocked"] is True

def test_closeout():
    co = _l(FILES[7])
    assert co["candidate_freeze_executed"] is True
    assert co["new_batch3_frozen_candidates"] == ["F21","F24","F30","F31"]
    assert len(co["all_frozen_candidates"]) == 10
    assert co["ready_for_f5_4_unified_candidate_monitoring_plan_update"] is True
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"

def test_registry_update():
    r = _l(FILES[8])
    assert len(r["all_frozen_candidates"]) == 10
    assert "F21" in r["all_frozen_candidates"]
    assert r["promotion_allowed"] is False

def test_registry_file():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert "F21" in reg.get("all_frozen_candidates", [])
    assert reg["next_legal_entry"] == "PREPARE_V13_F5_4_UNIFIED_CANDIDATE_MONITORING_PLAN_UPDATE"
