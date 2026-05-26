"""Benchmark Relative — excess return vs index"""
from __future__ import annotations

def calc_excess_return(paper_return: float | None, benchmark_return: float | None) -> float | None:
    """Calculate excess return = paper_return - benchmark_return."""
    if paper_return is None or benchmark_return is None:
        return None
    return round(paper_return - benchmark_return, 2)

def calc_benchmark_comparison(paper_returns: dict, benchmark_returns: dict) -> dict:
    """Compare paper returns against benchmark for all horizons."""
    return {
        "excess_return_t5": calc_excess_return(paper_returns.get("actual_return_t5"), benchmark_returns.get("bm_return_t5")),
        "excess_return_t20": calc_excess_return(paper_returns.get("actual_return_t20"), benchmark_returns.get("bm_return_t20")),
        "excess_return_t60": calc_excess_return(paper_returns.get("actual_return_t60"), benchmark_returns.get("bm_return_t60")),
    }
