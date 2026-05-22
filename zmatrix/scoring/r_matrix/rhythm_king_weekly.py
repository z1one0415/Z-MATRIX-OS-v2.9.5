"""R-Matrix 律动天王 / 波动天王 — multi-scale BOX/TREND classifier

Usage:
  冲动天王(日线): window=500, beta=0.008 → Type A/B via oscillation_king_ranker
  波动天王(5日): window=50, beta=0.002, step=5 → BOX hunter (17% BOX optimal)
  律动天王(周线): window=26, beta=0.004 → mid-term swing (30% BOX)
  轮动天王(双周): window=30, beta=0.004, step=10 → rotation entry (13% BOX)

与波动天王/轮动天王的区别:
  波动天王(日): OscillationKing — Type A水平箱体 / Type B上升通道 (500日K, 日线级别)
  律动天王(周): RhythmKing    — BOX箱体 / TREND_UP上升 / TREND_DOWN下降 (26周K, 中线级别)
  轮动天王(月): RotationKing  — RISING/HORIZONTAL/DECLINING (12月K, 长线级别)

最佳尺度: 周线BOX占比约30% > 日线0% > 月线4%
         周线是最优均值回归交易尺度

通道识别逻辑:
  BOX (箱体震荡):
    条件: |β_norm| < 0.004 (趋势极弱) + 振幅15-120% (有交易价值)
    入场: position < 0.3 (箱体底部)
    出场: position > 0.7 (箱体顶部)
    优化: mr_ratio < 1.0 (波动在压缩→即将突破)

  TREND_UP (上升通道):
    条件: β_norm > 0.004 (正趋势) + 周线站上MA13
    入场: position < 0.6 (通道中低位)
    持有: position 0.6-0.85 (通道中高位, 趋势还在)
    收割: position > 0.85 (接近通道上沿)
    OLS残差: 计算残差回归通道 → 识别超买/超卖

  TREND_DOWN (下降通道):
    条件: β_norm < -0.004 (负趋势)
    动作: AVOID (不参与下降趋势)

动作映射:
  WATCH_ENTRY: 箱体底部, 低风险买入区
  RIDE:        上升趋势中低位, 顺势加仓区
  HOLD:        上升趋势中高位, 持有观察
  HARVEST:     箱体顶部/趋势末端, 获利了结
  WAIT:        箱体中位, 等方向确认
  AVOID:       下降趋势, 不参与
"""
from __future__ import annotations
from typing import List


