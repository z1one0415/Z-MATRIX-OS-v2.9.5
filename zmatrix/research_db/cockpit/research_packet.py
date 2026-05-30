"""Batch-E: Research Packet — final consolidated research output."""
from __future__ import annotations
from dataclasses import dataclass, field
import json, hashlib

@dataclass
class ResearchPacket:
    packet_id: str; session_id: str; ticker: str
    thesis: str = ""; factor_summary: dict = field(default_factory=dict)
    attribution_summary: dict = field(default_factory=dict)
    replay_summary: dict = field(default_factory=dict)
    council_summary: dict = field(default_factory=dict)
    verdict: str = "PENDING"; risks: list = field(default_factory=list)
    audit_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchPacketBuilder:
    @staticmethod
    def build(packet_id: str, session_id: str, ticker: str, output) -> ResearchPacket:
        p = ResearchPacket(packet_id=packet_id, session_id=session_id, ticker=ticker)
        p.thesis = f"Research on {ticker}"; p.factor_summary = output.factor_result
        p.attribution_summary = output.attribution_result; p.replay_summary = output.replay_result
        p.council_summary = {"verdict": output.council_verdict}
        p.verdict = output.council_verdict; p.risks = output.risks
        p.audit_hash = hashlib.sha256(json.dumps({"sid":session_id,"v":p.verdict},sort_keys=True).encode()).hexdigest()[:16]
        return p

    @staticmethod
    def to_json(packet: ResearchPacket) -> str:
        return json.dumps({"packet_id":packet.packet_id,"session_id":packet.session_id,"ticker":packet.ticker,
            "thesis":packet.thesis,"factor_summary":packet.factor_summary,
            "attribution_summary":packet.attribution_summary,"replay_summary":packet.replay_summary,
            "council_summary":packet.council_summary,"verdict":packet.verdict,
            "risks":packet.risks,"audit_hash":packet.audit_hash}, indent=2)

    @staticmethod
    def batch_build(sessions: list, outputs: list) -> list[ResearchPacket]:
        return [ResearchPacketBuilder.build(f"PKT-{s.session_id}", s.session_id, s.ticker, o) for s,o in zip(sessions, outputs)]
