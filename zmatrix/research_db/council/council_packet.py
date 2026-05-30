"""Batch-D: Council Packet — complete experiment evidence bundle."""
from __future__ import annotations
from dataclasses import dataclass, field
import json

@dataclass
class CouncilPacket:
    packet_id: str; experiment_id: str; replay_hash: str = ""
    attribution_summary: dict = field(default_factory=dict)
    factor_summary: dict = field(default_factory=dict)
    reviewer_results: list = field(default_factory=list)
    council_decision: dict = field(default_factory=dict)
    consensus: dict = field(default_factory=dict)
    devil_opinion: str = ""; verdict: dict = field(default_factory=dict)
    audit_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class CouncilPacketBuilder:
    @staticmethod
    def build(packet_id: str, experiment_id: str, replay_hash: str, attribution: dict, factors: dict,
              reviewer_results: list, council, consensus, devil: str, verdict) -> CouncilPacket:
        import hashlib
        p = CouncilPacket(packet_id=packet_id, experiment_id=experiment_id, replay_hash=replay_hash,
                          attribution_summary=attribution, factor_summary=factors,
                          reviewer_results=[{"id":r.reviewer_id,"verdict":r.verdict,"score":r.score} for r in reviewer_results],
                          council_decision={"status":council.status,"pass":council.pass_count,"avg":council.avg_score},
                          consensus={"agreement":consensus.agree_count,"confidence":consensus.confidence},
                          devil_opinion=devil, verdict={"status":verdict.council_status,"confidence":verdict.final_confidence})
        p.audit_hash = hashlib.sha256(json.dumps(p.council_decision,sort_keys=True).encode()).hexdigest()[:16]
        return p

    @staticmethod
    def batch_build(experiments: list[dict]) -> list[CouncilPacket]:
        return [CouncilPacketBuilder.build(**e) for e in experiments]
