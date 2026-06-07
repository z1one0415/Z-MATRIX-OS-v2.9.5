"""
Test: Level 4 no-blocking behavior.

Verifies that all failure scenarios return CONTINUE without exceptions.
No blocking. No fail-closed. No caller-visible exceptions.
"""

import pytest

from skillos.level4.config import load_config, Level4Config
from skillos.level4.evaluator import evaluate_level4
from skillos.level4.guards import is_level4_enabled
from skillos.level4.models import Level4EvaluationInput, Level4EvaluationResult


class TestLevel4NoBlocking:

    def test_config_missing_returns_continue(self):
        """None config source must return CONTINUE."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action == "CONTINUE"

    def test_config_unreadable_returns_continue(self):
        """Non-dict source must return CONTINUE (simulates unreadable config)."""
        config = load_config("not_a_dict")  # type: ignore
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action == "CONTINUE"

    def test_config_malformed_returns_continue(self):
        """Malformed config (list instead of dict) must return CONTINUE."""
        config = load_config(["invalid"])  # type: ignore
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action == "CONTINUE"

    def test_unknown_category_returns_continue(self):
        """Unknown/none category input must return CONTINUE."""
        config = load_config(None)
        inp = Level4EvaluationInput(category=None)
        result = evaluate_level4(inp, config)
        assert result.action == "CONTINUE"

    def test_malformed_evidence_returns_continue(self):
        """Malformed evidence ref must return CONTINUE."""
        config = load_config(None)
        inp = Level4EvaluationInput(evidence_ref="")
        result = evaluate_level4(inp, config)
        assert result.action == "CONTINUE"

    def test_severity_mapping_error_returns_continue(self):
        """Invalid severity confidence must return CONTINUE."""
        config = load_config(None)
        inp = Level4EvaluationInput(severity_confidence=-1.0)
        result = evaluate_level4(inp, config)
        assert result.action == "CONTINUE"

    def test_multiple_scenarios_all_return_continue(self):
        """All failure scenarios must return CONTINUE, not raise."""
        scenarios = [
            load_config(None),
            load_config("bad"),  # type: ignore
            load_config([]),  # type: ignore
            load_config(42),  # type: ignore
            load_config({"LEVEL4_WARNING_ENABLED": "maybe"}),
        ]
        for config in scenarios:
            result = evaluate_level4(Level4EvaluationInput(), config)
            assert result.action == "CONTINUE", f"failed for config={config!r}"

    def test_no_caller_visible_exception(self):
        """None of the failure scenarios should raise."""
        for source in [None, "bad", [], 42, {"x": 1}]:
            try:
                config = load_config(source)  # type: ignore
                evaluate_level4(Level4EvaluationInput(), config)
            except Exception as e:
                pytest.fail(f"Unexpected exception for source={source!r}: {e}")

    def test_config_parse_failure_not_blocking(self):
        """Config parse failure in guards must return False, not raise."""
        config = load_config(None)
        try:
            enabled = is_level4_enabled(config)
            assert enabled is False
        except Exception as e:
            pytest.fail(f"Unexpected exception in guard: {e}")

    def test_action_never_blocked(self):
        """action field must never be BLOCKED."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action != "BLOCKED"

    def test_action_never_fail_closed(self):
        """action field must never be FAIL_CLOSED."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action != "FAIL_CLOSED"
