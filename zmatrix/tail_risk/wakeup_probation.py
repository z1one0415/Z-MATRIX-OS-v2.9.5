"""WAKEUP_PROBATION — allow limited actions after HIBERNATE recovery"""
from __future__ import annotations
import hashlib

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY


def evaluate_wakeup_probation(*, market_signals: dict, previous_state: str = "NORMAL") -> dict:
    hgpr = market_signals.get("hard_gate_pass_rate", 0.0)
    mbpr = market_signals.get("market_breadth_pass_rate", 0.0)
    triggered = previous_state == "HIBERNATE" and hgpr >= 0.03 and mbpr >= 0.03

    if not triggered:
        return {
            "gate_id": "0"*32, "gate_type": "WAKEUP_PROBATION",
            "state": "NORMAL", "decision": "ALLOW", "action_downgrade": "NO_ACTION",
            "reason": f"prev={previous_state} hgpr={hgpr:.4f} mbpr={mbpr:.4f}",
            "evidence": {"previous_state": previous_state, "hard_gate_pass_rate": hgpr},
            "affected_roles": [], "affected_tickers": [],
            "freeze_new_entries": False,
            "allow_existing_position_review": True, "requires_human_review": False,
            "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
        }

    seed = f"WAKEUP_PROBATION|{hgpr}|{mbpr}"
    gid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "gate_id": gid, "gate_type": "WAKEUP_PROBATION",
        "state": "WAKEUP_PROBATION", "decision": "DOWNGRADE",
        "action_downgrade": "ENTER_TO_WAIT",
        "reason": f"recovered hgpr={hgpr:.4f} mbpr={mbpr:.4f}",
        "evidence": {"previous_state": previous_state, "hard_gate_pass_rate": hgpr},
        "affected_roles": ["B_MID_ROTATION"],
        "affected_tickers": [],
        "freeze_new_entries": False, "allow_existing_position_review": True,
        "max_role_allowed": "B_MID_ROTATION",
        "d_matrix_allowed": False,
        "requires_human_review": True,
        "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
