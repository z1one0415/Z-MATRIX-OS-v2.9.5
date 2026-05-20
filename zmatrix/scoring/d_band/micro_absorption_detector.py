from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


def _clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


@dataclass(slots=True)
class MicroAbsorptionResult:
    score: float
    status: str
    level2_required_for_real: bool
    allowed_lifecycle_max: str
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_micro_absorption(payload: dict[str, Any] | float | int | None) -> MicroAbsorptionResult:
    """M1 approximation for micro absorption.

    This is not a Level-2 confirmation.  It can raise paper confidence only.
    Numeric input is treated as an already-normalized upstream score for compatibility
    with coverage fields.
    """

    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        score = _clamp(float(payload))
        return MicroAbsorptionResult(
            score=round(score, 2),
            status="M1_APPROX_CONFIRMED" if score >= 6.0 else "M1_WEAK_OR_UNKNOWN",
            level2_required_for_real=True,
            allowed_lifecycle_max="D3_CANDIDATE",
            reasons=["upstream_micro_absorption_score"],
        )

    score = 0.0
    reasons: list[str] = []
    if bool(payload.get("down_minutes_volume_contract", False)):
        score += 1.8; reasons.append("down_volume_contract")
    if bool(payload.get("up_minutes_volume_expand", False)):
        score += 1.8; reasons.append("up_volume_expand")
    if bool(payload.get("vwap_reclaim", False)):
        score += 1.6; reasons.append("vwap_reclaim")
    if bool(payload.get("pullback_not_break_low", False)):
        score += 1.5; reasons.append("pullback_not_break_low")
    if bool(payload.get("index_drop_stock_hold", False)):
        score += 1.3; reasons.append("index_drop_stock_hold")
    close_pos = float(payload.get("close_position_pct", 50.0))
    if close_pos >= 65:
        score += 1.0; reasons.append("close_high")
    score = _clamp(score)
    status = "M1_APPROX_CONFIRMED" if score >= 6.0 else "M1_WEAK_OR_UNKNOWN"
    return MicroAbsorptionResult(
        score=round(score, 2),
        status=status,
        level2_required_for_real=True,
        allowed_lifecycle_max="D3_CANDIDATE",
        reasons=reasons or ["no_absorption_evidence"],
    )
