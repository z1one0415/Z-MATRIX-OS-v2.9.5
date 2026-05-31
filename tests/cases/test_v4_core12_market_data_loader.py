"""Test V4 Core 12 market data loader and readiness."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS_SCRIPT = WORKSPACE / "scripts" / "cases" / "check_core12_real_market_data_readiness.py"

@pytest.fixture
def readiness():
    subprocess.run(["python3", str(READINESS_SCRIPT)], cwd=str(WORKSPACE), capture_output=True)
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json").read_text())

def test_readiness_12_cases(readiness):
    assert len(readiness["cases"]) == 12

def test_readiness_missing_marked(readiness):
    """All cases without real data must be marked MISSING or FIXTURE."""
    c002 = [c for c in readiness["cases"] if c["case_id"] == "CORE_002"][0]
    assert c002["daily_price_status"] in ("MISSING", "FIXTURE"), f"Expected MISSING, got {c002['daily_price_status']}"

def test_readiness_no_alpha(readiness):
    assert readiness["summary"]["ready_for_alpha_claim"] == 0

def test_readiness_blocked(readiness):
    for c in readiness["cases"]:
        assert c["production"] == "BLOCKED"
        assert c["broker_runtime"] == "BLOCKED"

def test_readiness_zero_real_if_no_data(readiness):
    """If processed/ is empty, price_real must be 0."""
    real = readiness["summary"]["daily_price_real"]
    fixture = readiness["summary"]["daily_price_fixture"]
    assert real + fixture <= 12

def test_readiness_has_summary_fields(readiness):
    s = readiness["summary"]
    for f in ["total", "daily_price_real", "daily_price_missing", "ready_for_real_return", "ready_for_alpha_claim"]:
        assert f in s

def test_protected_dirs_not_committed():
    """raw/staging/vendor must only contain .gitkeep files."""
    for dname in ["raw","staging","vendor"]:
        d = WORKSPACE / "data" / "research_db" / "market_data" / dname
        has_data = [f for f in d.glob("*") if f.name != ".gitkeep" and f.is_file()]
        assert len(has_data) == 0, f"{dname} contains data files: {has_data}"
