"""Batch-D: Base Reviewer Framework — structured review protocol."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable

class ReviewVerdict(str, Enum):
    PASS="PASS"; CONDITIONAL_PASS="CONDITIONAL_PASS"; FAIL="FAIL"; INSUFFICIENT_EVIDENCE="INSUFFICIENT_EVIDENCE"

@dataclass
class ReviewContext:
    experiment_id: str; dataset_hash: str; replay_hash: str
    metrics: dict = field(default_factory=dict); attribution: dict = field(default_factory=dict)
    factors: list = field(default_factory=list); risk_flags: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class ReviewResult:
    reviewer_id: str; reviewer_name: str; verdict: str = "INSUFFICIENT_EVIDENCE"
    score: float = 0.0; evidence: list = field(default_factory=list)
    concerns: list = field(default_factory=list); minority_note: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class BaseReviewer:
    def __init__(self, reviewer_id: str, name: str, review_fn: Callable):
        self.reviewer_id = reviewer_id; self.name = name; self._review_fn = review_fn

    def review(self, ctx: ReviewContext) -> ReviewResult:
        r = self._review_fn(ctx)
        r.reviewer_id = self.reviewer_id; r.reviewer_name = self.name
        return r

    def review_batch(self, contexts: list[ReviewContext]) -> list[ReviewResult]:
        return [self.review(ctx) for ctx in contexts]
