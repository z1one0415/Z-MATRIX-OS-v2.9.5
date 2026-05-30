"""Phase 3-C: Alpha Engine — benchmark relative returns."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AlphaResult:
    benchmark_code: str; benchmark_return: float = 0.0; excess_return: float = 0.0
    alpha_status: str = "UNKNOWN"; production_allowed: bool = field(default=False,repr=False)
    def __post_init__(self): self.production_allowed=False

class AlphaEngine:
    @staticmethod
    def compute_benchmark_return(benchmark_id: str, entry_date: str, exit_date: str,
                                  price_bar_store) -> float:
        """Compute benchmark return between entry_date and exit_date using close prices."""
        # Map benchmark_id to ticker via benchmark_registry lookup from bar_store
        entry_bar = price_bar_store.get_bar(benchmark_id, entry_date)
        exit_bar = price_bar_store.get_bar(benchmark_id, exit_date)
        if entry_bar is None or exit_bar is None or entry_bar.get("close",0) <= 0:
            return 0.0
        return (exit_bar["close"] - entry_bar["close"]) / entry_bar["close"]

    @staticmethod
    def compute_alpha(signal_return: float, benchmark_return: float) -> float:
        return signal_return - benchmark_return

    @staticmethod
    def compute_alpha_vs_market(entry_price: float, exit_price: float, entry_date: str,
                                 exit_date: str, bar_store, benchmark_registry) -> dict:
        signal_return = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0
        bm_id = benchmark_registry.get_default_benchmark("STOCK")
        bm_return = AlphaEngine.compute_benchmark_return(bm_id, entry_date, exit_date, bar_store)
        return {"market_return": bm_return, "alpha_vs_market": signal_return - bm_return,
                "benchmark_code": bm_id, "production_allowed": False}

    @staticmethod
    def compute_alpha_vs_all(entry_price: float, exit_price: float, entry_date: str,
                              exit_date: str, bar_store, benchmark_registry) -> list[dict]:
        signal_return = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0
        results = []
        for bm in benchmark_registry.list_benchmarks():
            bm_return = AlphaEngine.compute_benchmark_return(bm["benchmark_id"], entry_date, exit_date, bar_store)
            results.append({"benchmark_id": bm["benchmark_id"], "benchmark_name": bm["benchmark_name"],
                           "benchmark_return": bm_return, "excess_return": signal_return - bm_return,
                           "production_allowed": False})
        return results
