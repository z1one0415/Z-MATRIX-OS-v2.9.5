"""轮动天王 — Bi-weekly Rotation King (双周线)

与波动天王(OscillationKing)的区别:
  波动天王: 日线级别, Type A(水平箱体)/Type B(上升通道) — 日内/周内波动
  轮动天王: 双周线级别 (bi-weekly), 识别月线趋势 + 周期轮动阶段 + 位置操作建议

分类:
  RISING:   月线β>0.8% — 上升趋势中
  HORIZONTAL: |β|<0.8% — 月线箱体震荡
  DECLINING: 月线β<-0.8% — 下降趋势

位置:
  <0.25: 低位(潜在买点) → WATCH_ENTRY
  0.25-0.75: 中位 → HOLD/WAIT
  >0.75: 高位(潜在卖点) → HARVEST
"""
from __future__ import annotations
from datetime import datetime, timedelta


def classify_rotation_trend(closes: list[float], dates: list[str] | None = None,
                           beta_threshold: float = 0.008) -> dict:
    """月线轮动分类 — 基于最近12个月close数据。

    Returns:
        type: RISING | HORIZONTAL | DECLINING
        beta_norm: 标准化趋势斜率(%/月)
        channel_amp: 通道振幅(%)
        position: 当前在12个月通道中的位置(0-1)
        action: HARVEST | HOLD | WATCH_ENTRY | AVOID
    """
    n = min(12, len(closes))
    recent = list(closes[-n:])

    if len(recent) < 3:
        return {"type": "DATA_INSUFFICIENT", "beta_norm": 0, "channel_amp": 0,
                "position": 0.5, "action": "WAIT"}

    # Rolling OLS trend
    x = list(range(n))
    mean_x = sum(x) / n
    mean_y = sum(recent) / n
    num = sum((x[i] - mean_x) * (recent[i] - mean_y) for i in range(n))
    den = max(sum((x[i] - mean_x) ** 2 for i in range(n)), 0.0001)
    beta = num / den
    beta_norm = beta / max(abs(mean_y), 0.01)

    # Channel amplitude
    mn, mx = min(recent), max(recent)
    channel_amp = (mx / mn - 1) * 100 if mn > 0 else 0

    # Classification
    if abs(beta_norm) < beta_threshold:
        osc_type = "HORIZONTAL"
    elif beta_norm > 0:
        osc_type = "RISING"
    else:
        osc_type = "DECLINING"

    # Position in channel
    pos = (recent[-1] - mn) / max(mx - mn, 0.01)

    # Action mapping
    if osc_type == "RISING":
        action = "HARVEST" if pos > 0.75 else ("WATCH_ENTRY" if pos < 0.25 else "HOLD")
    elif osc_type == "HORIZONTAL":
        action = "WATCH_ENTRY" if pos < 0.3 else ("HARVEST" if pos > 0.7 else "WAIT")
    else:
        action = "AVOID"

    return {
        "type": osc_type,
        "beta_norm": round(beta_norm * 100, 2),
        "channel_amp": round(channel_amp, 1),
        "position": round(pos, 2),
        "action": action,
        "months": len(recent),
    }
