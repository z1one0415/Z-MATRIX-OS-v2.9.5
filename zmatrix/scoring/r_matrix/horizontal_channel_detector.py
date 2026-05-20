"""Type A 水平通道检测器 — quantile channel + rolling OLS slope filter"""
from dataclasses import dataclass
import math
from .rolling_trend_channel import rolling_ols_residuals

@dataclass
class HorizontalChannelResult:
    passed: bool
    beta: float
    lower: float
    upper: float
    mid: float
    amplitude: float
    channel_position: float
    residuals: list
    reason: str

def _quantile(xs: list, q: float) -> float:
    s = sorted(xs)
    idx = min(len(s)-1, max(0, int((len(s)-1)*q)))
    return s[idx]

def detect_horizontal_channel(prices, window=250, beta_flat_threshold=0.00008,
    max_endpoint_drift=0.25, min_amplitude=0.25, max_amplitude=1.20):
    if len(prices) < window:
        return HorizontalChannelResult(False,0,0,0,0,0,0,[],"insufficient prices")
    if any(p<=0 for p in prices):
        return HorizontalChannelResult(False,0,0,0,0,0,0,[],"non-positive price")
    recent = prices[-window:]
    # endpoint drift
    drift = recent[-1]/recent[0]-1
    if abs(drift) > max_endpoint_drift:
        return HorizontalChannelResult(False,0,0,0,0,0,0,[],f"drift {drift:.2%} > {max_endpoint_drift:.0%}")
    # rolling OLS beta
    pts = rolling_ols_residuals(prices, window=window, include_current_for_next_day=False)
    if not pts:
        return HorizontalChannelResult(False,0,0,0,0,0,0,[],"no rolling OLS")
    beta = pts[-1].beta
    if abs(beta) > beta_flat_threshold:
        return HorizontalChannelResult(False,beta,0,0,0,0,0,[],f"beta {beta:.6f} > {beta_flat_threshold}")
    # quantile channel
    logp = [math.log(p) for p in recent]
    lower = _quantile(logp, 0.10)
    upper = _quantile(logp, 0.90)
    mid = _quantile(logp, 0.50)
    if upper <= lower:
        return HorizontalChannelResult(False,beta,lower,upper,mid,0,0,[],"invalid channel")
    amplitude = math.exp(upper-lower)-1
    if amplitude < min_amplitude:
        return HorizontalChannelResult(False,beta,lower,upper,mid,amplitude,0,[],f"amp {amplitude:.0%}<{min_amplitude:.0%}")
    if amplitude > max_amplitude:
        return HorizontalChannelResult(False,beta,lower,upper,mid,amplitude,0,[],f"amp {amplitude:.0%}>{max_amplitude:.0%}")
    pos = (logp[-1]-lower)/(upper-lower)
    residuals = [x-mid for x in logp]
    return HorizontalChannelResult(True,beta,lower,upper,mid,amplitude,pos,residuals,"horizontal channel candidate")
