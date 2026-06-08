"""Proof: evidence — Noop default, InMemory optional, hash-only, no files."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.evidence import (
    NoopWave0EvidenceSink, InMemoryWave0EvidenceSink,
    plan_enablement_evidence, get_evidence_sink, reset_evidence_sink,
)


def test_noop_default():
    sink = NoopWave0EvidenceSink()
    sink.record({"test": "data"})
    assert sink.is_empty() is True  # noop stores nothing


def test_noop_flush_noop():
    sink = NoopWave0EvidenceSink()
    sink.flush()  # should not raise
    assert sink.is_empty() is True


def test_inmemory_records_evidence():
    sink = InMemoryWave0EvidenceSink()
    sink.record({"action": "test"})
    assert sink.is_empty() is False
    assert len(sink.records) == 1


def test_inmemory_hash_only():
    """Evidence stored as hash, not raw content."""
    sink = InMemoryWave0EvidenceSink()
    sink.record({"sensitive": "data"})
    record = sink.records[0]
    assert "hash" in record  # only hash stored
    assert "sensitive" not in record  # raw data not stored


def test_inmemory_flush_clears():
    sink = InMemoryWave0EvidenceSink()
    sink.record({"a": 1})
    sink.flush()
    assert sink.is_empty() is True


def test_plan_evidence_returns_hash():
    evidence = plan_enablement_evidence({"decision": "DENY"})
    assert "hash" in evidence
    assert evidence["type"] == "enablement_decision"


def test_default_sink_is_noop():
    sink = get_evidence_sink()
    assert isinstance(sink, NoopWave0EvidenceSink)


def test_reset_evidence_sink():
    reset_evidence_sink()
    sink = get_evidence_sink()
    assert isinstance(sink, NoopWave0EvidenceSink)
