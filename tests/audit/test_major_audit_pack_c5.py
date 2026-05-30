#!/usr/bin/env python3
"""Pack C.5: Core Module Re-Audit Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_reaudit_report_exists(): assert (WORKSPACE / "docs" / "audit" / "CORE_MODULE_REAUDIT_AFTER_C4_1.md").exists()
def test_reaudit_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "core_module_reaudit_after_c4_1.json").exists()
def test_c5_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C5_CLOSEOUT.md").exists()

def test_7_core_modules():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_reaudit_after_c4_1.json").read_text())
    modules = {r["module"] for r in data}
    assert modules == {"account_truth","master_data","market_data","outcome_engine","attribution","replay","council"}

def test_p1_blocking_zero():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_reaudit_after_c4_1.json").read_text())
    blocking = sum(1 for r in data if r.get("blocking_after"))
    assert blocking == 0

def test_p1_fixed_two():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_reaudit_after_c4_1.json").read_text())
    fixed = sum(1 for r in data if r.get("current_risk") == "P1_FIXED")
    assert fixed == 2

def test_account_truth_verdict_pass():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_reaudit_after_c4_1.json").read_text())
    at = next(r for r in data if r["module"] == "account_truth")
    assert at["verdict"] == "PASS"

def test_c5_closeout_status():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C5_CLOSEOUT.md").read_text()
    assert "PACK_C5_PASS" in text or "PACK_C5_REPAIR_REQUIRED" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
