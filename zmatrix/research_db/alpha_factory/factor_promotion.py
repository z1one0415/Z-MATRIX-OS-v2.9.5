"""Phase 4-F4: Factor Promotion — Candidate→Validated→Research→Approved→ProductionCandidate."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone

class PromotionLevel(str, Enum):
    CANDIDATE="CANDIDATE"; VALIDATED="VALIDATED"; RESEARCH="RESEARCH"
    APPROVED="APPROVED"; PRODUCTION_CANDIDATE="PRODUCTION_CANDIDATE"

@dataclass
class PromotionRecord:
    factor_id: str; from_level: str; to_level: str
    promoted_at: str; evidence: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorPromotion:
    PROMOTION_PATH = {
        PromotionLevel.CANDIDATE: PromotionLevel.VALIDATED,
        PromotionLevel.VALIDATED: PromotionLevel.RESEARCH,
        PromotionLevel.RESEARCH: PromotionLevel.APPROVED,
        PromotionLevel.APPROVED: PromotionLevel.PRODUCTION_CANDIDATE,
    }

    def __init__(self): self._history: list[PromotionRecord] = []

    def promote(self, factor_id: str, current_level: str, evidence: list) -> PromotionRecord | None:
        if current_level not in [l.value for l in PromotionLevel]: return None
        cl = PromotionLevel(current_level)
        if cl not in self.PROMOTION_PATH: return None
        next_level = self.PROMOTION_PATH[cl]
        r = PromotionRecord(factor_id=factor_id, from_level=current_level, to_level=next_level.value,
                           promoted_at=datetime.now(timezone.utc).isoformat(), evidence=evidence)
        self._history.append(r); return r

    def get_history(self, factor_id: str) -> list[PromotionRecord]:
        return [r for r in self._history if r.factor_id == factor_id]

    def current_level(self, factor_id: str) -> str:
        hist = self.get_history(factor_id)
        return hist[-1].to_level if hist else PromotionLevel.CANDIDATE.value

    @staticmethod
    def is_production_candidate(level: str) -> bool:
        return level == PromotionLevel.PRODUCTION_CANDIDATE.value
