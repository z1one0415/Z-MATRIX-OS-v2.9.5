"""Market Signals — normalize raw external signals (no network, no real fetch)"""
from __future__ import annotations

SIGNAL_VERSION = "TAIL_RISK_SIGNAL_V10"


def normalize_market_signals(raw: dict) -> dict:
    """Normalize raw market signals.

    Takes external/local snapshot input only.
    Does NOT network fetch. Does NOT use external API.
    """
    mbpr = raw.get("market_breadth_pass_rate", 0.0)
    hgpr = raw.get("hard_gate_pass_rate", 0.0)
    ldn = raw.get("limit_down_count", 0)
    lun = raw.get("limit_up_count", 0)
    scs = raw.get("small_cap_liquidity_score", 0.0)
    lcs = raw.get("large_cap_liquidity_score", 0.0)
    lsc = scs / max(lcs, 0.01)
    if lsc > 1.0:
        lsc = 1.0 - (lsc - 1.0)
    # When both scores are 0 (default/unknown), scissor should be 0 (no stress detected)
    if scs == 0.0 and lcs == 0.0:
        lsc = 1.0

    return {
        "signal_version": SIGNAL_VERSION,
        "market_breadth_pass_rate": mbpr,
        "hard_gate_pass_rate": hgpr,
        "limit_down_count": ldn,
        "limit_up_count": lun,
        "liquidity_scissor": round(1.0 - lsc, 4),
        "small_cap_liquidity_score": scs,
        "large_cap_liquidity_score": lcs,
        "index_drawdown_5d": raw.get("index_drawdown_5d", 0.0),
        "sector_heat_status": raw.get("sector_heat_status", "UNKNOWN"),
        "derivative_basis_stress": raw.get("derivative_basis_stress", 0.0),
        "d_matrix_candidate_count": raw.get("d_matrix_candidate_count", 0),
        "external_api_used": False,
        "real_market_fetch_allowed": False,
    }
