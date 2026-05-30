"""OutcomeSnapshot — PIT-compliant snapshot dataclass with future-access blocking."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Optional


@dataclass
class OutcomeSnapshot:
    snapshot_id: str
    universe_id: str
    as_of_date: str
    total_events: int = 0
    market_return: float = 0.0
    regime_distribution: dict = field(default_factory=dict)
    event_coverage: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    _as_of_timestamp: float = field(default=0.0, repr=False)

    def __post_init__(self):
        self.production_allowed = False
        if isinstance(self._as_of_timestamp, float) and self._as_of_timestamp == 0.0:
            self._as_of_timestamp = datetime.now(timezone.utc).timestamp()

    def _block_future_access(self, requested_date: str) -> None:
        from datetime import date as dt_date
        try:
            req_dt = dt_date.fromisoformat(requested_date)
            as_of_dt = dt_date.fromisoformat(self.as_of_date)
            if req_dt > as_of_dt:
                raise ValueError(
                    f"PIT BLOCKED: requested_date {requested_date} is after as_of_date {self.as_of_date}"
                )
        except ValueError as e:
            if "PIT BLOCKED" in str(e):
                raise
            pass

    def get_regime_for(self, regime: str) -> int:
        self._block_future_access(self.as_of_date)
        return self.regime_distribution.get(regime, 0)

    def get_coverage_for(self, year: str) -> int:
        self._block_future_access(self.as_of_date)
        return self.event_coverage.get(str(year), 0)

    @staticmethod
    def build_snapshot(universe, as_of_date: str | None = None) -> OutcomeSnapshot:
        from .outcome_universe import OutcomeUniverse
        events = universe.list_events()
        as_of = as_of_date or date.today().isoformat()
        regime_dist = universe.type_distribution()
        coverage: dict[str, int] = {}
        for year in universe.years_covered():
            coverage[str(year)] = len(universe.events_in_year(year))
        mr_agg = universe.aggregate_return()
        snapshot_id = f"OS-{as_of}-{len(events)}"
        return OutcomeSnapshot(
            snapshot_id=snapshot_id,
            universe_id="outcome_universe_v1",
            as_of_date=as_of,
            total_events=len(events),
            market_return=mr_agg.get("avg", 0.0),
            regime_distribution=regime_dist,
            event_coverage=coverage,
        )

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "universe_id": self.universe_id,
            "as_of_date": self.as_of_date,
            "total_events": self.total_events,
            "market_return": self.market_return,
            "regime_distribution": dict(self.regime_distribution),
            "event_coverage": dict(self.event_coverage),
            "created_at": self.created_at,
            "production_allowed": False,
        }
