"""Batch-D: Research Verdict — thesis + evidence + unknowns."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ResearchVerdict:
    experiment_id: str; thesis: str = ""
    supporting_evidence: list = field(default_factory=list)
    contradicting_evidence: list = field(default_factory=list)
    remaining_unknowns: list = field(default_factory=list)
    final_confidence: float = 0.0
    council_status: str = "PENDING"
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class VerdictBuilder:
    @staticmethod
    def build(experiment_id: str, council_decision, consensus_result, devil_challenges: dict) -> ResearchVerdict:
        v = ResearchVerdict(experiment_id=experiment_id)
        v.council_status = council_decision.status
        v.final_confidence = consensus_result.confidence
        if council_decision.status == "PASS": v.thesis = "Experiment validated by council"
        elif council_decision.status == "FAIL": v.thesis = "Experiment rejected by council"
        else: v.thesis = "Experiment requires further evidence"
        v.contradicting_evidence = devil_challenges.get("challenges", [])
        v.remaining_unknowns = [o["concerns"] for o in council_decision.minority_opinions if o.get("concerns")]
        v.supporting_evidence = consensus_result.minority_report if not consensus_result.consensus_reached else [{"note": "Council consensus reached"}]
        return v
