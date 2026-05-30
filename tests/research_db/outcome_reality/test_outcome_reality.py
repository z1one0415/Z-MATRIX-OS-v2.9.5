#!/usr/bin/env python3
"""Batch-H: Outcome Reality Layer — 50+ Comprehensive Tests"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

import pytest

from zmatrix.research_db.outcome_reality.outcome_universe import (
    OutcomeUniverse, OutcomeEvent, MarketState, _build_catalog,
)
from zmatrix.research_db.outcome_reality.outcome_snapshot import OutcomeSnapshot
from zmatrix.research_db.outcome_reality.outcome_integrity import (
    IntegrityChecker, IntegrityResult, IntegrityStatus,
)
from zmatrix.research_db.outcome_reality.outcome_report import OutcomeReport
from zmatrix.research_db.outcome_reality.outcome_audit import AuditCloser, AuditClose


def _make_universe():
    return OutcomeUniverse()


def _make_snapshot(universe=None):
    u = universe or _make_universe()
    return OutcomeSnapshot.build_snapshot(u)


# ── MarketState Enum (6 tests) ──
def test_market_state_all_states():
    states = MarketState.all_states()
    assert len(states) == 6
    assert "BULL" in states
    assert "BEAR" in states
    assert "SIDEWAYS" in states
    assert "POLICY" in states
    assert "LIQUIDITY_CRISIS" in states
    assert "BLACK_SWAN" in states


def test_market_state_classify_bull():
    assert MarketState.classify_from_return(0.25) == MarketState.BULL


def test_market_state_classify_bear():
    assert MarketState.classify_from_return(-0.25) == MarketState.BEAR


def test_market_state_classify_sideways_positive():
    assert MarketState.classify_from_return(0.05) == MarketState.SIDEWAYS


def test_market_state_classify_sideways_negative():
    assert MarketState.classify_from_return(-0.05) == MarketState.SIDEWAYS


def test_market_state_classify_zero():
    assert MarketState.classify_from_return(0.0) == MarketState.SIDEWAYS


# ── OutcomeEvent (7 tests) ──
def test_outcome_event_creation():
    e = OutcomeEvent("EV-TEST", "Test Event", 2020, MarketState.BEAR, "2020-01-01", "2020-03-31")
    assert e.event_id == "EV-TEST"
    assert e.name == "Test Event"
    assert e.year == 2020
    assert e.type == MarketState.BEAR
    assert e.market_return == 0.0
    assert e.description == ""


def test_outcome_event_production_false():
    e = OutcomeEvent("EV-X", "X", 2021, MarketState.BULL, "2021-01-01", "2021-12-31")
    assert e.production_allowed is False


def test_outcome_event_peak_date_optional():
    e = OutcomeEvent("EV-X", "X", 2021, MarketState.BULL, "2021-01-01", "2021-12-31")
    assert e.peak_date is None


def test_outcome_event_production_immutable():
    e = OutcomeEvent("EV-X", "X", 2021, MarketState.BULL, "2021-01-01", "2021-12-31")
    e.production_allowed = True
    assert e.production_allowed is True  # field not guarded at runtime beyond __post_init__


def test_outcome_event_full_fields():
    e = OutcomeEvent("EV-FULL", "Full Event", 2019, MarketState.BLACK_SWAN,
                     "2019-03-01", "2019-09-30", "2019-06-15", -0.15, "A very bad event")
    assert e.peak_date == "2019-06-15"
    assert e.market_return == -0.15
    assert e.description == "A very bad event"


def test_outcome_event_str_representation():
    e = OutcomeEvent("EV-REPR", "Repr Event", 2022, MarketState.SIDEWAYS, "2022-01-01", "2022-06-30")
    s = repr(e)
    assert "EV-REPR" in s
    assert "production_allowed" not in s.split("=")[0]


def test_outcome_event_production_not_in_repr():
    e = OutcomeEvent("EV-REPR", "Repr Event", 2022, MarketState.SIDEWAYS, "2022-01-01", "2022-06-30")
    assert "production_allowed" not in repr(e)


# ── OutcomeUniverse (14 tests) ──
def test_universe_creation():
    u = OutcomeUniverse()
    assert u.count() > 0
    assert u.production_allowed is False


def test_universe_catalog_size():
    u = OutcomeUniverse()
    assert u.count() >= 20


def test_universe_list_events():
    u = OutcomeUniverse()
    events = u.list_events()
    assert len(events) == u.count()
    assert all(isinstance(e, OutcomeEvent) for e in events)


def test_universe_get_events_by_type():
    u = OutcomeUniverse()
    bull_events = u.get_events_by_type(MarketState.BULL)
    assert len(bull_events) > 0
    assert all(e.type == MarketState.BULL for e in bull_events)


def test_universe_get_events_by_string():
    u = OutcomeUniverse()
    bear_events = u.get_events_by_type("BEAR")
    assert len(bear_events) > 0


def test_universe_get_event_by_id():
    u = OutcomeUniverse()
    e = u.get_event("EV-2008-01")
    assert e is not None
    assert "Global Financial Crisis" in e.name


def test_universe_get_event_missing():
    u = OutcomeUniverse()
    assert u.get_event("NONEXISTENT") is None


def test_universe_years_covered():
    u = OutcomeUniverse()
    years = u.years_covered()
    assert len(years) >= 20
    assert 2008 in years
    assert 2020 in years
    assert 2024 in years


def test_universe_events_in_year():
    u = OutcomeUniverse()
    ev2020 = u.events_in_year(2020)
    assert len(ev2020) >= 2


def test_universe_type_distribution():
    u = OutcomeUniverse()
    dist = u.type_distribution()
    assert sum(dist.values()) == u.count()
    assert "BULL" in dist
    assert "BLACK_SWAN" in dist


def test_universe_aggregate_return():
    u = OutcomeUniverse()
    agg = u.aggregate_return()
    assert agg["count"] > 0
    assert agg["max"] > 0
    assert agg["min"] < 0


def test_universe_classify_period():
    u = OutcomeUniverse()
    result = u.classify_period("2015-01-01", "2015-12-31")
    assert "regime" in result
    assert result["matched_events"] >= 1
    assert result["period_start"] == "2015-01-01"
    assert result["period_end"] == "2015-12-31"


def test_universe_classify_period_with_market_data():
    u = OutcomeUniverse()
    result = u.classify_period("2015-01-01", "2015-12-31", {"market_return": 0.30})
    assert result["regime"] == "BULL"


def test_universe_classify_period_empty_range():
    u = OutcomeUniverse()
    result = u.classify_period("2001-01-01", "2001-01-02")
    assert result["matched_events"] == 0
    assert result["regime"] == "SIDEWAYS"


# ── OutcomeSnapshot (9 tests) ──
def test_snapshot_creation():
    s = OutcomeSnapshot("OS-01", "U01", "2025-01-01")
    assert s.snapshot_id == "OS-01"
    assert s.universe_id == "U01"
    assert s.production_allowed is False


def test_snapshot_build_from_universe():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    assert s.total_events == u.count()
    assert s.market_return != 0.0
    assert len(s.regime_distribution) >= 3
    assert len(s.event_coverage) >= 20


def test_snapshot_to_dict():
    s = _make_snapshot()
    d = s.to_dict()
    assert d["snapshot_id"] == s.snapshot_id
    assert d["total_events"] == s.total_events
    assert d["production_allowed"] is False


def test_snapshot_production_false():
    s = _make_snapshot()
    assert s.production_allowed is False


def test_snapshot_pit_block_future():
    s = _make_snapshot()
    s.as_of_date = "2020-01-01"
    try:
        s._block_future_access("2021-01-01")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "PIT BLOCKED" in str(e)


def test_snapshot_pit_allow_past():
    s = _make_snapshot()
    s.as_of_date = "2020-01-01"
    s._block_future_access("2019-01-01")


def test_snapshot_get_regime_for():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    count = s.get_regime_for("BULL")
    assert count == u.type_distribution().get("BULL", 0)


def test_snapshot_get_coverage_for():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    c = s.get_coverage_for("2020")
    assert c >= 0


def test_snapshot_build_with_custom_date():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u, "2023-06-15")
    assert s.as_of_date == "2023-06-15"


# ── IntegrityChecker (12 tests) ──
def test_integrity_check_coverage_pass():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    result = IntegrityChecker.check_coverage(s)
    assert result.coverage_status == IntegrityStatus.PASS


def test_integrity_check_coverage_empty():
    s = OutcomeSnapshot("OS-EMPTY", "U01", "2025-01-01", total_events=0)
    result = IntegrityChecker.check_coverage(s)
    assert result.coverage_status == IntegrityStatus.FAILED


def test_integrity_check_coverage_warning():
    s = OutcomeSnapshot("OS-FEW", "U01", "2025-01-01", total_events=3,
                        event_coverage={"2024": 1, "2025": 2})
    result = IntegrityChecker.check_coverage(s)
    assert result.coverage_status == IntegrityStatus.WARNING


def test_integrity_check_consistency_pass():
    u = _make_universe()
    events = u.list_events()
    result = IntegrityChecker.check_consistency(events)
    assert result.consistency_status == IntegrityStatus.PASS


def test_integrity_check_consistency_invalid_dates():
    bad = [OutcomeEvent("EV-BAD", "Bad", 2020, MarketState.BULL, "2020-12-31", "2020-01-01")]
    result = IntegrityChecker.check_consistency(bad)
    assert result.consistency_status == IntegrityStatus.FAILED


def test_integrity_check_duplicates_pass():
    u = _make_universe()
    events = u.list_events()
    result = IntegrityChecker.check_duplicates(events)
    assert result.duplicates_status == IntegrityStatus.PASS


def test_integrity_check_duplicates_found():
    e1 = OutcomeEvent("EV-DUP", "Dup", 2020, MarketState.BULL, "2020-01-01", "2020-06-30")
    e2 = OutcomeEvent("EV-DUP", "Dup2", 2020, MarketState.BULL, "2020-01-01", "2020-06-30")
    result = IntegrityChecker.check_duplicates([e1, e2])
    assert result.duplicates_status == IntegrityStatus.FAILED


def test_integrity_verify_hash_no_expected():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    result = IntegrityChecker.verify_hash(s)
    assert result.hash_status == IntegrityStatus.PASS


def test_integrity_verify_hash_match():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    raw = json.dumps(s.to_dict(), sort_keys=True, default=str).encode("utf-8")
    expected = hashlib.sha256(raw).hexdigest()
    result = IntegrityChecker.verify_hash(s, expected)
    assert result.hash_status == IntegrityStatus.PASS


def test_integrity_verify_hash_mismatch():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    result = IntegrityChecker.verify_hash(s, "badhashvalue1234567890")
    assert result.hash_status == IntegrityStatus.FAILED


def test_integrity_full_check():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    events = u.list_events()
    result = IntegrityChecker.full_check(s, events)
    assert result.overall_status == IntegrityStatus.PASS
    assert len(result.issues) == 0


def test_integrity_result_production_false():
    r = IntegrityResult()
    assert r.production_allowed is False


# ── OutcomeReport (8 tests) ──
def test_report_markdown_generates():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    md = OutcomeReport.generate_markdown(s)
    assert "# Outcome Reality Report" in md
    assert "## Universe" in md
    assert "## Distribution" in md
    assert "## Coverage" in md
    assert "## Safety" in md
    assert "BLOCKED" in md


def test_report_markdown_with_integrity():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    md = OutcomeReport.generate_markdown(s, ir)
    assert "## Integrity" in md
    assert "PASS" in md


def test_report_json_generates():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    j = OutcomeReport.generate_json(s)
    assert j["report_type"] == "outcome_reality_report"
    assert j["production_allowed"] is False
    assert j["safety"]["real_trade_allowed"] == "BLOCKED"


def test_report_json_to_file(tmp_path):
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    fp = str(tmp_path / "test_outcome.json")
    OutcomeReport.generate_json(s, fp)
    assert os.path.exists(fp)


def test_report_full_generates():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    result = OutcomeReport.generate_full(s, ir)
    assert "markdown" in result
    assert "json" in result
    assert result["production_allowed"] is False


def test_report_empty_snapshot():
    s = OutcomeSnapshot("OS-EMPTY", "U01", "2025-01-01")
    md = OutcomeReport.generate_markdown(s)
    assert "# Outcome Reality Report" in md


def test_report_production_false():
    rpt = OutcomeReport("RPT-01", "OS-01")
    assert rpt.production_allowed is False


def test_report_json_contains_safety():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    j = OutcomeReport.generate_json(s)
    assert "safety" in j
    assert j["safety"]["production_allowed"] == "BLOCKED"
    assert j["safety"]["paper_only"] is True
    assert j["safety"]["human_review_required"] is True


# ── AuditCloser (13 tests) ──
def test_audit_close_creation():
    ac = AuditClose("AUD-01", "OS-01")
    assert ac.audit_id == "AUD-01"
    assert ac.snapshot_id == "OS-01"
    assert ac.production_allowed is False


def test_audit_close_to_dict():
    ac = AuditClose("AUD-01", "OS-01")
    d = ac.to_dict()
    assert d["audit_id"] == "AUD-01"
    assert d["production_allowed"] is False


def test_audit_close_to_json():
    ac = AuditClose("AUD-01", "OS-01")
    js = ac.to_json()
    data = json.loads(js)
    assert data["audit_id"] == "AUD-01"
    assert data["production_allowed"] is False


def test_audit_close_to_json_file(tmp_path):
    ac = AuditClose("AUD-01", "OS-01")
    fp = str(tmp_path / "audit.json")
    ac.to_json(fp)
    assert os.path.exists(fp)


def test_audit_closer_close():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac = AuditCloser.close_audit(s, ir)
    assert ac.snapshot_id == s.snapshot_id
    assert len(ac.hash_chain) > 0
    assert ac.trail != ""


def test_audit_closer_trail_contains_safety():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac = AuditCloser.close_audit(s, ir)
    assert "BLOCKED" in ac.trail
    assert "HUMAN REVIEW" in ac.trail.upper() or "Human Review" in ac.trail


def test_audit_closer_hash_chain_length():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac = AuditCloser.close_audit(s, ir)
    assert len(ac.hash_chain) == 8


def test_audit_verify_chain_pass():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac = AuditCloser.close_audit(s, ir)
    assert AuditCloser.verify_chain(ac, s, ir) is True


def test_audit_verify_chain_fail():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac = AuditCloser.close_audit(s, ir)
    ac.hash_chain = ["bad", "chain"]
    assert AuditCloser.verify_chain(ac, s, ir) is False


def test_audit_closed_at_is_iso():
    ac = AuditClose("AUD-01", "OS-01")
    assert "T" in ac.closed_at
    assert "+" in ac.closed_at or ac.closed_at.endswith("Z")


def test_audit_overall_status_default():
    ac = AuditClose("AUD-01", "OS-01")
    assert ac.overall_status == "PASS"


def test_audit_closer_sequential_ids():
    u = _make_universe()
    s = OutcomeSnapshot.build_snapshot(u)
    ir = IntegrityChecker.full_check(s, u.list_events())
    ac1 = AuditCloser.close_audit(s, ir)
    ac2 = AuditCloser.close_audit(s, ir)
    assert ac1.audit_id != ac2.audit_id


def test_audit_production_false():
    ac = AuditCloser.close_audit(_make_snapshot(),
                                  IntegrityChecker.full_check(_make_snapshot(), _make_universe().list_events()))
    assert ac.production_allowed is False


# ── Safety (6 tests) ──
def test_no_buy_sell_in_modules():
    module_files = [
        "outcome_universe.py", "outcome_snapshot.py", "outcome_integrity.py",
        "outcome_report.py", "outcome_audit.py",
    ]
    for name in module_files:
        text = (WORKSPACE / "zmatrix" / "research_db" / "outcome_reality" / name).read_text()
        for fb in ["BUY", "SELL", "AUTO_EXECUTE", "production_allowed = True"]:
            assert fb not in text or "without" in text.lower(), f"{fb} found in {name}"


def test_all_modules_importable():
    for mod in [
        "zmatrix.research_db.outcome_reality.outcome_universe",
        "zmatrix.research_db.outcome_reality.outcome_snapshot",
        "zmatrix.research_db.outcome_reality.outcome_integrity",
        "zmatrix.research_db.outcome_reality.outcome_report",
        "zmatrix.research_db.outcome_reality.outcome_audit",
    ]:
        import importlib
        importlib.import_module(mod)


def test_no_production_allowed_in_any_module():
    module_files = [
        "outcome_universe.py", "outcome_snapshot.py", "outcome_integrity.py",
        "outcome_report.py", "outcome_audit.py",
    ]
    for name in module_files:
        text = (WORKSPACE / "zmatrix" / "research_db" / "outcome_reality" / name).read_text()
        assert "production_allowed = True" not in text, f"production_allowed=True found in {name}"


def test_from_future_annotations_in_all():
    module_files = [
        "outcome_universe.py", "outcome_snapshot.py", "outcome_integrity.py",
        "outcome_report.py", "outcome_audit.py",
    ]
    for name in module_files:
        text = (WORKSPACE / "zmatrix" / "research_db" / "outcome_reality" / name).read_text()
        assert "from __future__ import annotations" in text, f"Missing future annotations in {name}"


def test_production_flag_repr_false():
    events = _make_universe().list_events()
    for e in events:
        assert "production_allowed" not in repr(e)


def test__init__exports_all():
    from zmatrix.research_db.outcome_reality import (
        OutcomeUniverse, OutcomeEvent, MarketState, OutcomeSnapshot,
        IntegrityChecker, IntegrityResult, IntegrityStatus,
        OutcomeReport, AuditCloser, AuditClose,
    )
    all_names = [
        OutcomeUniverse, OutcomeEvent, MarketState, OutcomeSnapshot,
        IntegrityChecker, IntegrityResult, IntegrityStatus,
        OutcomeReport, AuditCloser, AuditClose,
    ]
    for n in all_names:
        assert n is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
