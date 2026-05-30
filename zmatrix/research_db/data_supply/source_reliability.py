"""SourceReliabilityTracker — track success/failure and compute reliability scores per source."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SourceReliabilityTracker:
    source: str
    success_count: int = 0
    failure_count: int = 0
    total_attempts: int = 0
    last_success: str = ""
    last_failure: str = ""
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False

    def record_success(self, timestamp: str | None = None) -> None:
        self.success_count += 1
        self.total_attempts += 1
        self.last_success = timestamp or datetime.now(timezone.utc).isoformat()

    def record_failure(self, timestamp: str | None = None) -> None:
        self.failure_count += 1
        self.total_attempts += 1
        self.last_failure = timestamp or datetime.now(timezone.utc).isoformat()

    def compute_score(self) -> float:
        if self.total_attempts == 0:
            return 1.0
        return self.success_count / self.total_attempts

    @property
    def reliability(self) -> float:
        return self.compute_score()

    @property
    def is_healthy(self) -> bool:
        return self.compute_score() >= 0.8

    def reset(self) -> None:
        self.success_count = 0
        self.failure_count = 0
        self.total_attempts = 0
        self.last_success = ""
        self.last_failure = ""
