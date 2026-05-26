"""HIBERNATE_MODE — freeze offensive recommendations when pass rate is critically low"""
from __future__ import annotations
import hashlib

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY


def evaluate_hibernate_mode(*, market_signals: dict) -> dict:
    hgpr = market_signals.get("hard_gate_pass_rate", 1.0)
    mbpr = market_signals.get("market_breadth_pass_rate", 1.0)
    triggered = hgpr < 0.01 or mbpr < 0.01

    if not triggered:
        return {
            "gate_id": "0"*32, "gate_type": "HIBERNATE_MODE",
            "state": "NORMAL", "decision": "ALLOW", "action_downgrade": "NO_ACTION",
            "reason": f"hgpr={hgpr:.4f} mbpr={mbpr:.4f}",
            "evidence": {"hard_gate_pass_rate": hgpr, "market_breadth_pass_rate": mbpr},
            "affected_roles": [], "freeze_new_entries": False,
            "allow_existing_position_review": True, "requires_human_review": False,
            "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
        }

    seed = f"HIBERNATE_MODE|{hgpr}|{mbpr}"
    gid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "gate_id": gid, "gate_type": "HIBERNATE_MODE",
        "state": "HIBERNATE", "decision": "HIBERNATE",
        "action_downgrade": "FREEZE_TO_HIBERNATE",
        "reason": f"hard_gate_pass_rate={hgpr:.4f} breadth={mbpr:.4f}",
        "evidence": {"hard_gate_pass_rate": hgpr, "market_breadth_pass_rate": mbpr},
        "affected_roles": ["B_MID_ROTATION", "C_SHORT_EVENT", "D_BLACK_HORSE"],
        "freeze_new_entries": True, "allow_existing_position_review": True,
        "requires_human_review": True, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
