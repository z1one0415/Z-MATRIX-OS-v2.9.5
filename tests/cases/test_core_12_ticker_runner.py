"""Test the Core 12 batch runner for evidence integrity."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def _runner_text():
    return Path(WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()


def test_runner_no_dev_null():
    """Runner must not contain /dev/null."""
    t = _runner_text()
    assert "/dev/null" not in t


def test_runner_no_dev_null_redirect():
    """Runner must not contain 2>/dev/null."""
    t = _runner_text()
    assert "2>/dev/null" not in t


def test_runner_no_or_true():
    """Runner must not contain || true."""
    t = _runner_text()
    assert "|| true" not in t


def test_runner_no_nominal_only():
    """Runner must not contain CORE_12_NOMINAL_ONLY."""
    t = _runner_text()
    assert "CORE_12_NOMINAL_ONLY" not in t


def test_summary_status_ticker_specific():
    """core_12_summary.json status == CORE_12_TICKER_SPECIFIC_ATTEMPTED."""
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    assert s["status"] == "CORE_12_TICKER_SPECIFIC_ATTEMPTED"


def test_summary_attempted_12():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    assert s["attempted"] == 12


def test_summary_ticker_specific_true():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    assert s["ticker_specific"] is True


def test_summary_runner_parameterized_true():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    assert s["runner_parameterized"] is True


def test_summary_unique_hash_count_12():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_summary.json").read_text())
    assert s["unique_hash_count"] == 12


def test_audit_json_count_12():
    audits = list((WORKSPACE / "runtime_reports" / "cases" / "core_12").glob("CORE_*_*/*_audit.json"))
    assert len(audits) == 12


def test_audit_jsons_all_completed():
    import sys; sys.path.insert(0, str(WORKSPACE))
    audits = list((WORKSPACE / "runtime_reports" / "cases" / "core_12").glob("CORE_*_*/*_audit.json"))
    for p in audits:
        d = json.loads(p.read_text())
        assert d["status"] == "COMPLETED", f"{p}: status={d['status']}"