def classify_rhythm(
    closes: List[float],
    dates: List[str] | None = None,
    beta_threshold: float = 0.004,
    box_amp_min: float = 10.0,
    box_amp_max: float = 150.0,
) -> dict:
    """周线律动天王 — 26周滚动窗口三通道识别。

    Args:
        closes: 周线close序列 (至少20根)
        beta_threshold: OLS趋势斜率阈值 (默认0.004 = 0.4%/周 ≈ 1.6%/月)
        box_amp_min: BOX最小振幅 (低于此值无交易价值)
        box_amp_max: BOX最大振幅 (高于此值视为趋势而非箱体)

    Returns:
        type: BOX | TREND_UP | TREND_DOWN
        beta_norm: 标准化周趋势 (%)
        channel_amp: 26周通道振幅 (%)
        position: 当前在通道中的位置 (0-1)
        mr_ratio: 均值回归比率 (<1波动压缩, >1波动扩张)
        ma13: 13周均线位置 (1=上方, -1=下方)
        action: WATCH_ENTRY | RIDE | HOLD | HARVEST | WAIT | AVOID
        channel_upper: 通道上轨价格 (相对于最新close的比例)
        channel_lower: 通道下轨价格
    """
    n = min(26, len(closes))
    if n < 20:
        return _data_insufficient()

    recent = list(closes[-n:])

    # ── 1. Rolling OLS 趋势识别 ──
    x = list(range(n))
    mean_x = sum(x) / n
    mean_y = sum(recent) / n
    num = sum((x[i] - mean_x) * (recent[i] - mean_y) for i in range(n))
    den = max(sum((x[i] - mean_x) ** 2 for i in range(n)), 0.0001)
    beta = num / den
    beta_norm = beta / max(abs(mean_y), 0.01)

    # OLS residuals for channel detection
    residuals = [recent[i] - (mean_y + beta * (x[i] - mean_x)) for i in range(n)]
    residual_range = max(residuals) - min(residuals)

    # ── 2. 通道识别 ──
    mn, mx = min(recent), max(recent)
    amp = (mx / mn - 1) * 100 if mn > 0 else 100
    pos = (recent[-1] - mn) / max(mx - mn, 0.01)

    # 均值回归比率: 近8周振幅 / 26周振幅
    recent8 = recent[-8:] if len(recent) >= 8 else recent
    r8_range = max(recent8) / min(recent8) - 1 if min(recent8) > 0 else 0
    full_range = mx / mn - 1 if mn > 0 else 0.001
    mr_ratio = round(r8_range / max(full_range, 0.001), 2)

    # MA13 position
    ma13_val = sum(recent[-13:]) / min(len(recent[-13:]), 13) if len(recent) >= 13 else mean_y
    above_ma13 = 1 if recent[-1] > ma13_val else -1

    # ── 3. 三通道分类 ──
    abs_beta = abs(beta_norm)

    if abs_beta < beta_threshold and box_amp_min <= amp <= box_amp_max:
        # BOX: 趋势极弱 + 振幅在可交易区间
        channel_type = "BOX"
        # 位置映射
        if pos < 0.25:
            action = "WATCH_ENTRY"  # 箱体底部, 低风险买入区
        elif pos > 0.75:
            action = "HARVEST"      # 箱体顶部, 获利了结
        elif 0.35 <= pos <= 0.65:
            action = "WAIT"         # 箱体中位, 等方向确认
        else:
            action = "HOLD"         # 偏箱体边缘, 持有观察

    elif beta_norm > beta_threshold:
        # TREND_UP: 正趋势
        channel_type = "TREND_UP"
        if pos < 0.60:
            action = "RIDE"          # 趋势中低位, 顺势加仓
        elif pos > 0.85:
            action = "HARVEST"       # 趋势末端, 超买
        else:
            action = "HOLD"          # 上升趋势中高位, 持有

    else:
        # TREND_DOWN: 负趋势
        channel_type = "TREND_DOWN"
        action = "AVOID"

    # ── 4. 残差通道边界 ──
    # 基于OLS残差计算标准化通道
    mid_price = mean_y + beta * (n - 1)  # OLS预估当前价
    channel_upper = (mid_price + residual_range * 1.5) / max(recent[-1], 0.01)
    channel_lower = (mid_price - residual_range * 1.5) / max(recent[-1], 0.01)

    return {
        "type": channel_type,
        "beta_norm": round(beta_norm * 100, 2),
        "channel_amp": round(amp, 1),
        "position": round(pos, 2),
        "mr_ratio": mr_ratio,
        "above_ma13": above_ma13,
        "action": action,
        "residual_range_pct": round(residual_range / max(abs(mean_y), 0.01) * 100, 1),
        "channel_upper_ratio": round(channel_upper, 2),
        "channel_lower_ratio": round(channel_lower, 2),
        "weeks": n,
        "latest_close": recent[-1],
        "ma13": round(ma13_val, 2),
    }


def _data_insufficient() -> dict:
    return {
        "type": "DATA_INSUFFICIENT",
        "beta_norm": 0, "channel_amp": 0, "position": 0.5,
        "mr_ratio": 0, "above_ma13": 0, "action": "WAIT",
        "residual_range_pct": 0, "channel_upper_ratio": 1, "channel_lower_ratio": 1,
        "weeks": 0, "latest_close": 0, "ma13": 0,
    }


# ── Four King aliases ──

def impulse_king_daily(closes, dates=None):
    """冲动天王: 日线500K → 委托 oscillation_king_ranker Type A/B.
    不在此模块实现, 仅提供接口别名。"""
    return {"type": "IMPULSE_DELEGATED", "note": "use oscillation_king_ranker_v11 for daily"}


def oscillation_king_5d(closes, dates=None):
    """波动天王: 5日线50K → BOX hunter (17% BOX optimal)."""
    return classify_rhythm(closes, dates, beta_threshold=0.002, box_amp_min=5.0, box_amp_max=200.0)


def rhythm_king_weekly(closes, dates=None):
    """律动天王: 7日/周线26K → mid-term swing (30% BOX)."""
    return classify_rhythm(closes, dates, beta_threshold=0.004, box_amp_min=10.0, box_amp_max=150.0)


def rotation_king_biweekly(closes, dates=None):
    """轮动天王: 双周线30K → rotation entry (13% BOX, 3x entries vs monthly)."""
    return classify_rhythm(closes, dates, beta_threshold=0.004, box_amp_min=8.0, box_amp_max=200.0)

# Backward compat
classify_weekly_rhythm = rhythm_king_weekly
