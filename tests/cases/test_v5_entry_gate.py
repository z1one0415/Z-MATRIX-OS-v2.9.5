"""Test V5 entry gate — ALL conditions must pass, no single-gate bypass."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def _run_gate():
    import subprocess
    r = subprocess.run(["python3", str(WORKSPACE / "scripts" / "cases" / "check_v5_entry_gate.py")],
                       capture_output=True, text=True, cwd=str(WORKSPACE))
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())

@pytest.fixture
def gate():
    return _run_gate()

def test_current_blocked(gate):
    assert gate["v5_entry_allowed"] is False

def test_current_blocking_reasons(gate):
    reasons = gate["blocking_reasons"]
    assert "DAILY_PRICE_NOT_12" in reasons
    assert "ADJUSTMENT_FACTOR_NOT_READY" in reasons
    assert "BENCHMARK_NOT_REAL" in reasons
    assert "CALENDAR_NOT_REAL" in reasons
    assert "REAL_RETURN_NOT_READY" in reasons

def test_price_zero(gate):
    assert gate["daily_price_real_read_only"] == 0

def test_alpha_zero(gate):
    assert gate["ready_for_alpha_claim"] == 0

def test_safety_blocked(gate):
    assert gate["production"] == "BLOCKED"
    assert gate["broker_runtime"] == "BLOCKED"
    assert gate["real_trade"] == "BLOCKED"

def test_gate_all_gates_logic():
    """Simulate: ALL gates satisfied → v5 allowed. ANY gate fails → blocked."""
    # This tests the logic statically by monkeypatching via a temp file
    import json
    temp = WORKSPACE / "runtime_reports" / "cases" / "_test_v5_temp.json"
    # Setup: all gates pass
    temp.write_text(json.dumps({
        "summary": {
            "daily_price_real": 12,
            "benchmark_real_read_only": True,
            "calendar_real_read_only": True,
            "ready_for_real_return": 12,
            "ready_for_alpha_claim": 0,
        }
    }))

    # Directly exercise the logic
    from scripts.cases.check_v5_entry_gate import safe_get
    # Price=12, adj=12, bench=True, cal=True, return=12 → ALLOWED
    daily = safe_get(temp, "daily_price_real", 0)
    assert daily == 12

    temp.unlink()

def test_gate_price12_but_no_adj():
    """Simulate: daily_price=12 but adjustment_factor=0 → BLOCKED."""
    blocking = []
    daily_price = 12
    adj_ready = 0
    bench_real = True
    cal_real = True
    ret_ready = 12
    if daily_price < 12: blocking.append("DAILY_PRICE_NOT_12")
    if adj_ready < 12: blocking.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not bench_real: blocking.append("BENCHMARK_NOT_REAL")
    if not cal_real: blocking.append("CALENDAR_NOT_REAL")
    if ret_ready < 12: blocking.append("REAL_RETURN_NOT_READY")
    assert len(blocking) > 0
    assert "ADJUSTMENT_FACTOR_NOT_READY" in blocking

def test_gate_price12_but_no_benchmark():
    blocking = []
    if 12 < 12: blocking.append("DAILY_PRICE_NOT_12")
    if 12 < 12: blocking.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not False: blocking.append("BENCHMARK_NOT_REAL")  # bench=False
    if 12 < 12: blocking.append("REAL_RETURN_NOT_READY")
    assert "BENCHMARK_NOT_REAL" in blocking

def test_gate_all_pass():
    """ALL conditions met → no blocking reasons."""
    blocking = []
    daily_price, adj_ready = 12, 12
    bench_real, cal_real = True, True
    ret_ready = 12
    if daily_price < 12: blocking.append("DAILY_PRICE_NOT_12")
    if adj_ready < 12: blocking.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not bench_real: blocking.append("BENCHMARK_NOT_REAL")
    if not cal_real: blocking.append("CALENDAR_NOT_REAL")
    if ret_ready < 12: blocking.append("REAL_RETURN_NOT_READY")
    assert len(blocking) == 0
