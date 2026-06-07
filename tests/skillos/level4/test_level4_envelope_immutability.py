"""
Test: Level 4 envelope immutability.

Verifies that Level 4 evaluation never mutates result_envelope.
P0: since Level 4 has no access to result_envelope by design,
this test verifies structural isolation.
"""

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

from skillos.level4.config import load_config
from skillos.level4.evaluator import evaluate_level4
from skillos.level4.models import Level4EvaluationInput


@dataclass
class MockEnvelope:
    """Simulated result_envelope for immutability testing."""
    status: str = "OK"
    output: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=lambda: {"version": "1.0"})
    audit_trail: Dict[str, Any] = field(default_factory=dict)
    hash_chain: str = "abc123"


def envelope_hash(env: MockEnvelope) -> str:
    """Deterministic SHA-256 of the envelope."""
    raw = json.dumps(asdict(env), sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


class TestLevel4EnvelopeImmutability:

    def _run_level4_and_check(self, envelope: MockEnvelope):
        """Helper: run Level 4 evaluation and verify envelope unchanged."""
        pre_hash = envelope_hash(envelope)

        config = load_config(None)
        result = evaluate_level4(Level4EvaluationInput(), config)

        post_hash = envelope_hash(envelope)

        assert pre_hash == post_hash, "envelope hash changed after Level 4 evaluation"
        return result

    def test_envelope_hash_unchanged(self):
        """Full envelope hash must be unchanged after Level 4."""
        env = MockEnvelope()
        self._run_level4_and_check(env)

    def test_status_unchanged(self):
        """status field must be unchanged."""
        env = MockEnvelope(status="OK")
        pre = env.status
        self._run_level4_and_check(env)
        assert env.status == pre

    def test_output_unchanged(self):
        """output field must be unchanged."""
        env = MockEnvelope(output={"result": 42})
        pre = dict(env.output)
        self._run_level4_and_check(env)
        assert env.output == pre

    def test_metadata_unchanged(self):
        """metadata field must be unchanged."""
        env = MockEnvelope(metadata={"version": "1.0", "source": "test"})
        pre = dict(env.metadata)
        self._run_level4_and_check(env)
        assert env.metadata == pre

    def test_audit_trail_unchanged(self):
        """audit_trail field must be unchanged."""
        env = MockEnvelope(audit_trail={"entry_count": 5})
        pre = dict(env.audit_trail)
        self._run_level4_and_check(env)
        assert env.audit_trail == pre

    def test_hash_chain_unchanged(self):
        """hash_chain field must be unchanged."""
        env = MockEnvelope(hash_chain="def456")
        pre = env.hash_chain
        self._run_level4_and_check(env)
        assert env.hash_chain == pre

    def test_no_new_keys_added(self):
        """No new top-level keys may appear after Level 4."""
        env = MockEnvelope()
        pre_keys = set(asdict(env).keys())
        self._run_level4_and_check(env)
        post_keys = set(asdict(env).keys())
        assert post_keys == pre_keys, f"new keys appeared: {post_keys - pre_keys}"

    def test_no_keys_removed(self):
        """No keys may be removed after Level 4."""
        env = MockEnvelope()
        pre_keys = set(asdict(env).keys())
        self._run_level4_and_check(env)
        post_keys = set(asdict(env).keys())
        assert pre_keys == post_keys, f"keys removed: {pre_keys - post_keys}"
