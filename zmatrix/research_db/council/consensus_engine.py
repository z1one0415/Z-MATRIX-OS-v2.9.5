"""Batch-D: Consensus Engine — agreement + minority report preservation."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ConsensusResult:
    experiment_id: str; agree_count: int = 0; disagree_count: int = 0
    confidence: float = 0.0; minority_report: list = field(default_factory=list)
    consensus_reached: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ConsensusEngine:
    @staticmethod
    def compute(results: list, experiment_id: str = "") -> ConsensusResult:
        r = ConsensusResult(experiment_id=experiment_id)
        verdicts = [res.verdict for res in results]
        r.agree_count = sum(1 for v in verdicts if v in ("PASS","CONDITIONAL_PASS"))
        r.disagree_count = len(results) - r.agree_count
        r.confidence = r.agree_count / len(results) if results else 0
        r.consensus_reached = r.confidence >= 0.67
        r.minority_report = [{"reviewer": res.reviewer_name, "verdict": res.verdict, "concerns": res.concerns} for res in results if res.verdict == "FAIL" or res.concerns]
        return r
