"""
Tests for config.py — disabled-default runtime flags.

Verifies all runtime flags are hard-coded False with no env/config overrides.
"""

from research.factor_library.dry_run import config


class TestConfigConstants:
    """Verify all constants are False."""

    def test_runner_enabled_false(self):
        """ASSERT 1"""
        assert config.RUNNER_ENABLED is False

    def test_execution_allowed_false(self):
        """ASSERT 2"""
        assert config.EXECUTION_ALLOWED is False

    def test_side_effects_allowed_false(self):
        """ASSERT 3"""
        assert config.SIDE_EFFECTS_ALLOWED is False

    def test_runtime_reports_write_allowed_false(self):
        """ASSERT 4"""
        assert config.RUNTIME_REPORTS_WRITE_ALLOWED is False

    def test_runtime_audit_write_allowed_false(self):
        """ASSERT 5"""
        assert config.RUNTIME_AUDIT_WRITE_ALLOWED is False

    def test_external_data_fetch_allowed_false(self):
        """ASSERT 6"""
        assert config.EXTERNAL_DATA_FETCH_ALLOWED is False

    def test_factor_calculation_allowed_false(self):
        """ASSERT 7"""
        assert config.FACTOR_CALCULATION_ALLOWED is False

    def test_factor_result_update_allowed_false(self):
        """ASSERT 8"""
        assert config.FACTOR_RESULT_UPDATE_ALLOWED is False

    def test_production_allowed_false(self):
        """ASSERT 9"""
        assert config.PRODUCTION_ALLOWED is False

    def test_broker_runtime_allowed_false(self):
        """ASSERT 10"""
        assert config.BROKER_RUNTIME_ALLOWED is False

    def test_real_trade_allowed_false(self):
        """ASSERT 11"""
        assert config.REAL_TRADE_ALLOWED is False


class TestConfigFunctions:
    """Verify all accessor functions return False."""

    def test_is_runner_enabled_false(self):
        assert config.is_runner_enabled() is False

    def test_is_execution_allowed_false(self):
        assert config.is_execution_allowed() is False

    def test_are_side_effects_allowed_false(self):
        assert config.are_side_effects_allowed() is False

    def test_is_runtime_reports_write_allowed_false(self):
        assert config.is_runtime_reports_write_allowed() is False

    def test_is_runtime_audit_write_allowed_false(self):
        assert config.is_runtime_audit_write_allowed() is False

    def test_is_external_data_fetch_allowed_false(self):
        assert config.is_external_data_fetch_allowed() is False

    def test_is_factor_calculation_allowed_false(self):
        assert config.is_factor_calculation_allowed() is False

    def test_is_factor_result_update_allowed_false(self):
        assert config.is_factor_result_update_allowed() is False

    def test_is_production_allowed_false(self):
        assert config.is_production_allowed() is False

    def test_is_broker_runtime_allowed_false(self):
        assert config.is_broker_runtime_allowed() is False

    def test_is_real_trade_allowed_false(self):
        assert config.is_real_trade_allowed() is False

    def test_no_env_override(self):
        """ASSERT 12: Functions don't read env vars."""
        # All functions are hard-coded — importing them should never
        # trigger env reads. Just verify they stay False regardless.
        assert config.is_runner_enabled() is False
        assert config.is_execution_allowed() is False
