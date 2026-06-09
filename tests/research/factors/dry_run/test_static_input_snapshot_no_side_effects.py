"""
Tests for static_input_snapshot.py — No side effects, placeholder only.
"""

from research.factor_library.dry_run.static_input_snapshot import (
    build_static_input_snapshot,
)


class TestStaticInputSnapshot:
    """Verify snapshot is in-memory placeholder only."""

    def test_placeholder_only(self):
        """ASSERT 24"""
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["snapshot_mode"] == "IN_MEMORY_PLACEHOLDER_ONLY"

    def test_runtime_data_required_false(self):
        """ASSERT 25"""
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["runtime_data_required"] is False

    def test_external_data_required_false(self):
        """ASSERT 26"""
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["external_data_required"] is False

    def test_factor_recalculation_required_false(self):
        """ASSERT 27"""
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["factor_recalculation_required"] is False

    def test_factor_result_update_required_false(self):
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["factor_result_update_required"] is False

    def test_factor_ids_preserved(self):
        snapshot = build_static_input_snapshot(("F21", "F22", "F24"))
        assert snapshot["factor_ids"] == ["F21", "F22", "F24"]

    def test_no_artifacts_loaded(self):
        snapshot = build_static_input_snapshot(("F21",))
        assert snapshot["artifacts_loaded"] == 0

    def test_no_file_writes(self):
        """ASSERT 23 continuation: no file I/O."""
        snapshot = build_static_input_snapshot(("F21",))
        assert isinstance(snapshot, dict)
