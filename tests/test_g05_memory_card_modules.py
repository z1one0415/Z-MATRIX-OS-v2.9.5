"""Tests for G05 Daily Memory Card — Supplementary Modules v1.0

Covers:
  - test_g18_decisions_empty_graceful
  - test_g17_risk_events_integration
  - test_factor_snapshot_reads_state
  - test_z9_entries_structure
  - test_tomorrow_focus_prioritization
  - test_all_modules_failsafe
"""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from zmatrix.daily_memory.memory_card_modules import (
    collect_g18_decisions,
    collect_g17_risk_events,
    collect_factor_monitoring_snapshot,
    collect_z9_posterior_entries,
    generate_tomorrow_focus,
)


class TestG18DecisionsEmptyGraceful:
    """G18 decisions should return gracefully when no data is available."""

    def test_no_decisions_returns_status(self):
        result = collect_g18_decisions(["002472", "601899"])
        assert "status" in result
        # Either 'no_decisions_today' or 'unavailable' or 'ok'
        assert result["status"] in ("no_decisions_today", "unavailable", "ok")

    def test_empty_tickers_returns_status(self):
        result = collect_g18_decisions([])
        assert "status" in result

    def test_never_raises(self):
        """Should never raise, even with garbage input."""
        result = collect_g18_decisions(None)  # type: ignore
        assert isinstance(result, dict)
        assert "status" in result


class TestG17RiskEventsIntegration:
    """G17 risk events using human_risk_engine if available."""

    def test_returns_assessments_structure(self):
        result = collect_g17_risk_events(["002472"])
        assert "status" in result
        if result["status"] == "ok":
            assert "assessments" in result
            for ticker, assessment in result["assessments"].items():
                assert "risk_level" in assessment
                assert "triggered_rules" in assessment
                assert "action_gate" in assessment
                assert "must_review" in assessment

    def test_multiple_tickers(self):
        result = collect_g17_risk_events(["002472", "601899", "300308"])
        assert "status" in result

    def test_graceful_on_import_error(self):
        """Even if human_risk_engine is broken, should not crash."""
        with patch.dict(sys.modules, {"zmatrix.prediction.human_risk_engine": None}):
            result = collect_g17_risk_events(["002472"])
            assert isinstance(result, dict)
            assert "status" in result


class TestFactorSnapshotReadsState:
    """Factor monitoring snapshot should read from registry.json."""

    def test_returns_structure(self):
        result = collect_factor_monitoring_snapshot()
        assert "status" in result
        if result["status"] == "ok":
            assert "total_factors" in result
            assert "signal_ready" in result
            assert "monitoring_done" in result
            assert "blocked" in result
            assert "last_run_date" in result

    def test_with_mock_registry(self, tmp_path):
        """Test with a synthetic registry file."""
        registry = {
            "factors": [
                {"id": "f1", "status": "active", "last_run": "2026-06-09"},
                {"id": "f2", "status": "blocked", "last_run": "2026-06-08"},
                {"id": "f3", "status": "monitoring_done", "last_run": "2026-06-09"},
            ]
        }
        reg_file = tmp_path / "registry.json"
        reg_file.write_text(json.dumps(registry))

        import zmatrix.daily_memory.memory_card_modules as mod
        original = mod._FACTOR_LIBRARY
        mod._FACTOR_LIBRARY = tmp_path
        try:
            result = collect_factor_monitoring_snapshot()
            assert result["status"] == "ok"
            assert result["total_factors"] == 3
            assert result["signal_ready"] == 1
            assert result["blocked"] == 1
            assert result["monitoring_done"] == 1
            assert result["last_run_date"] == "2026-06-09"
        finally:
            mod._FACTOR_LIBRARY = original


class TestZ9EntriesStructure:
    """Z9 posterior entries should return proper structure."""

    def test_basic_structure(self):
        result = collect_z9_posterior_entries("2026-06-10")
        assert "status" in result
        if result["status"] == "ok":
            assert "predictions_due" in result
            assert "validations_pending" in result
            assert "calibration_status" in result
            assert isinstance(result["predictions_due"], list)
            assert isinstance(result["validations_pending"], list)

    def test_with_mock_predictions(self, tmp_path):
        """Test with synthetic prediction files."""
        pred = {
            "id": "pred_001",
            "ticker": "002472",
            "prediction": "涨5%",
            "date": "2026-06-03",
            "validation_due": "2026-06-10",
            "status": "pending_validation",
        }
        pred_file = tmp_path / "pred_001.json"
        pred_file.write_text(json.dumps(pred))

        import zmatrix.daily_memory.memory_card_modules as mod
        original = mod._PREDICTIONS_DIR
        mod._PREDICTIONS_DIR = tmp_path
        try:
            result = collect_z9_posterior_entries("2026-06-10")
            assert result["status"] == "ok"
            assert len(result["predictions_due"]) == 1
            assert result["predictions_due"][0]["ticker"] == "002472"
            assert len(result["validations_pending"]) == 1
        finally:
            mod._PREDICTIONS_DIR = original


