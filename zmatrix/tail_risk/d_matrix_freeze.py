"""D_MATRIX_FREEZE — freeze D-Matrix new entries under stress"""
from __future__ import annotations
import hashlib

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY


def evaluate_d_matrix_freeze(*, candidate_context: dict, market_signals: dict) -> dict:
    role = candidate_context.get("role", "")
    sector_heat = market_signals.get("sector_heat_status", "")
    triggered = (
        role == "D_BLACK_HORSE" and sector_heat in ("RETREAT", "CLIMAX", "CRASH")
    )

    if not triggered:
        return {
            "gate_id": "0"*32, "gate_type": "D_MATRIX_FREEZE",
            "state": "NORMAL", "decision": "ALLOW", "action_downgrade": "NO_ACTION",
            "reason": f"role={role} heat={sector_heat}", "evidence": {},
            "affected_roles": [], "affected_tickers": [],
            "freeze_new_entries": False, "allow_existing_position_review": True,
            "requires_human_review": False, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
        }

    seed = f"D_MATRIX_FREEZE|{role}|{sector_heat}"
    gid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "gate_id": gid, "gate_type": "D_MATRIX_FREEZE",
        "state": "STRESS", "decision": "FREEZE",
        "action_downgrade": "REVIEW_TO_FREEZE",
        "reason": f"role={role} sector_heat={sector_heat}",
        "evidence": {"role": role, "sector_heat": sector_heat},
        "affected_roles": ["D_BLACK_HORSE"], "affected_tickers": [],
        "freeze_new_entries": True, "allow_existing_position_review": True,
        "candidate_action_allowed": False, "fallback_action": "WATCH_ONLY",
        "requires_human_review": True, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
