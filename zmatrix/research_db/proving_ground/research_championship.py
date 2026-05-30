"""F.5-6: Research Championship — auto-compare factors/portfolios → Winner Table."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ChampionshipResult:
    entry_id: str; entry_type: str  # FACTOR or PORTFOLIO
    ic: float = 0.0; sharpe: float = 0.0; max_dd: float = 0.0
    walk_forward_grade: str = "F"; regime_robustness: float = 0.0
    overall_score: float = 0.0; rank: int = 0; status: str = "UNRANKED"
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class ChampionshipTable:
    table_id: str; entries: list = field(default_factory=list)
    winners: list = field(default_factory=list); retired: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchChampionship:
    @staticmethod
    def score_entry(entry_id: str, entry_type: str, metrics: dict) -> ChampionshipResult:
        r = ChampionshipResult(entry_id=entry_id, entry_type=entry_type, ic=metrics.get("ic",0),
                               sharpe=metrics.get("sharpe",0), max_dd=metrics.get("max_dd",0),
                               walk_forward_grade=metrics.get("wf_grade","F"), regime_robustness=metrics.get("robustness",0))
        r.overall_score = (abs(r.ic) * 0.3 + max(0, r.sharpe) * 0.2 + (1.0 - abs(r.max_dd)) * 0.2 +
                           (1.0 if r.walk_forward_grade in ("A","B") else 0.5 if r.walk_forward_grade=="C" else 0) * 0.15 +
                           r.regime_robustness * 0.15)
        return r

    @staticmethod
    def run_championship(entries: list[dict]) -> ChampionshipTable:
        results = [ResearchChampionship.score_entry(e["id"], e["type"], e.get("metrics",{})) for e in entries]
        sorted_results = sorted(results, key=lambda x: x.overall_score, reverse=True)
        for i, r in enumerate(sorted_results): r.rank = i + 1
        winners = [r for r in sorted_results if r.rank <= 3]
        retired = [r for r in sorted_results if r.overall_score < 0.2]
        for r in retired: r.status = "RETIRED"
        for r in winners: r.status = "WINNER"
        return ChampionshipTable(table_id=f"CHAMP-{len(results)}", entries=sorted_results, winners=winners, retired=retired)
