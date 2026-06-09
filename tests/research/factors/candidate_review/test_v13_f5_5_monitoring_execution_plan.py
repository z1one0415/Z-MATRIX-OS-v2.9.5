"""V13.F5.5 Monitoring Execution Plan Tests."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_monitoring_execution_plan")

def _l(n): return json.loads((D / n).read_text())

def test_dir_and_files():
    assert D.exists()
    assert len(list(D.glob("*.json"))) == 7

def test_contract():
    c = _l("v13_f5_5_monitoring_execution_plan_contract.json")
    assert c["planning_only"] is True
    assert c["monitoring_execution_allowed"] is False
    assert len(c["monitoring_scope"]) == 10
    assert c["production"] == "BLOCKED"

def test_oos_availability():
    a = _l("v13_f5_5_oos_label_availability_audit.json")
    assert a["horizon_availability"]["20D"]["available"] is True
    assert a["horizon_availability"]["60D"]["available"] is False
    assert a["labels_require_generation_before_monitoring"] is True

def test_readiness_matrix():
    r = _l("v13_f5_5_factor_horizon_readiness_matrix.json")
    assert r["fully_ready_count"] == 4
    assert r["partial_ready_count"] == 6
    assert "F11" in r["fully_ready_factors"]
    assert "F21" in r["partial_ready_factors"]

def test_partial_policy():
    p = _l("v13_f5_5_partial_monitoring_policy.json")
    assert p["partial_monitoring_allowed"] is True
    assert len(p["eligible_for_first_partial_monitoring"]) == 10

def test_schema():
    s = _l("v13_f5_5_monitoring_execution_schema.json")
    assert "rank_ic" in s["report_fields"]
    assert "PROMOTED" in s["forbidden_decisions"]

def test_safety():
    sa = _l("v13_f5_5_monitoring_execution_safety_audit.json")
    assert sa["violation_count"] == 0
    assert sa["checks"]["monitoring_execution_executed"] is False
    assert sa["checks"]["production_blocked"] is True

def test_closeout():
    co = _l("v13_f5_5_monitoring_execution_plan_closeout.json")
    assert co["ready_for_first_monitoring_execution"] is True
    assert co["labels_require_generation_first"] is True
    assert co["monitoring_execution_executed"] is False
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert "F5_5_1" in co["recommended_next_action"]
