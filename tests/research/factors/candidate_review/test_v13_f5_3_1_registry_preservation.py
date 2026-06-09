"""V13.F5.3.1 Registry Preservation Canonicalization Tests."""
import json
from pathlib import Path

REG = Path("research/factor_library/registry.json")
CO = Path("research/factor_library/reviews/batch_003/f5_3_1_registry_preservation/v13_f5_3_1_registry_preservation_closeout.json")

def test_registry_exists():
    assert REG.exists()

def test_closeout_exists():
    assert CO.exists()

def test_registry_frozen_candidates():
    r = json.loads(REG.read_text())
    assert len(r["frozen_candidates"]) == 10
    assert "F21" in r["frozen_candidates"]
    assert "F24" in r["frozen_candidates"]
    assert "F30" in r["frozen_candidates"]
    assert "F31" in r["frozen_candidates"]

def test_registry_watch_only():
    r = json.loads(REG.read_text())
    assert r["watch_only"] == ["F22", "F26", "F27", "F34"]

def test_registry_rejected():
    r = json.loads(REG.read_text())
    assert r["rejected"] == ["F02", "F03", "F05"]

def test_registry_blocked_by_sample():
    r = json.loads(REG.read_text())
    assert r["blocked_by_sample"] == ["F06", "F07", "F08", "F12", "F13"]

def test_registry_source_audit():
    r = json.loads(REG.read_text())
    assert r["source_audit"] == ["F09", "F17", "F18", "F19", "F20"]

def test_registry_hypothesis_only():
    r = json.loads(REG.read_text())
    assert r["hypothesis_only"] == ["F03R"]

def test_registry_safety_boundary():
    r = json.loads(REG.read_text())
    assert r["runner_enabled"] is False
    assert r["execution_allowed"] is False
    assert r["promotion_allowed"] is False
    assert r["alpha_claim_allowed"] is False
    assert r["production"] == "BLOCKED"
    assert r["broker_runtime"] == "BLOCKED"
    assert r["real_trade"] == "BLOCKED"

def test_registry_next_legal_entry():
    r = json.loads(REG.read_text())
    assert r["next_legal_entry"] == "PREPARE_V13_F5_4_UNIFIED_CANDIDATE_MONITORING_PLAN_UPDATE"

def test_registry_governance_commits():
    r = json.loads(REG.read_text())
    assert r["merge_commit"] == "9d63225"
    assert r["clean_target_head"] == "b9dd7b5"
    assert r["f5_3_candidate_freeze_commit"] == "e89b78c"

def test_closeout_status():
    co = json.loads(CO.read_text())
    assert co["status"] == "V13_F5_3_1_REGISTRY_PRESERVATION_PASS"
    assert co["registry_preservation_executed"] is True
    assert co["f5_3_freeze_result_preserved"] is True
    assert len(co["all_frozen_candidates"]) == 10
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"
