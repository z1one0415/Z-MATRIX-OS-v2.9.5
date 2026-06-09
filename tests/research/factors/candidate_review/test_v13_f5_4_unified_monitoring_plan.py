"""V13.F5.4 Unified Candidate Monitoring Plan Update Tests."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_4_unified_monitoring")

def _l(n): return json.loads((D / n).read_text())

def test_dir_and_files():
    assert D.exists()
    assert len(list(D.glob("*.json"))) == 9

def test_contract():
    c = _l("v13_f5_4_unified_monitoring_update_contract.json")
    assert c["monitoring_scope"] == ["F04","F10","F11","F14","F15","F16","F21","F24","F30","F31"]
    assert c["updated_frozen_candidate_count"] == 10
    assert c["monitoring_execution_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["production"] == "BLOCKED"

def test_scope_registry():
    s = _l("v13_f5_4_unified_monitoring_scope_registry.json")
    assert len(s["monitored_candidates"]) == 10
    assert "F21" in s["monitored_candidates"]
    assert s["monitored_candidates"]["F31"]["type"] == "DOWNSIDE_TAIL_RISK_REGIME"

def test_metrics():
    m = _l("v13_f5_4_monitoring_metric_registry_update.json")
    assert len(m["global_metrics"]) >= 10
    assert "F21" in m["batch3_specific_metrics"]
    assert "trend_persistence_score" in m["batch3_specific_metrics"]["F21"]

def test_rules():
    r = _l("v13_f5_4_per_factor_monitoring_rules_update.json")
    assert "F21" in r["rules"]
    assert "retain" in r["rules"]["F21"]
    assert "suspension_review" in r["rules"]["F31"]

def test_state_machine():
    sm = _l("v13_f5_4_unified_monitoring_state_machine_update.json")
    assert "FROZEN" in sm["allowed_states"]
    assert "OVERLAP_DRIFT_WARNING" in sm["allowed_states"]
    assert "PROMOTED" in sm["forbidden_states"]
    assert "REAL_TRADE_READY" in sm["forbidden_states"]

def test_calendar():
    cal = _l("v13_f5_4_monitoring_trigger_calendar_update.json")
    assert cal["minimum_oos_start_exclusive"] == "20260501"
    assert cal["oos_label_generation_executed_this_round"] is False
    assert cal["monitoring_execution_executed_this_round"] is False

def test_watch_only():
    w = _l("v13_f5_4_watch_only_monitoring_backlog.json")
    assert w["watch_only"] == ["F22","F26","F27","F34"]
    assert w["watch_only_not_in_frozen_monitoring_scope"] is True
    assert w["promotion_allowed"] is False

def test_safety():
    sa = _l("v13_f5_4_unified_monitoring_plan_safety_audit.json")
    assert sa["violation_count"] == 0
    assert sa["checks"]["monitoring_execution_executed"] is False
    assert sa["checks"]["runner_enabled"] is False
    assert sa["checks"]["production_blocked"] is True

def test_closeout():
    co = _l("v13_f5_4_unified_monitoring_plan_closeout.json")
    assert co["monitoring_plan_update_executed"] is True
    assert co["monitoring_execution_executed"] is False
    assert co["frozen_candidate_count"] == 10
    assert co["promotion_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert "F5_5" in co["recommended_next_action"]

def test_registry():
    r = json.loads(Path("research/factor_library/registry.json").read_text())
    assert r["monitoring_plan_updated"] is True
    assert r["monitoring_execution_executed"] is False
    assert len(r["monitoring_plan_scope"]) == 10
