from dataclasses import dataclass
from typing import List

@dataclass
class RisingChannelPosition:
    position: float
    zone: str
    lower: float
    upper: float


def _quantile(xs: List[float], q: float) -> float:
    if not xs:
        raise ValueError("empty series")
    ys = sorted(xs)
    idx = min(max(int(round((len(ys)-1)*q)), 0), len(ys)-1)
    return ys[idx]


def locate_residual_position(residuals: List[float], q_low: float = 0.05, q_high: float = 0.95) -> RisingChannelPosition:
    if len(residuals) < 30:
        return RisingChannelPosition(0.5, "UNKNOWN", 0.0, 0.0)
    lower = _quantile(residuals, q_low)
    upper = _quantile(residuals, q_high)
    current = residuals[-1]
    width = upper - lower
    if width <= 1e-9:
        return RisingChannelPosition(0.5, "NARROW_CHANNEL", lower, upper)
    pos = (current - lower) / width
    if pos < 0:
        zone = "UNDERCUT"
    elif pos < 0.25:
        zone = "LOW_ZONE"
    elif pos < 0.45:
        zone = "LOW_REPAIR_ZONE"
    elif pos < 0.70:
        zone = "MID_ZONE"
    else:
        zone = "HIGH_HARVEST_ZONE"
    return RisingChannelPosition(pos, zone, lower, upper)
