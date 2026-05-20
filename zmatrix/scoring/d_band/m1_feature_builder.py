from __future__ import annotations

import math

import pandas as pd

from .m1_data_contracts import M1FeaturePack
from .m1_data_quality import align_and_fill_m1, assess_m1_quality
from .m1_time_axis import AShareM1AxisConfig


def _safe_pct(a: float, b: float) -> float:
    if b == 0 or math.isnan(b):
        return 0.0
    return (a / b - 1.0) * 100.0


def build_m1_feature_pack(
    m1_df: pd.DataFrame,
    trade_date: str | None = None,
    config: AShareM1AxisConfig | None = None,
) -> M1FeaturePack:
    config = config or AShareM1AxisConfig()
    aligned = align_and_fill_m1(m1_df, trade_date=trade_date, config=config)
    quality = assess_m1_quality(aligned, config=config)

    first_close = float(aligned["close"].iloc[0])
    last_close = float(aligned["close"].iloc[-1])
    total_gain = _safe_pct(last_close, first_close)

    late = aligned.between_time("14:30", "15:00")
    if len(late) == 0:
        late_gain = 0.0
        late_turnover = 0.0
    else:
        late_gain = _safe_pct(float(late["close"].iloc[-1]), float(late["close"].iloc[0]))
        late_turnover = float(late["turnover"].sum())
    total_turnover = float(aligned["turnover"].sum())
    contribution = 0.0
    if abs(total_gain) > 1e-9 and late_gain > 0 and total_gain > 0:
        contribution = min(9.99, max(0.0, late_gain / total_gain))
    high = float(aligned["high"].max())
    low = float(aligned["low"].min())
    close_position = 50.0 if high <= low else (last_close - low) / (high - low) * 100.0
    warnings = []
    if quality.usability.value != "USABLE":
        warnings.extend(quality.warnings)
    return M1FeaturePack(
        total_gain_pct=round(total_gain, 4),
        late_day_gain_pct=round(late_gain, 4),
        late_day_gain_contribution=round(contribution, 4),
        total_turnover=round(total_turnover, 2),
        late_day_turnover=round(late_turnover, 2),
        late_day_turnover_share=round(0.0 if total_turnover == 0 else late_turnover / total_turnover, 4),
        close_position_pct=round(close_position, 2),
        data_quality=quality,
        warnings=warnings,
    )
