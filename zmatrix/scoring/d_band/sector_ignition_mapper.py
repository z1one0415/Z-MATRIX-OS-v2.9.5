from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


@dataclass(slots=True)
class SectorIgnitionResult:
    total_score_0_10: float
    normalized_score: float
    is_ignition: bool
    sector_stage_hint: str
    components: dict[str, float]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_sector_return(pct: float | None) -> float:
    if pct is None:
        return 5.0
    if pct >= 4:
        return 9.0
    if pct >= 2:
        return 7.5
    if pct >= 1:
        return 6.0
    if pct >= 0:
        return 4.5
    return 2.0


def score_breadth(pct: float | None) -> float:
    if pct is None:
        return 5.0
    if pct >= 80:
        return 9.0
    if pct >= 65:
        return 7.5
    if pct >= 55:
        return 6.0
    if pct >= 45:
        return 4.5
    return 2.5


def score_limit_count(count: int | None) -> float:
    if count is None:
        return 5.0
    if count >= 5:
        return 9.0
    if count >= 3:
        return 7.5
    if count >= 1:
        return 6.0
    return 3.5


def score_raw_0_10(v: float | None) -> float:
    if v is None:
        return 5.0
    return clamp(v)


def score_sector_ignition(payload: dict[str, Any]) -> SectorIgnitionResult:
    comps = {
        "sector_return": score_sector_return(payload.get("sector_return_pct")),
        "breadth": score_breadth(payload.get("breadth_pct")),
        "limit_count": score_limit_count(payload.get("limit_count")),
        "leader_strength": score_raw_0_10(payload.get("leader_strength_score")),
        "diffusion": score_raw_0_10(payload.get("diffusion_score")),
        "turnover_share_delta": score_raw_0_10(payload.get("turnover_share_delta_score")),
    }
    total = (
        comps["sector_return"] * 0.20
        + comps["breadth"] * 0.20
        + comps["limit_count"] * 0.15
        + comps["leader_strength"] * 0.20
        + comps["diffusion"] * 0.15
        + comps["turnover_share_delta"] * 0.10
    )
    norm = total / 10.0
    notes = []
    if norm >= 0.75:
        stage = "CONFIRMATION_OR_LEADING"
        notes.append("板块点火并进入确认/主升倾向")
    elif norm >= 0.65:
        stage = "IGNITION"
        notes.append("板块处于点火早期")
    elif norm >= 0.50:
        stage = "NEUTRAL_WATCH"
    else:
        stage = "COLD_OR_RETREAT"
    return SectorIgnitionResult(round(total, 2), round(norm, 3), norm >= 0.65, stage, comps, notes)