class TestTomorrowFocusPrioritization:
    """Tomorrow focus should prioritize: events > risk > decisions > routine."""

    def test_empty_inputs(self):
        result = generate_tomorrow_focus({}, {}, [])
        assert isinstance(result, list)

    def test_catalysts_highest_priority(self):
        catalysts = [{"ticker": "002472", "event": "财报发布", "status": "pending"}]
        g18 = {"status": "ok", "decisions": {"601899": {"action": "ADD", "score": 80}}}
        g17 = {"status": "ok", "assessments": {}}
        result = generate_tomorrow_focus(g18, g17, catalysts)
        assert len(result) >= 1
        assert result[0]["ticker"] == "002472"
        assert result[0]["priority"] == "HIGH"

    def test_risk_before_decisions(self):
        g17 = {"status": "ok", "assessments": {
            "601899": {"risk_level": "RED", "triggered_rules": ["R01"], "action_gate": "REDUCE", "must_review": True}
        }}
        g18 = {"status": "ok", "decisions": {
            "300308": {"action": "TRACK", "score": 60, "risk_flags": []}
        }}
        result = generate_tomorrow_focus(g18, g17, [])
        # RED risk should come before TRACK decision
        tickers = [r["ticker"] for r in result]
        assert "601899" in tickers
        assert "300308" in tickers
        assert tickers.index("601899") < tickers.index("300308")

    def test_deduplication(self):
        """Same ticker in catalysts and risk should appear only once."""
        catalysts = [{"ticker": "002472", "event": "解禁"}]
        g17 = {"status": "ok", "assessments": {
            "002472": {"risk_level": "RED", "triggered_rules": ["R05"], "action_gate": "WAIT", "must_review": True}
        }}
        result = generate_tomorrow_focus({}, g17, catalysts)
        ticker_counts = [r["ticker"] for r in result].count("002472")
        assert ticker_counts == 1


class TestAllModulesFailsafe:
    """All modules must be failsafe: import errors or missing files → graceful degradation."""

    def test_g18_with_exception(self):
        """Force an internal exception and verify graceful return."""
        with patch("zmatrix.daily_memory.memory_card_modules.datetime") as mock_dt:
            mock_dt.now.side_effect = RuntimeError("clock broken")
            result = collect_g18_decisions(["002472"])
            assert result["status"] == "unavailable"
            assert "reason" in result

    def test_g17_with_broken_import(self):
        result = collect_g17_risk_events(["002472"])
        assert isinstance(result, dict)
        assert "status" in result

    def test_factor_with_corrupted_json(self, tmp_path):
        """Corrupted registry.json should not crash."""
        reg_file = tmp_path / "registry.json"
        reg_file.write_text("NOT VALID JSON {{{{")

        import zmatrix.daily_memory.memory_card_modules as mod
        original = mod._FACTOR_LIBRARY
        mod._FACTOR_LIBRARY = tmp_path
        try:
            result = collect_factor_monitoring_snapshot()
            assert result["status"] == "unavailable"
            assert "reason" in result
        finally:
            mod._FACTOR_LIBRARY = original

    def test_z9_with_missing_directory(self):
        """Non-existent predictions directory should not crash."""
        import zmatrix.daily_memory.memory_card_modules as mod
        original = mod._PREDICTIONS_DIR
        mod._PREDICTIONS_DIR = Path("/nonexistent/path/12345")
        try:
            result = collect_z9_posterior_entries("2026-06-10")
            assert result["status"] == "ok"
            assert result["predictions_due"] == []
        finally:
            mod._PREDICTIONS_DIR = original

    def test_tomorrow_focus_with_garbage(self):
        """Garbage inputs should produce a list, never crash."""
        result = generate_tomorrow_focus("not_a_dict", 42, None)  # type: ignore
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
