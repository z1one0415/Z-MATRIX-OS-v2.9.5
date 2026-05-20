from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


def _clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


@dataclass(slots=True)
class SilentAccumulationResult:
    score: float
    stage_hint: str
    vcp_detected: bool
    relative_strength_score: float
    volume_accumulation_score: float
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def detect_vcp(retracements_pct: list[float]) -> bool:
    """Volatility contraction pattern: pullbacks contract over time."""

    if len(retracements_pct) < 3:
        return False
    vals = [abs(float(x)) for x in retracements_pct[-3:]]
    return vals[0] > vals[1] > vals[2]


def score_silent_accumulation(payload: dict[str, Any]) -> SilentAccumulationResult:
    retr = payload.get("retracements_pct") or []
    vcp = detect_vcp(retr)
    rs = float(payload.get("relative_strength_on_down_days", 0.0))  # 0-1
    volume_mild = float(payload.get("volume_mild_rising_score", 0.0))  # 0-10
    lows_not_down = bool(payload.get("lows_not_down", False))
    center_not_down = bool(payload.get("center_not_down", False))
    sector_hot_but_stock_flat = bool(payload.get("sector_hot_but_stock_flat", False))
    score = 0.0
    reasons: list[str] = []
    if vcp:
        score += 2.5; reasons.append("vcp_detected")
    score += _clamp(rs * 3.0, 0, 3.0)
    if rs >= 0.75:
        reasons.append("relative_strength_on_down_days")
    score += _clamp(volume_mild, 0, 10) * 0.2
    if lows_not_down:
        score += 1.0; reasons.append("lows_not_down")
    if center_not_down:
        score += 1.0; reasons.append("center_not_down")
    if sector_hot_but_stock_flat:
        score += 0.8; reasons.append("possible_pressure_accumulation")
    score = _clamp(score)
    return SilentAccumulationResult(
        score=round(score, 2),
        stage_hint="D2_SILENT_ACCUMULATION" if score >= 6.5 else "WATCH_ONLY",
        vcp_detected=vcp,
        relative_strength_score=round(_clamp(rs * 10), 2),
        volume_accumulation_score=round(_clamp(volume_mild), 2),
        reasons=reasons or ["insufficient_silent_accumulation_evidence"],
    )
