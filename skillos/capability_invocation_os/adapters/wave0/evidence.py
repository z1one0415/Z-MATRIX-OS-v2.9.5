"""Wave0 Evidence — Noop default, InMemory optional, no file/network writes.

- Hash-only proof
- No file writes
- No stdout/stderr
- No runtime_audit/runtime_reports/data artifacts
- Noop remains default
- InMemory only if explicitly instantiated
"""

from dataclasses import dataclass, field
from typing import List, Optional
import hashlib
import json


class NoopWave0EvidenceSink:
    """Default: records nothing, writes nothing."""
    def record(self, evidence) -> None:
        pass

    def flush(self) -> None:
        pass

    def is_empty(self) -> bool:
        return True


@dataclass
class InMemoryWave0EvidenceSink:
    """In-memory only. No file/network writes. Hash-only proof."""
    records: List[dict] = field(default_factory=list)
    _max_records: int = 1000

    def record(self, evidence) -> None:
        if len(self.records) >= self._max_records:
            self.records = self.records[-self._max_records + 1:]
        self.records.append(self._serialize(evidence))

    def flush(self) -> None:
        self.records.clear()

    def is_empty(self) -> bool:
        return len(self.records) == 0

    def _serialize(self, evidence) -> dict:
        """Serialize evidence with hash-only proof."""
        if hasattr(evidence, '__dict__'):
            raw = {k: str(v) for k, v in evidence.__dict__.items()}
        elif isinstance(evidence, dict):
            raw = {k: str(v) for k, v in evidence.items()}
        else:
            raw = {"raw": str(evidence)}
        content_hash = hashlib.sha256(
            json.dumps(raw, sort_keys=True).encode()
        ).hexdigest()
        return {"hash": content_hash, "count": len(self.records) + 1}


def plan_enablement_evidence(decision) -> dict:
    """Produce hash-only evidence of an enablement decision.
    No file writes. No stdout/stderr. No runtime artifacts."""
    if hasattr(decision, '__dict__'):
        content = str(decision.__dict__)
    else:
        content = str(decision)
    return {
        "hash": hashlib.sha256(content.encode()).hexdigest(),
        "type": "enablement_decision",
    }


# Module-level default: Noop (no side effects)
_default_sink = NoopWave0EvidenceSink()


def get_evidence_sink():
    return _default_sink


def reset_evidence_sink():
    global _default_sink
    _default_sink = NoopWave0EvidenceSink()


def plan_controlled_readonly_evidence(decision) -> dict:
    import hashlib
    return {"hash": hashlib.sha256(str(decision).encode()).hexdigest(), "type": "controlled_readonly"}
