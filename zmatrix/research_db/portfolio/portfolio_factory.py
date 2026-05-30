"""Phase 5: Portfolio Factory — build portfolios with constraints, NAV curve, risk metrics."""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib, json

@dataclass
class PortfolioSnapshot:
    portfolio_id: str; name: str; candidate_id: str = ""
    tickers: list = field(default_factory=list); weights: dict = field(default_factory=dict)
    nav_curve: list = field(default_factory=list); max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0; annual_return: float = 0.0; volatility: float = 0.0
    sector_exposure: dict = field(default_factory=dict); audit_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PortfolioFactory:
    def __init__(self, marketplace=None): self.marketplace = marketplace; self._portfolios: list[PortfolioSnapshot] = []

    def build(self, portfolio_id: str, candidate: "PortfolioCandidate", tickers: list[str] = None,
              max_positions: int = 20, sector_diversify: bool = True) -> PortfolioSnapshot:
        t = tickers or candidate.factor_ids[:max_positions]
        w = {tk: candidate.weights.get(tk, 1.0/len(t)) for tk in t} if t else {}
        p = PortfolioSnapshot(portfolio_id=portfolio_id, name=candidate.name,
                              candidate_id=candidate.candidate_id, tickers=t, weights=w)
        p.audit_hash = hashlib.sha256(json.dumps({"pid":portfolio_id,"tickers":sorted(t)},sort_keys=True).encode()).hexdigest()[:16]
        self._portfolios.append(p); return p

    def build_with_constraints(self, portfolio_id: str, candidate: "PortfolioCandidate",
                                max_positions: int = 20, sector_diversify: bool = True) -> PortfolioSnapshot:
        return self.build(portfolio_id, candidate, max_positions=max_positions, sector_diversify=sector_diversify)

    def list_all(self) -> list[PortfolioSnapshot]: return list(self._portfolios)
    def get_by_id(self, portfolio_id: str) -> PortfolioSnapshot | None:
        return next((p for p in self._portfolios if p.portfolio_id == portfolio_id), None)
