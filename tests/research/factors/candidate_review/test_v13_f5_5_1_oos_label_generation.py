"""V13.F5.5.1 OOS Label Generation Tests."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_oos_label_generation")

def _l(n): return json.loads((D / n).read_text())

def test_dir_and_files():
    assert D.exists()
    assert len(list(D.glob("*.json"))) == 7
    assert (D / "v13_f5_5_1_oos_label_panel.csv").exists()

def test_contract():
    c = _l("v13_f5_5_1_oos_label_generation_contract.json")
    assert c["label_month"] == "2026-05"
    assert c["allowed_horizons"] == ["5D", "20D"]
    assert c["blocked_horizons"] == ["60D"]
    assert len(c["eligible_factors"]) == 10
    assert c["monitoring_execution_allowed"] is False
    assert c["production"] == "BLOCKED"

def test_price_data_audit():
    a = _l("v13_f5_5_1_oos_price_data_availability_audit.json")
    assert a["checks"]["5D_forward_window_complete"] is True
    assert a["checks"]["20D_forward_window_complete"] is True
    assert a["checks"]["60D_forward_window_complete"] is False
    assert a["checks"]["no_feature_store_write"] is True

def test_label_panel_manifest():
    m = _l("v13_f5_5_1_oos_label_panel_manifest.json")
    assert m["label_role"] == "OUTCOME_LABEL_ONLY"
    assert m["written_to_feature_store"] is False
    assert m["used_for_factor_calculation"] is False

def test_isolation():
    i = _l("v13_f5_5_1_oos_label_isolation_audit.json")
    assert i["violation_count"] == 0
    assert i["checks"]["no_factor_score_in_panel"] is True
    assert i["checks"]["no_alpha_signal_in_panel"] is True

def test_horizon_completeness():
    h = _l("v13_f5_5_1_oos_label_horizon_completeness.json")
    assert h["results"]["5D"] == "PASS"
    assert h["results"]["20D"] == "PASS"
    assert h["results"]["60D"] == "BLOCKED_NOT_GENERATED"

def test_safety():
    s = _l("v13_f5_5_1_oos_label_generation_safety_audit.json")
    assert s["violation_count"] == 0
    assert s["checks"]["oos_label_generation_executed"] is True
    assert s["checks"]["monitoring_execution_executed"] is False
    assert s["checks"]["production_blocked"] is True

def test_closeout():
    co = _l("v13_f5_5_1_oos_label_generation_closeout.json")
    assert co["oos_label_generation_executed"] is False
    assert co["generated_horizons"] == ["5D", "20D"]
    assert co["ready_for_first_monitoring_execution"] is False
    assert co["monitoring_execution_executed"] is False
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert "F5_5_2" in co["recommended_next_action"]

def test_csv_schema():
    csv_path = D / "v13_f5_5_1_oos_label_panel.csv"
    header = csv_path.read_text().strip().split("\n")[0]
    assert "ticker" in header
    assert "forward_return" in header
    assert "label_role" in header
