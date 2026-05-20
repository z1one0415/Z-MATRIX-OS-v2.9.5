from __future__ import annotations

import pandas as pd

from .m1_data_contracts import M1DataQuality, M1Usability
from .m1_time_axis import AShareM1AxisConfig, coerce_m1_datetime_index, generate_a_share_minute_index

REQUIRED_M1_COLUMNS = {"open", "high", "low", "close", "volume"}


def validate_raw_m1_frame(df: pd.DataFrame) -> list[str]:
    missing = REQUIRED_M1_COLUMNS.difference(df.columns)
    warnings: list[str] = []
    if missing:
        warnings.append(f"missing_required_columns:{sorted(missing)}")
    if len(df) == 0:
        warnings.append("empty_m1_frame")
    return warnings


def assess_m1_quality(aligned_df: pd.DataFrame, config: AShareM1AxisConfig | None = None) -> M1DataQuality:
    config = config or AShareM1AxisConfig()
    synthetic = int(aligned_df.get("is_synthetic_bar", pd.Series(False, index=aligned_df.index)).sum())
    actual = int(config.expected_bar_count - synthetic)
    missing = synthetic
    tail = aligned_df.between_time("14:30", "15:00")
    missing_tail = int(tail.get("is_synthetic_bar", pd.Series(False, index=tail.index)).sum())
    warnings: list[str] = []
    if missing > config.fatal_missing_minutes:
        usability = M1Usability.UNUSABLE
        warnings.append("fatal_missing_minutes_exceeded")
    elif missing > config.allow_missing_minutes or missing_tail > config.allow_missing_minutes:
        usability = M1Usability.DEGRADED
        warnings.append("m1_missing_minutes_degraded")
    else:
        usability = M1Usability.USABLE
    return M1DataQuality(
        usability=usability,
        expected_bars=config.expected_bar_count,
        actual_bars=actual,
        missing_minutes=missing,
        synthetic_bars=synthetic,
        missing_tail_minutes=missing_tail,
        warnings=warnings,
    )


def align_and_fill_m1(
    m1_df: pd.DataFrame,
    trade_date: str | None = None,
    config: AShareM1AxisConfig | None = None,
) -> pd.DataFrame:
    """Align M1 bars to the standard A-share axis and mark synthetic bars.

    Price fields are forward-filled to preserve a continuous state path.
    Volume/turnover are filled with 0 because synthetic bars are not real trades.
    Synthetic bars are never allowed to become real absorption evidence.
    """

    config = config or AShareM1AxisConfig()
    warnings = validate_raw_m1_frame(m1_df)
    if warnings and any(w.startswith("missing_required_columns") or w == "empty_m1_frame" for w in warnings):
        raise ValueError("invalid_m1_frame:" + ",".join(warnings))
    raw = coerce_m1_datetime_index(m1_df, trade_date=trade_date)
    axis = generate_a_share_minute_index(trade_date=trade_date, config=config)
    aligned = raw.reindex(axis)
    aligned["is_synthetic_bar"] = aligned["close"].isna()
    for col in ["close", "open", "high", "low", "vwap"]:
        if col in aligned.columns:
            aligned[col] = aligned[col].ffill()
    # If the first bar is missing and cannot ffill, backfill only price state; it remains synthetic.
    for col in ["close", "open", "high", "low", "vwap"]:
        if col in aligned.columns:
            aligned[col] = aligned[col].bfill()
    aligned["volume"] = aligned["volume"].fillna(0.0)
    if "turnover" not in aligned.columns:
        aligned["turnover"] = aligned["close"] * aligned["volume"]
    aligned["turnover"] = aligned["turnover"].fillna(0.0)
    return aligned
