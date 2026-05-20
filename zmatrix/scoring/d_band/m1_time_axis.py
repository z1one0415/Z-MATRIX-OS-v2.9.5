from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

import pandas as pd

BarLabelPolicy = Literal["bar_start", "bar_end"]


@dataclass(frozen=True, slots=True)
class AShareM1AxisConfig:
    """A-share M1 axis configuration.

    Different data sources label the same one-minute bar differently.
    Some use the bar start time, some use the bar end time.  The feature layer
    must know this policy before slicing intervals such as 14:30-15:00.
    """

    bar_label_policy: BarLabelPolicy = "bar_end"
    expected_bar_count: int = 240
    allow_missing_minutes: int = 3
    fatal_missing_minutes: int = 10


def _normalize_trade_date(trade_date: str | date | datetime | None) -> pd.Timestamp:
    if trade_date is None:
        return pd.Timestamp("2000-01-01")
    return pd.Timestamp(trade_date).normalize()


def generate_a_share_minute_index(
    trade_date: str | date | datetime | None = None,
    config: AShareM1AxisConfig | None = None,
) -> pd.DatetimeIndex:
    """Generate the 240-bar A-share M1 standard axis.

    bar_end default:
      09:31-11:30 and 13:01-15:00
    bar_start:
      09:30-11:29 and 13:00-14:59
    """

    config = config or AShareM1AxisConfig()
    day = _normalize_trade_date(trade_date)
    if config.bar_label_policy == "bar_end":
        morning = pd.date_range(day + pd.Timedelta(hours=9, minutes=31), day + pd.Timedelta(hours=11, minutes=30), freq="min")
        afternoon = pd.date_range(day + pd.Timedelta(hours=13, minutes=1), day + pd.Timedelta(hours=15), freq="min")
    elif config.bar_label_policy == "bar_start":
        morning = pd.date_range(day + pd.Timedelta(hours=9, minutes=30), day + pd.Timedelta(hours=11, minutes=29), freq="min")
        afternoon = pd.date_range(day + pd.Timedelta(hours=13), day + pd.Timedelta(hours=14, minutes=59), freq="min")
    else:  # defensive; type checker should prevent this.
        raise ValueError(f"Unsupported bar_label_policy: {config.bar_label_policy}")
    idx = morning.append(afternoon)
    if len(idx) != config.expected_bar_count:
        raise RuntimeError(f"A-share M1 axis expected {config.expected_bar_count}, got {len(idx)}")
    return idx


def coerce_m1_datetime_index(df: pd.DataFrame, trade_date: str | date | datetime | None = None) -> pd.DataFrame:
    """Return a copy indexed by datetime.

    Accepts either an existing DatetimeIndex or a `minute` column containing HH:MM
    or datetime-like strings.  HH:MM is anchored to `trade_date`.
    """

    out = df.copy()
    if isinstance(out.index, pd.DatetimeIndex):
        return out.sort_index()
    if "minute" not in out.columns:
        raise ValueError("M1 dataframe requires DatetimeIndex or `minute` column")
    day = _normalize_trade_date(trade_date)
    def parse(v):
        s = str(v)
        if len(s) <= 5 and ":" in s:
            hh, mm = map(int, s.split(":")[:2])
            return day + pd.Timedelta(hours=hh, minutes=mm)
        return pd.Timestamp(s)
    out.index = pd.DatetimeIndex([parse(v) for v in out["minute"]])
    return out.sort_index()
