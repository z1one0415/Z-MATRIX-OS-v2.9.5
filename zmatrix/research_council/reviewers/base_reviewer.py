# allowlist: forbidden-token-definition
"""V4.0-C3 Research Council — Base Reviewer + ReviewerResult dataclass"""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib, json

@dataclass
class ReviewerResult:
    """Standardized output for all 12 independent reviewers.

    Every reviewer must return this structure.
    All trade/execution flags default to False for paper-only safety.
    """
    reviewer_id: str
    facts: dict = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    deterministic_score: float = 0.0
    score_trace: dict = field(default_factory=dict)
    risk_flags: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    review_status: str = "DATA_INSUFFICIENT"
    real_trade_allowed: bool = False
    broker_order_allowed: bool = False
    production_allowed: bool = False
    human_review_required: bool = True
    paper_only: bool = True

    def to_dict(self) -> dict:
        return {
            "reviewer_id": self.reviewer_id,
            "facts": self.facts,
            "deterministic_score": self.deterministic_score,
            "score_trace": self.score_trace,
            "risk_flags": self.risk_flags,
            "missing_evidence": self.missing_evidence,
            "review_status": self.review_status,
            "real_trade_allowed": self.real_trade_allowed,
            "broker_order_allowed": self.broker_order_allowed,
            "production_allowed": self.production_allowed,
            "human_review_required": self.human_review_required,
            "paper_only": self.paper_only,
        }


class BaseReviewer:
    """Abstract reviewer with fact extraction, scoring, and evidence policy.

    Each of the 12 independent reviewers extends this.
    """
    reviewer_id: str = ""
    methodology_kernel: str = ""
    fact_schema: dict = {}
    required_evidence: list[str] = []
    allowed_enums: dict = {}
    scoring_config: dict = {}

    def __init__(self, reviewer_id: str, methodology_kernel: str):
        self.reviewer_id = reviewer_id
        self.methodology_kernel = methodology_kernel
        self.fact_schema = {}
        self.required_evidence = []
        self.allowed_enums = {}
        self.scoring_config = {}

    def extract_required_facts(self, payload: dict) -> dict:
        """Extract only the required evidence fields from payload."""
        return {k: payload.get(k) for k in self.required_evidence if k in payload}

    def deterministic_score(self, facts: dict) -> tuple[float, dict]:
        """Default scoring: +8 per fact, max 100. Override in subclasses."""
        score = min(100, len(facts) * 8)
        trace = {
            "reviewer": self.reviewer_id,
            "method": self.methodology_kernel,
            "input_facts": dict(facts),
            "calculation": f"default: len(facts)={len(facts)} * 8 = {score}",
        }
        return float(score), trace

    def review(self, payload: dict) -> ReviewerResult:
        """Full review pipeline: extract → validate → score → result."""
        facts = self.extract_required_facts(payload or {})
        missing = [f for f in self.required_evidence if f not in (payload or {})]
        if missing:
            return ReviewerResult(
                reviewer_id=self.reviewer_id,
                facts=facts,
                missing_evidence=missing,
                review_status="DATA_INSUFFICIENT",
            )
        score, trace = self.deterministic_score(facts)
        return ReviewerResult(
            reviewer_id=self.reviewer_id,
            facts=facts,
            deterministic_score=score,
            score_trace=trace,
            review_status="RESEARCH_SUPPORT",
        )
