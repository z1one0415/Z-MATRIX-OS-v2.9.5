"""Test V13.F6.4.2 Closeout."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_closeout_pass():
    co = _l("v13_f6_4_2_closeout.json")
    assert co["status"] == "V13_F6_4_2_HISTORICAL_STATUS_PRESERVATION_PATCH_PASS"
    assert co["patches_applied"] == 6

def test_status_fixes():
    co = _l("v13_f6_4_2_closeout.json")
    fixes = co["status_fixes"]
    assert fixes["rejected_restored"] == ["F02","F03","F05"]
    assert fixes["orange_monitoring_restored"] == ["F01"]
    assert fixes["source_audit_restored"] == ["F17","F18","F19","F20"]
    assert fixes["non_informative_labeled"] == ["F13"]
    assert fixes["watch_only_corrected"] == ["F22","F26","F27","F34"]
    assert fixes["hypothesis_sidecar_added"] == ["F03R"]

def test_informative_count():
    co = _l("v13_f6_4_2_closeout.json")
    assert co["corrected_tally"]["materialized_informative"] == 23
    assert co["corrected_tally"]["materialized_non_informative"] == 1

def test_blocked():
    co = _l("v13_f6_4_2_closeout.json")
    assert co["alpha_claim_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"

def test_next_action():
    co = _l("v13_f6_4_2_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F7_0_CANONICAL_REGISTRY_UPDATE_AFTER_STATUS_REPAIR"
