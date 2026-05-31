"""Test V2 closeout safety constraints."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_v2_closeout_exists():
    """case_expansion_v2_closeout.json must exist."""
    p = WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json"
    assert p.exists(), f"Missing: {p}"


def test_v2_closeout_status():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["status"] == "CASE_EXPANSION_V2_PARAMETERIZED_CONFIRMED"


def test_v2_buy_sell_zero():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["buy_sell_instruction_count"] == 0


def test_v2_production_blocked():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["production"] == "BLOCKED"


def test_v2_broker_runtime_blocked():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["broker_runtime"] == "BLOCKED"


def test_v2_real_trade_blocked():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["real_trade"] == "BLOCKED"


def test_v2_sub_stages_all_true():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["ce2_a_golden_path_parameterized"] is True
    assert c["ce2_b_human_report_parameterized"] is True
    assert c["ce2_c_core_12_attempted"] is True


def test_v2_unique_hash_count_12():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["unique_hash_count"] == 12


def test_v2_runner_parameterized():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["runner_parameterized"] is True


def test_v2_independent_outputs():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v2_closeout.json").read_text())
    assert c["independent_outputs"] is True
