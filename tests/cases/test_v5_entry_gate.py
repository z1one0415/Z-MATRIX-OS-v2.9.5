"""Test V5 entry gate."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
GATE = WORKSPACE / "scripts" / "cases" / "check_v5_entry_gate.py"

def test_v5_gate_runs():
    r = subprocess.run(["python3", str(GATE)], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0

def test_v5_gate_blocked():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["v5_entry_allowed"] is False
    assert "BLOCKED" in g["status"]

def test_v5_gate_price_zero():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["daily_price_real_read_only"] == 0
    assert g["ready_for_real_return"] == 0

def test_v5_gate_alpha_zero():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] == 0

def test_v5_gate_safety():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["production"] == "BLOCKED"
    assert g["broker_runtime"] == "BLOCKED"
    assert g["real_trade"] == "BLOCKED"

def test_v5_wont_enter_without_data():
    """V5 must not allow entry when 0 real data exists."""
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["v5_entry_allowed"] is False
