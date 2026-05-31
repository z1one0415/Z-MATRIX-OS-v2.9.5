"""Test V4 real return readiness gate."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS = WORKSPACE / "scripts" / "cases" / "check_core12_real_market_data_readiness.py"
GATE = WORKSPACE / "scripts" / "cases" / "run_core12_real_return_readiness.py"

@pytest.fixture
def return_readiness():
    subprocess.run(["python3", str(READINESS)], cwd=str(WORKSPACE), capture_output=True)
    subprocess.run(["python3", str(GATE)], cwd=str(WORKSPACE), capture_output=True)
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json").read_text())

def test_return_12_cases(return_readiness):
    assert len(return_readiness["cases"]) == 12

def test_return_no_alpha(return_readiness):
    for c in return_readiness["cases"]:
        assert c["ready_for_alpha_claim"] is False, f"{c['case_id']}: alpha_claim should be False"

def test_return_council_blocked(return_readiness):
    for c in return_readiness["cases"]:
        assert "BLOCKED" in c["council_status"], f"{c['case_id']}: council should be blocked"

def test_return_production_blocked(return_readiness):
    for c in return_readiness["cases"]:
        assert c["production"] == "BLOCKED"

def test_return_no_buy_sell(return_readiness):
    text = json.dumps(return_readiness)
    assert '"BUY"' not in text.upper()

def test_return_summary_fields(return_readiness):
    s = return_readiness["summary"]
    for f in ["total", "ready_for_real_return", "ready_for_alpha_claim", "blocked_missing_price"]:
        assert f in s

def test_return_graceful_missing_data():
    """When data is missing, return readiness should handle gracefully (not crash)."""
    r = subprocess.run(["python3", str(GATE)], cwd=str(WORKSPACE), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
