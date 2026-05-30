"""Phase 3-B: Outcome Fixture Builder — synthetic test data only."""
from __future__ import annotations

def build_outcome_test_requests() -> list[dict]:
    return [
        {"ticker":"000001","observation_date":"2024-01-02","horizon":"T5"},
        {"ticker":"000001","observation_date":"2024-01-02","horizon":"T20"},
        {"ticker":"000001","observation_date":"2024-01-30","horizon":"T60"},
        {"ticker":"600519","observation_date":"2024-01-04","horizon":"T5"},
    ]

def build_insufficient_forward_days_cases() -> list[dict]:
    return [
        {"ticker":"000001","observation_date":"2024-02-02","horizon":"T20"},
        {"ticker":"000001","observation_date":"2024-01-31","horizon":"T60"},
    ]

def build_missing_bar_cases() -> list[dict]:
    return [
        {"ticker":"999999","observation_date":"2024-01-02","horizon":"T5"},
        {"ticker":"000001","observation_date":"2024-01-01","horizon":"T1"},
    ]
