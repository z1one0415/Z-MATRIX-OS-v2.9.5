from dataclasses import dataclass
from typing import List
import math

@dataclass
class ResidualReversionResult:
    dfa_hurst: float
    half_life: float
    mean_reverting: bool
    notes: list[str]


def dfa_hurst(series: List[float], min_scale: int = 8) -> float:
    """Minimal DFA-Hurst estimator for engineering screening.

    This is intentionally compact. Production can replace with a vetted numerical package.
    """
    n = len(series)
    if n < 60:
        return 0.5
    mean = sum(series) / n
    y = []
    c = 0.0
    for v in series:
        c += v - mean
        y.append(c)
    scales = [s for s in [min_scale, 12, 16, 24, 32, 48, 64] if s < n // 2]
    fluct = []
    used = []
    for s in scales:
        vals = []
        for start in range(0, n - s + 1, s):
            seg = y[start:start+s]
            # detrend by line between endpoints
            if s <= 1:
                continue
            a = seg[0]
            b = (seg[-1] - seg[0]) / (s - 1)
            res = [seg[i] - (a + b * i) for i in range(s)]
            vals.append(math.sqrt(sum(r*r for r in res) / s))
        if vals:
            fluct.append(sum(vals)/len(vals))
            used.append(s)
    if len(fluct) < 2 or any(f <= 0 for f in fluct):
        return 0.5
    lx = [math.log(s) for s in used]
    ly = [math.log(f) for f in fluct]
    xbar = sum(lx)/len(lx); ybar = sum(ly)/len(ly)
    denom = sum((x-xbar)**2 for x in lx)
    if denom == 0:
        return 0.5
    return sum((x-xbar)*(y-ybar) for x,y in zip(lx,ly))/denom


def estimate_half_life(series: List[float]) -> float:
    """AR(1)-style half-life for residual mean reversion."""
    if len(series) < 30:
        return float('inf')
    x = series[:-1]
    y = [series[i+1] - series[i] for i in range(len(series)-1)]
    xbar = sum(x)/len(x); ybar = sum(y)/len(y)
    denom = sum((v-xbar)**2 for v in x)
    if denom == 0:
        return float('inf')
    beta = sum((a-xbar)*(b-ybar) for a,b in zip(x,y))/denom
    if beta >= 0:
        return float('inf')
    try:
        return -math.log(2) / beta
    except Exception:
        return float('inf')


def residual_reversion_check(residuals: List[float], hurst_threshold: float = 0.48, max_half_life: float = 80.0) -> ResidualReversionResult:
    h = dfa_hurst(residuals)
    hl = estimate_half_life(residuals)
    notes = []
    if h >= hurst_threshold:
        notes.append("DFA-Hurst does not show strong mean reversion")
    if not (0 < hl <= max_half_life):
        notes.append("Residual half-life is too long or invalid")
    return ResidualReversionResult(dfa_hurst=h, half_life=hl, mean_reverting=(h < hurst_threshold and 0 < hl <= max_half_life), notes=notes)
