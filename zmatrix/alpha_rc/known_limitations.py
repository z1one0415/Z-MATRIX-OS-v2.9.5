"""Known Limitations — operator warnings and non-goals"""
from __future__ import annotations

from zmatrix.alpha_rc.schemas import DEFAULT_ALPHA_RC_SAFETY

_LIMITATIONS = [
    "Not a live trading system.",
    "No broker connection.",
    "No real order execution.",
    "No automatic buy/sell/close.",
    "No Hermes long-term memory write.",
    "No real Z9 write.",
    "No automatic calibration.",
    "No prompt auto-injection.",
    "No runtime prompt injection.",
    "No real market API enabled by default.",
    "Dry-run uses sample inputs only.",
    "READY_FOR_ALPHA only means alpha rehearsal eligibility.",
]

_NON_GOALS = [
    "Real-time market data streaming.",
    "Automated trade execution.",
    "Portfolio rebalancing.",
    "Risk parity optimization.",
    "Machine learning model training.",
]

_OPERATOR_WARNINGS = [
    "Do not connect broker.",
    "Do not enable runtime.",
    "Do not write Hermes memory.",
    "Do not write Z9.",
    "Do not auto-calibrate.",
    "Do not inject Prompt.",
    "Do not place real orders.",
    "Release candidate does not represent production readiness.",
]


def build_v3_alpha_known_limitations() -> dict:
    return {
        "limitations_version": "V3_ALPHA_KNOWN_LIMITATIONS_V10",
        "limitations": list(_LIMITATIONS),
        "non_goals": list(_NON_GOALS),
        "operator_warnings": list(_OPERATOR_WARNINGS),
    }
