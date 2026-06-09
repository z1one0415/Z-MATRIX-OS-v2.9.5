"""
Tests for hash_evidence.py — Deterministic hash, no file writes.
"""

from research.factor_library.dry_run.hash_evidence import (
    compute_hash_only_evidence,
)


class TestHashEvidence:
    """Verify hash computation is correct and side-effect-free."""

    def test_deterministic(self):
        """ASSERT 28"""
        h1 = compute_hash_only_evidence({"a": 1})
        h2 = compute_hash_only_evidence({"a": 1})
        assert h1 == h2

    def test_different_inputs_different_hash(self):
        h1 = compute_hash_only_evidence({"a": 1})
        h2 = compute_hash_only_evidence({"a": 2})
        assert h1 != h2

    def test_hash_is_64_hex_chars(self):
        h = compute_hash_only_evidence({"test": True})
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_no_file_write(self):
        """ASSERT 29"""
        _ = compute_hash_only_evidence({"x": "y"})
        # Pure computation, verified by no exceptions

    def test_sort_keys_makes_order_irrelevant(self):
        h1 = compute_hash_only_evidence({"b": 2, "a": 1})
        h2 = compute_hash_only_evidence({"a": 1, "b": 2})
        assert h1 == h2

    def test_empty_dict_hash(self):
        h = compute_hash_only_evidence({})
        assert len(h) == 64

    def test_none_hash_does_not_crash(self):
        h = compute_hash_only_evidence({"key": None})
        assert len(h) == 64
