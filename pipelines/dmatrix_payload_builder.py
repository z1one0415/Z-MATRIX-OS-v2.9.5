"""D-Matrix v2.2 payload builder — single source for G07/G10/G14

Provides CRITICAL flat fields at top level (trade_date/close/volume/turnover/sector)
that D-Matrix scorer's assess_coverage() expects, NOT nested inside market dict.
"""
from __future__ import annotations
from datetime import datetime


def build_dmatrix_payload(ticker: str, name: str, kl: dict,
                          sector: str = "", theme: dict | None = None) -> dict:
    prices = kl.get("prices", [])
    volumes = kl.get("volume", [])
    closes = kl.get("close", prices)
    dates = kl.get("dates", [])

    # Critical flat fields (assess_coverage reads payload.get("close") not payload["market"]["close"])
    last_close = closes[-1] if closes else (prices[-1] if prices else 0)
    last_volume = volumes[-1] if volumes else 0
    avg_vol_20 = sum(volumes[-20:]) / max(len(volumes[-20:]), 1) if volumes else 1
    turnover = round(last_volume / max(avg_vol_20, 1), 2) if avg_vol_20 > 0 else 1.0
    trade_date = dates[-1] if dates else datetime.now().strftime("%Y-%m-%d")

    # Enrich sector from chain taxonomy
    if not sector:
        try:
            from pipelines.chain_taxonomy_provider import match_chain
            chain = match_chain(ticker, name, "")
            if chain:
                sector = chain
        except Exception:
            pass

    return {
        # Critical flat fields (D-Matrix assess_coverage uses payload.get())
        "code": ticker,
        "name": name or "",
        "sector": sector or "",
        "trade_date": trade_date,
        "close": last_close,
        "volume": last_volume,
        "turnover": turnover,
        # Core flat fields
        "float_market_cap_billion": 0,  # not available from Z-G01
        "overhead_pressure_pct": 0,
        "volatility_compression_pct": round(_compute_vol_compression(prices), 2) if len(prices) >= 20 else 0,
        "limit_up_count_120d": 0,
        "distance_to_platform_breakout_pct": 0,
        "turnover_memory_score": 0,
        "sector_breadth": 0,
        "leader_strength": 0,
        # Enhancement fields
        "theme": theme or {},
        "theme_seed": theme or {},
        "smart_money_preload": {},
        "micro_absorption": {},
        # Nested data for submodules
        "prices": prices,
        "market": {
            "dates": dates,
            "open": kl.get("open", []),
            "high": kl.get("high", []),
            "low": kl.get("low", []),
            "close": closes,
            "volume": volumes,
            "amount": kl.get("amount", []),
            "prices": prices,
            "data_contract": kl.get("data_contract", ""),
        },
        "silent_accumulation": {"prices": prices, "volume": volumes, "amount": kl.get("amount", [])},
        "micro_absorption": {"prices": prices, "volume": volumes, "amount": kl.get("amount", [])},
        "volume_price_preload": {"prices": prices, "volume": volumes, "amount": kl.get("amount", [])},
    }


def _compute_vol_compression(prices: list[float]) -> float:
    """Volatility compression: recent 5d std / 20d std. Lower = compressing."""
    if len(prices) < 25:
        return 0
    import statistics
    recent = statistics.stdev(prices[-5:]) / max(abs(sum(prices[-5:]) / 5), 0.01)
    long = statistics.stdev(prices[-20:]) / max(abs(sum(prices[-20:]) / 20), 0.01)
    return round(recent / max(long, 0.0001), 3)
