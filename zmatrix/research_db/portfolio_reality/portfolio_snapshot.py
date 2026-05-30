"""Batch-I: Portfolio Reality Snapshot — PIT-blocked state capture."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Optional


@dataclass
class PortfolioRealitySnapshot:
    snapshot_id: str
    portfolio_id: str
    as_of_date: str = field(default_factory=lambda: date.today().isoformat())
    capacity_grade: str = "E"
    liquidity_score: float = 100.0
    crowding_score: float = 0.0
    drift_score: float = 0.0
    audit_hash: str = ""
    ticker_count: int = 0
    notes: str = ""
    is_pit_protected: bool = True
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False
        if self.as_of_date > date.today().isoformat():
            raise ValueError(
                f"PIT VIOLATION: snapshot date {self.as_of_date} is in the future"
            )


class PortfolioSnapshot:
    @staticmethod
    def create(
        snapshot_id: str,
        portfolio_id: str,
        ticker_count: int = 0,
        capacity_grade: str = "E",
        liquidity_score: float = 100.0,
        crowding_score: float = 0.0,
        drift_score: float = 0.0,
        as_of_date: str | None = None,
    ) -> PortfolioRealitySnapshot:
        import hashlib
        import json

        snap = PortfolioRealitySnapshot(
            snapshot_id=snapshot_id,
            portfolio_id=portfolio_id,
            as_of_date=as_of_date or date.today().isoformat(),
            capacity_grade=capacity_grade,
            liquidity_score=liquidity_score,
            crowding_score=crowding_score,
            drift_score=drift_score,
            ticker_count=ticker_count,
        )
        payload = json.dumps({
            "sid": snapshot_id, "pid": portfolio_id,
            "d": snap.as_of_date, "cg": capacity_grade,
            "ls": liquidity_score, "cs": crowding_score,
            "ds": drift_score,
        }, sort_keys=True)
        snap.audit_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return snap

    @staticmethod
    def frozen_pit(
        snapshot_id: str,
        portfolio_id: str,
        as_of_date: str,
        **kwargs,
    ) -> PortfolioRealitySnapshot:
        return PortfolioSnapshot.create(
            snapshot_id=snapshot_id,
            portfolio_id=portfolio_id,
            as_of_date=as_of_date,
            **kwargs,
        )
