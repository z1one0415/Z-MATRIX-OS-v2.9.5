"""Batch-B: Factor Metrics Engine — IC, RankIC, HitRate, WinRate, LS Spread, Turnover, Coverage."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class FactorMetricsResult:
    factor_id: str; factor_name: str; ic: float = 0.0; rankic: float = 0.0
    hit_rate: float = 0.0; win_rate: float = 0.0; long_short_spread: float = 0.0
    turnover: float = 0.0; coverage: float = 0.0; universe_size: int = 0
    sample_size: int = 0; missing_count: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorMetricsEngine:
    @staticmethod
    def _validate_lists(a: list, b: list) -> tuple[list, list, int]:
        n = min(len(a), len(b))
        filtered = [(x, y) for (x, y) in zip(a[:n], b[:n]) if x is not None and y is not None]
        if not filtered: return [],[],n
        return list(zip(*filtered))[0], list(zip(*filtered))[1], len(a) - len(filtered)

    @staticmethod
    def compute_ic(factor_values, forward_returns) -> float:
        fv, fr, missing = FactorMetricsEngine._validate_lists(factor_values, forward_returns)
        if len(fv) < 3: return 0.0
        import statistics
        mean_f = statistics.mean(fv); mean_r = statistics.mean(fr)
        num = sum((x - mean_f) * (y - mean_r) for x, y in zip(fv, fr))
        den_f = sum((x - mean_f)**2 for x in fv)
        den_r = sum((y - mean_r)**2 for y in fr)
        den = (den_f * den_r) ** 0.5
        return num / den if den > 0 else 0.0

    @staticmethod
    def compute_rankic(factor_values, forward_returns) -> float:
        fv, fr, _ = FactorMetricsEngine._validate_lists(factor_values, forward_returns)
        if len(fv) < 3: return 0.0
        def rankify(data):
            sorted_idx = sorted(range(len(data)), key=lambda i: data[i])
            ranks = [0]*len(data)
            for rank, idx in enumerate(sorted_idx): ranks[idx] = rank + 1
            return ranks
        return FactorMetricsEngine.compute_ic(rankify(fv), rankify(fr))

    @staticmethod
    def compute_hit_rate(factor_values, forward_returns) -> float:
        fv, fr, _ = FactorMetricsEngine._validate_lists(factor_values, forward_returns)
        if not fv: return 0.0
        hits = sum(1 for x,y in zip(fv,fr) if (x>0)==(y>0))
        return hits / len(fv)

    @staticmethod
    def compute_win_rate(returns) -> float:
        valid = [r for r in returns if r is not None]
        if not valid: return 0.0
        return sum(1 for r in valid if r > 0) / len(valid)

    @staticmethod
    def compute_long_short_spread(top_returns, bottom_returns) -> float:
        t = [r for r in top_returns if r is not None]
        b = [r for r in bottom_returns if r is not None]
        if not t or not b: return 0.0
        import statistics
        return statistics.mean(t) - statistics.mean(b)

    @staticmethod
    def compute_turnover(current_positions, previous_positions) -> float:
        if not current_positions or not previous_positions: return 0.0
        cur_set = set(p["ticker"] for p in current_positions)
        prev_set = set(p["ticker"] for p in previous_positions)
        added = len(cur_set - prev_set); removed = len(prev_set - cur_set)
        total = len(cur_set | prev_set)
        return (added + removed) / total if total > 0 else 0.0

    @staticmethod
    def compute_coverage(factor_values, universe_size) -> float:
        valid = sum(1 for v in factor_values if v is not None)
        return valid / universe_size if universe_size > 0 else 0.0

    @staticmethod
    def compute_all(factor_id: str, factor_name: str, factor_values, forward_returns, universe_size: int) -> FactorMetricsResult:
        fv, fr, missing = FactorMetricsEngine._validate_lists(factor_values, forward_returns)
        return FactorMetricsResult(
            factor_id=factor_id, factor_name=factor_name,
            ic=FactorMetricsEngine.compute_ic(factor_values, forward_returns),
            rankic=FactorMetricsEngine.compute_rankic(factor_values, forward_returns),
            hit_rate=FactorMetricsEngine.compute_hit_rate(factor_values, forward_returns),
            win_rate=FactorMetricsEngine.compute_win_rate(forward_returns),
            long_short_spread=0.0, turnover=0.0,
            coverage=FactorMetricsEngine.compute_coverage(factor_values, universe_size),
            universe_size=universe_size, sample_size=len(fv), missing_count=missing,
        )
