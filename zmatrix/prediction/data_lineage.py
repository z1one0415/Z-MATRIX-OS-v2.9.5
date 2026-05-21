"""Data lineage cap — INV-TG18-02 + INV-TG18-07

Any factor with DAILY_OHLCV_PROXY/PROXY/M1_NOT_CONNECTED/L2_NOT_CONNECTED
→ confidence_cap ≤ MEDIUM, probability_cap ≤ 0.75.
DATA_GAP → LOW, probability_cap ≤ 0.60.
Missing lineage entirely → DEGRADED_MISSING_LINEAGE, LOW, 0.60.
"""
from __future__ import annotations

PROXY_KEYWORDS = {"DAILY_OHLCV_PROXY", "PROXY", "M1_NOT_CONNECTED", "L2_NOT_CONNECTED",
                  "NOT_CONNECTED", "UNKNOWN_PROXY", "DEGRADED_MISSING_LINEAGE"}

DEFAULT_DEGRADED_PROXY = {
    "market_data": "UNKNOWN_PROXY",
    "intraday": "NOT_CONNECTED",
    "m1": False,
    "l2": False,
    "source": ["UNKNOWN"],
    "upstream_status": "DEGRADED_MISSING_LINEAGE",
    "trust": "LOW",
}


def evaluate_lineage(lineage: dict | None) -> dict:
    """INV-TG18-07: if no lineage provided, use degraded defaults.

    Returns {confidence_cap, probability_cap, trust, upstream_status}.
    """
    if lineage is None:
        lineage = DEFAULT_DEGRADED_PROXY

    has_proxy = any(
        str(lineage.get(k, "")).upper() in PROXY_KEYWORDS or
        any(kw in str(lineage.get(k, "")) for kw in PROXY_KEYWORDS)
        for k in ("market_data", "intraday", "upstream_status")
    )

    is_data_gap = "DATA_GAP" in str(lineage.get("upstream_status", ""))
    is_unknown = lineage.get("trust", "") == "LOW" or "UNKNOWN" in str(lineage.get("source", ""))

    if is_data_gap or is_unknown:
        return {
            "confidence_cap": "LOW",
            "probability_cap": 0.60,
            "trust": "LOW",
            "upstream_status": lineage.get("upstream_status", "DEGRADED_LINEAGE"),
            "reason": "data_gap_or_unknown_source",
        }
    elif has_proxy:
        return {
            "confidence_cap": "MEDIUM",
            "probability_cap": 0.75,
            "trust": "MEDIUM",
            "upstream_status": lineage.get("upstream_status", "PROXY"),
            "reason": "proxy_data_detected",
        }
    else:
        return {
            "confidence_cap": "HIGH",
            "probability_cap": 0.95,
            "trust": "HIGH",
            "upstream_status": lineage.get("upstream_status", "PASS"),
            "reason": "clean_lineage",
        }


def apply_lineage_cap(probability: float, lineage_result: dict) -> float:
    """INV-TG18-02: hard cap based on lineage evaluation."""
    return round(min(probability, lineage_result["probability_cap"]), 4)
