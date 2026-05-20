from dataclasses import dataclass
from typing import List

@dataclass
class VolatilityConeResult:
    decay_ratio: float
    state: str
    reason: str


def residual_volatility_cone(residuals: List[float], watch_threshold: float = 0.50, expired_threshold: float = 0.35) -> VolatilityConeResult:
    if len(residuals) < 120:
        return VolatilityConeResult(decay_ratio=1.0, state="UNKNOWN", reason="insufficient residual history")
    mid = len(residuals)//2
    early = residuals[:mid]
    recent = residuals[mid:]
    early_amp = sum(abs(x) for x in early) / max(len(early), 1)
    recent_amp = sum(abs(x) for x in recent) / max(len(recent), 1)
    if early_amp == 0:
        return VolatilityConeResult(decay_ratio=1.0, state="ACTIVE", reason="no early residual amplitude")
    ratio = recent_amp / early_amp
    if ratio < expired_threshold:
        return VolatilityConeResult(decay_ratio=ratio, state="OSCILLATION_EXPIRED", reason="residual amplitude collapsed")
    if ratio < watch_threshold:
        return VolatilityConeResult(decay_ratio=ratio, state="OSCILLATION_DECAY", reason="residual amplitude decayed")
    return VolatilityConeResult(decay_ratio=ratio, state="ACTIVE", reason="residual amplitude remains active")
