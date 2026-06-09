"""V13.F5.5.1.1 Label Status Canonicalization Tests."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_oos_label_generation")

def _l(n): return json.loads((D / n).read_text())

def test_canonicalization_exists():
    assert (D / "v13_f5_5_1_1_label_status_canonicalization_closeout.json").exists()

def test_canonicalization_status():
    co = _l("v13_f5_5_1_1_label_status_canonicalization_closeout.json")
    assert co["status"] == "V13_F5_5_1_1_LABEL_STATUS_CANONICALIZATION_PASS"
    assert co["prior_status_corrected"] is True
    assert co["prior_ready_for_first_monitoring_execution_was_wrong"] is True

def test_actual_labels_not_generated():
    co = _l("v13_f5_5_1_1_label_status_canonicalization_closeout.json")
    assert co["actual_forward_returns_generated"] is False
    assert co["label_data_row_count"] == 0
    assert co["ready_for_first_monitoring_execution"] is False

def test_closeout_corrected():
    co = _l("v13_f5_5_1_oos_label_generation_closeout.json")
    assert co["status"] == "V13_F5_5_1_OOS_LABEL_SCHEMA_PLACEHOLDER_ONLY"
    assert co["oos_label_generation_executed"] is False
    assert co["label_schema_generated"] is True
    assert co["actual_forward_returns_generated"] is False
    assert co["ready_for_first_monitoring_execution"] is False

def test_no_ready_for_monitoring_in_f5_5_1():
    """Critical: ready_for_first_monitoring_execution must NOT be true anywhere in F5.5.1."""
    for f in D.glob("*.json"):
        data = json.loads(f.read_text())
        if "ready_for_first_monitoring_execution" in data:
            assert data["ready_for_first_monitoring_execution"] is False, f"WRONG in {f.name}"

def test_safety_boundary():
    co = _l("v13_f5_5_1_1_label_status_canonicalization_closeout.json")
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"

def test_next_action():
    co = _l("v13_f5_5_1_1_label_status_canonicalization_closeout.json")
    assert "F5_5_1_2" in co["recommended_next_action"]
