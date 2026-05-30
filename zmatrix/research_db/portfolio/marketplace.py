"""Phase 5: Factor Marketplace — search/filter/combine promoted factors into portfolio candidates."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PortfolioCandidate:
    candidate_id: str; name: str; factor_ids: list = field(default_factory=list)
    weights: dict = field(default_factory=dict); category: str = "MIXED"
    max_positions: int = 20; sector_diversify: bool = True
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorMarketplace:
    def __init__(self, ledger=None):
        self._candidates: list[PortfolioCandidate] = []; self.ledger = ledger

    def register(self, candidate: PortfolioCandidate) -> str:
        self._candidates.append(candidate); return candidate.candidate_id

    def search_by_category(self, category: str) -> list[PortfolioCandidate]:
        return [c for c in self._candidates if c.category == category]

    def filter_by_factors(self, factor_ids: list[str]) -> list[PortfolioCandidate]:
        return [c for c in self._candidates if any(f in c.factor_ids for f in factor_ids)]

    def combine_factors(self, name: str, factor_ids: list[str], weights: dict = None) -> PortfolioCandidate:
        w = weights or {f: 1.0/len(factor_ids) for f in factor_ids} if factor_ids else {}
        c = PortfolioCandidate(candidate_id=f"CAND-{len(self._candidates)+1:03d}", name=name,
                               factor_ids=factor_ids, weights=w)
        self._candidates.append(c); return c

    def list_all(self) -> list[PortfolioCandidate]: return list(self._candidates)
    def count(self) -> int: return len(self._candidates)
