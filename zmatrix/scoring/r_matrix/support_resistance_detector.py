"""Type A 支撑/阻力触碰验证器"""
from dataclasses import dataclass
import math

@dataclass
class SupportResistanceResult:
    passed: bool
    support_touches: int
    resistance_touches: int
    support_bounce_success: float
    resistance_reject_success: float
    reason: str

def _touch_indices(logp, lo, hi):
    return [i for i,x in enumerate(logp) if lo<=x<=hi]

def _dedupe_by_spacing(indices, min_spacing=10):
    out=[]; last=-10**9
    for i in indices:
        if i-last >= min_spacing: out.append(i); last=i
    return out

def verify_support_resistance(prices, lower, upper, forward_window=20, min_touches=3,
    min_spacing=10, bounce_threshold=0.08, reject_threshold=0.08):
    if len(prices)<120:
        return SupportResistanceResult(False,0,0,0,0,"insufficient prices")
    logp=[math.log(p) for p in prices if p>0]
    width=upper-lower
    if width<=0:
        return SupportResistanceResult(False,0,0,0,0,"invalid channel")
    s_hi=lower+0.15*width; r_lo=upper-0.15*width
    s_idx=_dedupe_by_spacing(_touch_indices(logp,lower,s_hi),min_spacing)
    r_idx=_dedupe_by_spacing(_touch_indices(logp,r_lo,upper),min_spacing)
    def bounce_ok(i):
        fut=prices[i+1:i+1+forward_window]
        return len(fut)>0 and max(fut)/prices[i]-1>=bounce_threshold
    def reject_ok(i):
        fut=prices[i+1:i+1+forward_window]
        return len(fut)>0 and 1-min(fut)/prices[i]>=reject_threshold
    s_ok=sum(1 for i in s_idx if bounce_ok(i))
    r_ok=sum(1 for i in r_idx if reject_ok(i))
    s_rate=s_ok/len(s_idx) if s_idx else 0; r_rate=r_ok/len(r_idx) if r_idx else 0
    passed=(len(s_idx)>=min_touches and len(r_idx)>=min_touches and s_rate>=0.5 and r_rate>=0.5)
    reason="support/resistance verified" if passed else "support/resistance not verified"
    return SupportResistanceResult(passed,len(s_idx),len(r_idx),round(s_rate,3),round(r_rate,3),reason)
