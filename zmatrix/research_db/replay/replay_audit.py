"""Batch-C: Replay Audit — cryptographic hash chain for reproducibility."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field

@dataclass
class AuditTrail:
    experiment_id: str; input_hash: str; output_hash: str; replay_hash: str
    reproducible: bool = True
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

def compute_replay_hash(*args) -> str:
    """Compute deterministic hash from any number of inputs."""
    h = hashlib.sha256()
    for a in args: h.update(json.dumps(a, sort_keys=True, default=str).encode())
    return h.hexdigest()[:16]

class ReplayAudit:
    @staticmethod
    def audit(experiment_id: str, inputs: dict, outputs: dict, previous_hash: str = "") -> AuditTrail:
        ih = compute_replay_hash(inputs); oh = compute_replay_hash(outputs)
        rh = compute_replay_hash(ih, oh, previous_hash)
        return AuditTrail(experiment_id=experiment_id, input_hash=ih, output_hash=oh, replay_hash=rh)

    @staticmethod
    def verify_reproducibility(audit_a: AuditTrail, audit_b: AuditTrail) -> bool:
        return audit_a.replay_hash == audit_b.replay_hash

    @staticmethod
    def chain_verify(audits: list[AuditTrail]) -> bool:
        for i in range(1, len(audits)):
            if not ReplayAudit.verify_reproducibility(audits[i-1], audits[i]):
                return False
        return True
