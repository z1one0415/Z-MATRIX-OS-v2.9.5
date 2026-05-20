from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(slots=True)
class TailGrabValidation:
    validated: bool
    failed: bool
    status: str
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_next_day_tail_grab(
    open_gap_pct: float,
    early_vwap_break: bool,
    sector_retreat: bool,
    holds_tail_start_price: bool,
    max_allowed_gap_down_pct: float = -3.0,
) -> TailGrabValidation:
    """Validate whether a prior smart-money tail grab was real or a next-day trap."""

    reasons: list[str] = []
    if open_gap_pct <= max_allowed_gap_down_pct:
        reasons.append("gap_down_too_large")
    if early_vwap_break:
        reasons.append("early_vwap_break")
    if sector_retreat:
        reasons.append("sector_retreat")
    if not holds_tail_start_price:
        reasons.append("lost_tail_start_price")
    failed = bool(reasons)
    return TailGrabValidation(
        validated=not failed,
        failed=failed,
        status="TAIL_GRAB_VALIDATED" if not failed else "FALSE_PREHEAT_CONFIRMED",
        reasons=reasons or ["next_day_validation_passed"],
    )
