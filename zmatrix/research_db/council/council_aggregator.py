"""Batch-D: Council Aggregator — structured multi-reviewer decision."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CouncilDecision:
    experiment_id: str; status: str = "INSUFFICIENT_EVIDENCE"
    pass_count: int = 0; conditional_count: int = 0; fail_count: int = 0
    total_reviewers: int = 0; avg_score: float = 0.0
    minority_opinions: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class CouncilAggregator:
    @staticmethod
    def aggregate(experiment_id: str, results: list, pass_threshold: float = 0.5) -> CouncilDecision:
        decision = CouncilDecision(experiment_id=experiment_id, total_reviewers=len(results))
        scores = []
        for r in results:
            scores.append(r.score)
            if r.verdict == "PASS": decision.pass_count += 1
            elif r.verdict == "CONDITIONAL_PASS": decision.conditional_count += 1
            else: decision.fail_count += 1; decision.minority_opinions.append({"reviewer": r.reviewer_name, "concerns": r.concerns})
        decision.avg_score = sum(scores) / len(scores) if scores else 0.0
        if not results: decision.status = "INSUFFICIENT_EVIDENCE"
        else: decision.status = "PASS" if (decision.pass_count + decision.conditional_count) / len(results) >= pass_threshold else "FAIL"
        return decision

    @staticmethod
    def batch_aggregate(experiments: list[dict]) -> list[CouncilDecision]:
        return [CouncilAggregator.aggregate(e["experiment_id"], e["results"]) for e in experiments]
