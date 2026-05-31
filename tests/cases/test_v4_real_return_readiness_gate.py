"""Test V4.1 real return readiness gate — FIXTURE ≠ REAL."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS = WORKSPACE / "scripts" / "cases" / "check_core12_real_market_data_readiness.py"
GATE = WORKSPACE / "scripts" / "cases" / "run_core12_real_return_readiness.py"

@pytest.fixture
def data():
    subprocess.run(["python3", str(READINESS)], cwd=str(WORKSPACE), capture_output=True)
    subprocess.run(["python3", str(GATE)], cwd=str(WORKSPACE), capture_output=True)
    rd = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json").read_text())
    rr = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json").read_text())
    return rd, rr

def test_core_001_fixture_not_real(data):
    rd, rr = data
    c001 = [c for c in rd["cases"] if c["case_id"] == "CORE_001"][0]
    assert c001["fixture_return_ready"] is True, "600519 has fixture data"
    assert c001["ready_for_real_return"] is False, "FIXTURE must not enable real return"

def test_core_001_return_blocked_fixture(data):
    _, rr = data
    c001 = [c for c in rr["cases"] if c["case_id"] == "CORE_001"][0]
    assert c001["real_return_status"] == "BLOCKED_FIXTURE_ONLY", f"Got {c001['real_return_status']}"
    assert c001["fixture_return_ready"] is True
    assert c001["ready_for_real_return"] is False
    assert c001["ready_for_alpha_claim"] is False

def test_core_002_blocked_missing(data):
    rd, rr = data
    c002 = [c for c in rd["cases"] if c["case_id"] == "CORE_002"][0]
    assert c002["ready_for_real_return"] is False
    c002r = [c for c in rr["cases"] if c["case_id"] == "CORE_002"][0]
    assert "MISSING" in c002r["real_return_status"] or "BLOCKED" in c002r["real_return_status"]

def test_readiness_summary_fixture_count(data):
    rd, _ = data
    assert rd["summary"]["fixture_return_ready"] == 1  # only 600519
    assert rd["summary"]["ready_for_real_return"] == 0  # no real data

def test_return_summary_real_zero(data):
    _, rr = data
    assert rr["summary"]["ready_for_real_return"] == 0
    assert rr["summary"]["fixture_return_ready"] == 1
    assert rr["summary"]["blocked_fixture_only"] == 1

def test_no_alpha(data):
    _, rr = data
    for c in rr["cases"]:
        assert c["ready_for_alpha_claim"] is False
        assert "BLOCKED" in c["council_status"]

def test_all_production_blocked(data):
    _, rr = data
    for c in rr["cases"]:
        assert c["production"] == "BLOCKED"
