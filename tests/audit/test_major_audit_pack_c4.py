#!/usr/bin/env python3
"""Pack C.4: Blocking Risk Fix Implementation Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_fix_result_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "pack_c4_blocking_risk_fix_result.json").exists()
def test_c4_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C4_CLOSEOUT.md").exists()

def test_both_risks_fixed():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c4_blocking_risk_fix_result.json").read_text())
    assert len(data) == 2
    for r in data: assert r["status"] == "FIXED_IN_C4"

def test_risk_register_no_blocking():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_risk_register.json").read_text())
    blocking = [r for r in data if r.get("blocking_pack_d")]
    assert len(blocking) == 0, f"Still blocking: {blocking}"

def test_reconcile_tolerance_exists():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_with_tolerance
    r = reconcile_with_tolerance(100.0, 100.0)
    assert r["status"] == "PASS"
    assert r["difference_abs"] == 0

def test_reconcile_tolerance_error():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_with_tolerance
    r = reconcile_with_tolerance(100.0, 101.0, tolerance_abs=0.5, strict_mode=True)
    assert r["status"] == "ERROR"

def test_reconcile_output_has_fields():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_with_tolerance
    r = reconcile_with_tolerance(100, 100.01)
    for field in ["difference_abs", "difference_pct", "tolerance_abs", "tolerance_pct", "reconciliation_status"]:
        assert field in r

def test_replay_calendar_none_fail():
    from zmatrix.research_db.replay.replay_dataset import ReplayDataset
    from zmatrix.research_db.replay.replay_runner import ReplayRunner
    ds = ReplayDataset(tickers=["A"])
    runner = ReplayRunner(ds)
    r = runner.run_rolling_replay("E1", "2024-01-02", "2024-01-09")
    assert r.status in ("FAILED", "ERROR"), f"Expected FAILED, got {r.status}"
    assert "CALENDAR" in r.details.get("error_type", "").upper()

def test_closeout_not_claim_pack_d_pass():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C4_CLOSEOUT.md").read_text()
    assert "PACK_D_PASS" not in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
