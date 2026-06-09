"""
Tests for rollback.py — No cleanup required.
"""

from research.factor_library.dry_run.rollback import rollback_plan


class TestRollback:
    """Verify rollback plan reports no cleanup required."""

    def test_cleanup_required_false(self):
        """ASSERT 35"""
        plan = rollback_plan()
        assert plan["cleanup_required"] is False

    def test_runtime_report_cleanup_false(self):
        """ASSERT 36"""
        plan = rollback_plan()
        assert plan["runtime_report_cleanup_required"] is False

    def test_runtime_audit_cleanup_false(self):
        plan = rollback_plan()
        assert plan["runtime_audit_cleanup_required"] is False

    def test_factor_result_cleanup_false(self):
        """ASSERT 37"""
        plan = rollback_plan()
        assert plan["factor_result_cleanup_required"] is False

    def test_reason_no_execution(self):
        plan = rollback_plan()
        assert plan["reason"] == "no execution occurred"

    def test_all_keys_present(self):
        plan = rollback_plan()
        assert "cleanup_required" in plan
        assert "runtime_report_cleanup_required" in plan
        assert "runtime_audit_cleanup_required" in plan
        assert "factor_result_cleanup_required" in plan
        assert "reason" in plan
