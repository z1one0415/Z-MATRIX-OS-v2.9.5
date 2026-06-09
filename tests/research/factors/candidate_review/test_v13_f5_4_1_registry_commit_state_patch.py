"""V13.F5.4.1 Registry Commit-State Patch Tests."""
import json
from pathlib import Path

REG = Path("research/factor_library/registry.json")
CO = Path("research/factor_library/reviews/batch_003/f5_4_1_registry_commit_state_patch/v13_f5_4_1_registry_commit_state_patch_closeout.json")

def test_files_exist():
    assert REG.exists()
    assert CO.exists()

def test_registry_version():
    r = json.loads(REG.read_text())
    assert r["version"] == "v13.f5.4.1"

def test_registry_current_head():
    r = json.loads(REG.read_text())
    assert r["current_head"] == "54b8fef"
    assert r["last_accepted_commit"] == "54b8fef"
    assert r["f5_4_monitoring_plan_commit"] == "54b8fef"

def test_registry_monitoring_preserved():
    r = json.loads(REG.read_text())
    assert r["monitoring_plan_updated"] is True
    assert r["monitoring_execution_executed"] is False
    assert len(r["monitoring_plan_scope"]) == 10

def test_registry_frozen():
    r = json.loads(REG.read_text())
    assert len(r["frozen_candidates"]) == 10
    assert "F21" in r["frozen_candidates"]

def test_registry_safety():
    r = json.loads(REG.read_text())
    assert r["runner_enabled"] is False
    assert r["execution_allowed"] is False
    assert r["promotion_allowed"] is False
    assert r["alpha_claim_allowed"] is False
    assert r["production"] == "BLOCKED"

def test_closeout_status():
    co = json.loads(CO.read_text())
    assert co["status"] == "V13_F5_4_1_REGISTRY_COMMIT_STATE_PATCH_PASS"
    assert co["registry_commit_state_patch_executed"] is True
    assert co["monitoring_plan_preserved"] is True
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"
