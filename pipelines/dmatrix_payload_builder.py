"""D-Matrix v2.2 payload builder — single source for G07/G10/G14"""
from __future__ import annotations


def build_dmatrix_payload(ticker: str, name: str, kl: dict,
                          sector: str = "", theme: dict | None = None) -> dict:
    """Build OHLCV-enriched D-Matrix payload from Z-G01 get_kline output.

    All D-Matrix consumers (G07 gate7, G10 _d_matrix_score, G14 _real_d_score)
    must use this builder to ensure consistent input across entry points.
    """
    prices = kl.get("prices", [])
    return {
        "code": ticker,
        "name": name or "",
        "sector": sector or "",
        "theme": theme or {},
        "prices": prices,
        "market": {
            "dates": kl.get("dates", []),
            "open": kl.get("open", []),
            "high": kl.get("high", []),
            "low": kl.get("low", []),
            "close": kl.get("close", prices),
            "volume": kl.get("volume", []),
            "amount": kl.get("amount", []),
            "prices": prices,
            "data_contract": kl.get("data_contract", ""),
        },
        "silent_accumulation": {
            "prices": prices,
            "volume": kl.get("volume", []),
            "amount": kl.get("amount", []),
        },
        "micro_absorption": {
            "prices": prices,
            "volume": kl.get("volume", []),
            "amount": kl.get("amount", []),
        },
        "volume_price_preload": {
            "prices": prices,
            "volume": kl.get("volume", []),
            "amount": kl.get("amount", []),
        },
    }
