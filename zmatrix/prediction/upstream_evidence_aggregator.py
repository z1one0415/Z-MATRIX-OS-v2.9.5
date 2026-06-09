"""G18 Upstream Evidence Aggregator v1.0 — assemble all pipeline evidence for final decision."""
from __future__ import annotations

# Default adapters for sources that are NOT_CONNECTED
_PLACEHOLDER = {"source": "...", "available": False, "reason": "NOT_CONNECTED", "warnings": ["..."]}

G08_DEFAULT = {"source": "Z-G08", "available": False, "reason": "NOT_CONNECTED", "warnings": ["G08_NOT_CONNECTED"]}
G11_DEFAULT = {"source": "Z-G11", "available": False, "risk_authority": "STRONG_WARNING_ONLY",
               "hard_veto_allowed": False, "warnings": []}
G14_DEFAULT = {"source": "Z-G14", "available": False, "role": "GLOBAL_BASELINE_ONLY",
               "not_duplicate_selection": True, "rank_bucket": None, "global_rank": None, "warnings": []}
Z16_DEFAULT = {"source": "Z16_PRICE_GATE", "available": False, "required": True,
               "status": "PLACEHOLDER_NOT_CONNECTED", "warnings": ["Z16_NOT_CONNECTED"]}
G17_DEFAULT = {"source": "G17_ACCOUNT_CONFIRMATION", "available": False, "required": True,
               "status": "PLACEHOLDER_NOT_CONNECTED", "warnings": ["G17_NOT_CONNECTED"]}
CAPITAL_FLOW_DEFAULT = {"source": "CAPITAL_FLOW_9WAY", "available": False,
                        "reason": "NOT_CONNECTED", "verdict": "unknown", "warnings": ["CAPITAL_FLOW_NOT_CONNECTED"]}
ALL_SOURCES = ["g09", "g08", "g11", "g14", "z16", "g17", "capital_flow"]


def build_upstream_evidence(
    ticker: str,
    *,
    g09_signal: dict | None = None,
    g08_signal: dict | None = None,
    g11_signal: dict | None = None,
    g14_signal: dict | None = None,
    z16_signal: dict | None = None,
    g17_signal: dict | None = None,
    capital_flow_signal: dict | None = None,
) -> dict:
    """Assemble all upstream pipeline evidence. Never raises, never blocks G18."""
    evidence = {}
    missing = []
    available = {}

    named = {
        "g09": (g09_signal, None),
        "g08": (g08_signal, G08_DEFAULT),
        "g11": (g11_signal, G11_DEFAULT),
        "g14": (g14_signal, G14_DEFAULT),
        "z16": (z16_signal, Z16_DEFAULT),
        "g17": (g17_signal, G17_DEFAULT),
        "capital_flow": (capital_flow_signal, CAPITAL_FLOW_DEFAULT),
    }

    for key, (sig, default) in named.items():
        if sig:
            is_avail = sig.get("available") is True or sig.get("status") in ("PASS", "DEGRADED")
        else:
            is_avail = False
        if is_avail:
            evidence[key] = sig
            available[key] = True
        elif default is not None:
            evidence[key] = default
            available[key] = False
            missing.append(key)
        else:
            evidence[key] = {"available": False, "source": "MISSING"}
            available[key] = False
            missing.append(key)

    return {
        "ticker": ticker,
        "evidence_version": "v1.1",
        "evidence_available": available,
        "missing_sources": missing,
        "warnings": [f"missing: {s}" for s in missing] if missing else [],
        "capital_flow_verdict": evidence.get("capital_flow", {}).get("verdict", "unknown"),
        **evidence,
    }
