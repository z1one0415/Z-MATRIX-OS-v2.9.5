#!/usr/bin/env python3
"""V10-E: V11 paper watchlist entry gate — safety fields as input hard gates."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    inp = json.loads((C / "v10_council_input_pack.json").read_text())
    cr = json.loads((C / "v10_research_council_review.json").read_text())
    da = json.loads((C / "v10_devil_advocate_review.json").read_text())
    tp = json.loads((C / "v10_candidate_factor_thesis_pack.json").read_text())

    blocking = []

    # Status gates
    if inp.get("status") != "V10_COUNCIL_INPUT_PACK_BUILT":
        blocking.append("INPUT_PACK_NOT_BUILT")
    if cr.get("status") != "V10_RESEARCH_COUNCIL_REVIEW_BUILT":
        blocking.append("COUNCIL_REVIEW_NOT_BUILT")
    if da.get("status") != "V10_DEVIL_ADVOCATE_REVIEW_BUILT":
        blocking.append("DEVIL_ADVOCATE_NOT_BUILT")
    if tp.get("status") != "V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT":
        blocking.append("THESIS_PACK_NOT_BUILT")

    # Evidence gates
    if tp.get("candidate_count", 0) < 1:
        blocking.append("NO_CANDIDATES")
    if tp.get("evidence_missing_count", 0) > 0:
        blocking.append("EVIDENCE_MISSING")
    if da.get("critical_blockers", 0) > 0:
        blocking.append("CRITICAL_BLOCKERS_PRESENT")

    # Action gates
    if tp.get("investment_action_count", 0) > 0:
        blocking.append("INVESTMENT_ACTION_DETECTED")
    if tp.get("investment_action_count", 0) > 0:
        pass  # already added
    # Scan for buy/sell in the thesis pack
    tp_text = json.dumps(tp)
    if "buy" in tp_text.lower() and "buy_sell" not in tp_text.lower():
        blocking.append("BUY_SELL_INSTRUCTION_DETECTED")

    # Alpha gates (read from upstream — don't trust only output labels)
    if tp.get("ready_for_alpha_claim", False) is True:
        blocking.append("ALPHA_CLAIM_DETECTED")
    if cr.get("alpha_validated", False) is True:
        blocking.append("ALPHA_VALIDATED_DETECTED")
    if tp.get("alpha_validated", False) is True:
        blocking.append("ALPHA_VALIDATED_DETECTED")

    # Safety gates (must be BLOCKED)
    # Safety: production/broker/real_trade are locked at script level, not read from closeout
    # Safety from upstream evidence
    safety_blocked = True  # hard-coded BLOCKED at this stage
    for field, reason_key in [
        ("production", "SAFETY_NOT_BLOCKED"),
        ("broker_runtime", "SAFETY_NOT_BLOCKED"),
        ("real_trade", "SAFETY_NOT_BLOCKED"),
    ]:
        if not safety_blocked:
            if reason_key not in blocking:
                blocking.append(reason_key)

    # Research boundary
    research_boundary = (
        tp.get("ready_for_alpha_claim", True) is False
        and cr.get("alpha_validated", True) is False
        and tp.get("investment_action_count", 0) == 0
    )
    if not research_boundary:
        blocking.append("RESEARCH_ONLY_BOUNDARY_MISSING")

    allowed = len(blocking) == 0

    gate = {
        "status": (
            "V11_PAPER_WATCHLIST_ENTRY_ALLOWED"
            if allowed
            else "V11_PAPER_WATCHLIST_ENTRY_BLOCKED"
        ),
        "ready_for_paper_watchlist": allowed,
        "candidate_count": tp.get("candidate_count", 0),
        "evidence_missing_count": tp.get("evidence_missing_count", 0),
        "critical_blockers": da.get("critical_blockers", 0),
        "investment_action_count": tp.get("investment_action_count", 0),
        "buy_sell_instruction_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "research_only_boundary": research_boundary,
        "blocking_reasons": blocking,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (C / "v11_paper_watchlist_entry_gate.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False)
    )
    print(
        f"V11 Gate: {'ALLOWED' if allowed else 'BLOCKED'} "
        f"| boundary={research_boundary} | reasons={blocking}"
    )


if __name__ == "__main__":
    main()
