"""
Test: Level 4 disabled-by-default behavior.

Verifies that LEVEL4_WARNING_ENABLED=false by default and produces
zero observable effects.
"""

from skillos.level4.config import load_config, Level4Config
from skillos.level4.guards import is_level4_enabled, disabled_guard, should_emit_warning
from skillos.level4.evaluator import evaluate_level4
from skillos.level4.models import Level4EvaluationInput


class TestLevel4DisabledDefault:

    # ── config layer: load_config defaults ──

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

    # ── guard layer: is_level4_enabled with non-bool truthy values ──

    def test_is_level4_enabled_default(self):
        """is_level4_enabled must return False by default."""
        config = load_config(None)
        assert is_level4_enabled(config) is False

    def test_is_level4_enabled_int_one(self):
        """is_level4_enabled with warning_enabled=1 must return False."""
        cfg = Level4Config(warning_enabled=1)  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_string_true(self):
        """is_level4_enabled with warning_enabled='true' must return False."""
        cfg = Level4Config(warning_enabled="true")  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_string_yes(self):
        """is_level4_enabled with warning_enabled='yes' must return False."""
        cfg = Level4Config(warning_enabled="yes")  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_list(self):
        """is_level4_enabled with warning_enabled=[True] must return False."""
        cfg = Level4Config(warning_enabled=[True])  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_dict(self):
        """is_level4_enabled with warning_enabled={'enabled': True} must return False."""
        cfg = Level4Config(warning_enabled={"enabled": True})  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_object(self):
        """is_level4_enabled with warning_enabled=object() must return False."""
        cfg = Level4Config(warning_enabled=object())  # type: ignore
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_missing_attr(self):
        """is_level4_enabled with config missing warning_enabled attr must return False."""
        from collections import namedtuple
        BadConfig = namedtuple("BadConfig", [])
        cfg = BadConfig()
        assert is_level4_enabled(cfg) is False

    def test_is_level4_enabled_none_config(self):
        """is_level4_enabled with None config must return False."""
        assert is_level4_enabled(None) is False  # type: ignore

    # ── guard layer: should_emit_warning with non-bool subcontrols ──

    def test_should_emit_with_exact_bool_true(self):
        """should_emit_warning with all three exactly True may return True."""
        cfg = Level4Config(warning_enabled=True, audit_file_enabled=True, operator_report_enabled=True)
        assert should_emit_warning(cfg) is True

    def test_should_emit_with_non_bool_audit(self):
        """should_emit_warning with audit_file_enabled=1 must return False."""
        cfg = Level4Config(warning_enabled=True, audit_file_enabled=1, operator_report_enabled=True)  # type: ignore
        assert should_emit_warning(cfg) is False

    def test_should_emit_with_non_bool_operator(self):
        """should_emit_warning with operator_report_enabled='true' must return False."""
        cfg = Level4Config(warning_enabled=True, audit_file_enabled=True, operator_report_enabled="true")  # type: ignore
        assert should_emit_warning(cfg) is False

    def test_should_emit_with_none_config(self):
        """should_emit_warning with None config must return False."""
        assert should_emit_warning(None) is False  # type: ignore

    def test_should_emit_with_missing_attrs(self):
        """should_emit_warning with missing attrs must return False."""
        from collections import namedtuple
        BadConfig = namedtuple("BadConfig", ["warning_enabled"])
        cfg = BadConfig(warning_enabled=True)
        assert should_emit_warning(cfg) is False

    # ── evaluator with P0 enabled path (must still be disabled placeholder) ──

    def test_evaluate_level4_with_non_bool_config_returns_continue(self):
        """evaluate_level4 with non-bool truthy values must still return CONTINUE."""
        for val in [1, "true", "yes", [True], {"x": True}, object()]:
            cfg = Level4Config(warning_enabled=val)  # type: ignore
            result = evaluate_level4(Level4EvaluationInput(), cfg)
            assert result.action == "CONTINUE", f"failed for value {val!r}"
            assert len(result.warnings) == 0, f"failed for value {val!r}"
            assert result.disabled is True, f"failed for value {val!r}"

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
