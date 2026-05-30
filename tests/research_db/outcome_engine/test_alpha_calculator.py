#!/usr/bin/env python3
"""Phase 3-B: Alpha Calculator Tests (8+)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.outcome_engine.alpha_calculator import (
    compute_gross_return,
    compute_benchmark_return,
    compute_alpha,
    compute_max_excursion,
)
from math import isclose


def test_compute_gross_return_positive():
    assert isclose(compute_gross_return(10.0, 10.5), 0.05)


def test_compute_gross_return_negative():
    assert isclose(compute_gross_return(10.0, 9.0), -0.10)


def test_compute_gross_return_zero():
    assert isclose(compute_gross_return(10.0, 10.0), 0.0)


def test_compute_gross_return_large_gain():
    assert isclose(compute_gross_return(5.0, 10.0), 1.0)


def test_compute_benchmark_return():
    prices = {"2024-01-02": 3000.0, "2024-01-30": 3036.0}
    r = compute_benchmark_return(prices, "2024-01-02", "2024-01-30")
    assert isclose(r, 0.012)


def test_compute_benchmark_return_missing_entry():
    prices = {"2024-01-30": 3036.0}
    r = compute_benchmark_return(prices, "2024-01-02", "2024-01-30")
    assert r is None


def test_compute_benchmark_return_missing_exit():
    prices = {"2024-01-02": 3000.0}
    r = compute_benchmark_return(prices, "2024-01-02", "2024-01-30")
    assert r is None


def test_compute_alpha_positive():
    assert isclose(compute_alpha(0.05, 0.02), 0.03)


def test_compute_alpha_negative():
    assert isclose(compute_alpha(-0.05, 0.02), -0.07)


def test_compute_alpha_benchmark_none():
    assert compute_alpha(0.05, None) is None


def test_compute_max_excursion():
    bars = [
        {"high": 10.5, "low": 9.8, "close": 10.0},
        {"high": 11.0, "low": 9.5, "close": 10.2},
        {"high": 10.8, "low": 9.2, "close": 10.5},
    ]
    max_fav, max_adv = compute_max_excursion(bars, 10.0)
    assert isclose(max_fav, 0.10)  # (11.0 - 10.0) / 10.0
    assert isclose(max_adv, 0.08)  # (10.0 - 9.2) / 10.0


def test_compute_max_excursion_no_excursion():
    bars = [{"high": 10.0, "low": 10.0, "close": 10.0}]
    max_fav, max_adv = compute_max_excursion(bars, 10.0)
    assert isclose(max_fav, 0.0)
    assert isclose(max_adv, 0.0)


def test_compute_max_excursion_fallback_close():
    bars = [{"close": 11.5}, {"close": 9.0}]
    max_fav, max_adv = compute_max_excursion(bars, 10.0)
    assert isclose(max_fav, 0.15)
    assert isclose(max_adv, 0.10)


if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
