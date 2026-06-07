"""
Test: Level 4 disabled-by-default behavior.

Verifies that LEVEL4_WARNING_ENABLED=false by default and produces
zero observable effects.
"""

from skillos.level4.config import load_config, Level4Config
from skillos.level4.guards import is_level4_enabled, disabled_guard
from skillos.level4.evaluator import evaluate_level4
from skillos.level4.models import Level4EvaluationInput


class TestLevel4DisabledDefault:

    def test_default_config_is_disabled(self):
        """Config created with no arguments must have warning_enabled=False."""
        config = load_config(None)
        assert config.warning_enabled is False

    def test_config_missing_key_is_disabled(self):
        """Missing key in config dict must result in disabled."""
        config = load_config({"UNRELATED_KEY": 42})
        assert config.warning_enabled is False

    def test_config_malformed_is_disabled(self):
        """Non-bool values must result in disabled."""
        config = load_config({"LEVEL4_WARNING_ENABLED": "yes"})
        assert config.warning_enabled is False

    def test_config_none_is_disabled(self):
        """None source must result in disabled."""
        config = load_config(None)
        assert config.warning_enabled is False

    def test_config_empty_dict_is_disabled(self):
        """Empty dict source must result in disabled."""
        config = load_config({})
        assert config.warning_enabled is False

    def test_config_int_one_is_disabled(self):
        """Integer value 1 (truthy but not bool True) must result in disabled."""
        config = load_config({"LEVEL4_WARNING_ENABLED": 1})
        assert config.warning_enabled is False

    def test_config_explicit_false_is_disabled(self):
        """Explicit bool False must remain disabled."""
        config = load_config({"LEVEL4_WARNING_ENABLED": False})
        assert config.warning_enabled is False

    def test_is_level4_enabled_default(self):
        """is_level4_enabled must return False by default."""
        config = load_config(None)
        assert is_level4_enabled(config) is False

    def test_disabled_guard_returns_continue(self):
        """disabled_guard must return CONTINUE action."""
        config = load_config(None)
        result = disabled_guard(config)
        assert result.action == "CONTINUE"

    def test_disabled_guard_warnings_empty(self):
        """disabled_guard must return empty warnings list."""
        config = load_config(None)
        result = disabled_guard(config)
        assert len(result.warnings) == 0

    def test_disabled_guard_disabled_true(self):
        """disabled_guard must set disabled=True."""
        config = load_config(None)
        result = disabled_guard(config)
        assert result.disabled is True

    def test_evaluate_level4_default_returns_continue(self):
        """evaluate_level4 with default config must return CONTINUE."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.action == "CONTINUE"

    def test_evaluate_level4_default_warnings_empty(self):
        """evaluate_level4 with default config must return empty warnings."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert len(result.warnings) == 0

    def test_evaluate_level4_default_disabled(self):
        """evaluate_level4 with default config must be disabled."""
        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)
        assert result.disabled is True
