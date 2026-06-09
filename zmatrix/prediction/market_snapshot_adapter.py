"""Market Snapshot Adapter — assembles MarketSnapshot from G18 pipeline data.

Responsibility: field mapping + safe defaults.
No external API calls. No trade actions. No alpha claims.

Design principle:
  - Available fields (close, high, volume, avg_volume_20d) are extracted from
    prediction context and kline_data.
  - G09-related fields (d1_support, cycle_origin) come from g09_signal if available.
  - user_cost_line comes from position_data if provided.
  - event_window_active comes from event_calendar if provided.
  - Safe default policy: if a field is unavailable, it defaults to a value that
    does NOT trigger the corresponding risk gate (conservative = don't block
    without evidence).
"""
from __future__ import annotations

from zmatrix.prediction.fast_risk_overlay import MarketSnapshot


def build_market_snapshot(
    prediction,  # PredictionResult
    kline_data: dict,
    g09_signal: dict | None = None,
    position_data: dict | None = None,
    event_calendar: dict | None = None,
) -> MarketSnapshot:
    """Assemble MarketSnapshot from available pipeline data.

    Safe defaults: if a field is unavailable, it defaults to a value that
    does NOT trigger the risk gate (conservative = don't block without evidence).

    Exception: if close/high/volume are clearly available from kline, use them.
    """
    g09 = g09_signal or {}
    pos = position_data or {}
    evt = event_calendar or {}

    # ── Price fields from kline ──
    closes = kline_data.get("close", [])
    highs = kline_data.get("high", [])
    volumes = kline_data.get("volume", [])

    close = closes[-1] if closes else None
    high = highs[-1] if highs else None
    volume = volumes[-1] if volumes else None

    # avg_volume_20d: mean of last 20 volume bars (default 1.0 to avoid div-by-zero)
    if volumes and len(volumes) >= 20:
        avg_volume_20d = sum(volumes[-20:]) / 20.0
    elif volumes and len(volumes) >= 5:
        avg_volume_20d = sum(volumes[-len(volumes):]) / len(volumes)
    else:
        avg_volume_20d = None  # None = gate won't fire

    # ── G09 cycle fields ──
    d1_support = g09.get("d1_support") if g09.get("available") else None
    cycle_origin = g09.get("cycle_origin") if g09.get("available") else None

    # ── Position data ──
    user_cost_line = pos.get("cost_line") or pos.get("avg_cost") if pos else None

    # ── Event calendar ──
    event_window_active = bool(evt.get("event_window_active", False))

    # ── Sector / style / catalyst (future wire — safe defaults) ──
    sector_momentum_rank_current = None  # None = gate won't fire
    sector_momentum_rank_prior = None
    style_mismatch_duration_days = 0  # 0 < 5, so R9 won't fire
    days_since_catalyst = None  # None = gate won't fire

    return MarketSnapshot(
        close=close,
        high=high,
        volume=volume,
        avg_volume_20d=avg_volume_20d,
        user_cost_line=user_cost_line,
        d1_support=d1_support,
        cycle_origin=cycle_origin,
        event_window_active=event_window_active,
        event_confirmation_received=False,
        sector_momentum_rank_current=sector_momentum_rank_current,
        sector_momentum_rank_prior=sector_momentum_rank_prior,
        style_mismatch_duration_days=style_mismatch_duration_days,
        days_since_catalyst=days_since_catalyst,
    )
