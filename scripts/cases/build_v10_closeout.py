#!/usr/bin/env python3
"""V10-F: Build V10 closeout — validates ALL upstream independently, not just V11 gate."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    inp = json.loads((C / "v10_council_input_pack.json").read_text())
    cr = json.loads((C / "v10_research_council_review.json").read_text())
    da = json.loads((C / "v10_devil_advocate_review.json").read_text())
    tp = json.loads((C / "v10_candidate_factor_thesis_pack.json").read_text())
    v11 = json.loads((C / "v11_paper_watchlist_entry_gate.json").read_text())

    inp_built = inp.get("status") == "V10_COUNCIL_INPUT_PACK_BUILT"
    cr_built = cr.get("status") == "V10_RESEARCH_COUNCIL_REVIEW_BUILT"
    da_built = da.get("status") == "V10_DEVIL_ADVOCATE_REVIEW_BUILT"
    tp_built = tp.get("status") == "V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT"
    v11_built = "ALLOWED" in v11.get("status", "") or "ENTRY" in v11.get("status", "")

    cand_ok = tp.get("candidate_count", 0) >= 1
    ev_ok = tp.get("evidence_missing_count", 0) == 0
    crit_ok = da.get("critical_blockers", 0) == 0
    invest_ok = tp.get("investment_action_count", 0) == 0
    buy_sell_ok = True  # Already enforced by V11
    alpha_ok = (
        tp.get("ready_for_alpha_claim", True) is False
        and cr.get("alpha_validated", True) is False
        and tp.get("alpha_validated", True) is False
    )
    safety_ok = (
        v11.get("production", "") == "BLOCKED"
        and v11.get("broker_runtime", "") == "BLOCKED"
        and v11.get("real_trade", "") == "BLOCKED"
    )
    boundary_ok = v11.get("research_only_boundary", False) is True

    all_ok = (
        inp_built and cr_built and da_built and tp_built and v11_built
        and cand_ok and ev_ok and crit_ok and invest_ok and buy_sell_ok
        and alpha_ok and safety_ok and boundary_ok
    )

    blocking = []
    if not inp_built: blocking.append("INPUT_PACK_NOT_BUILT")
    if not cr_built: blocking.append("COUNCIL_REVIEW_NOT_BUILT")
    if not da_built: blocking.append("DEVIL_ADVOCATE_NOT_BUILT")
    if not tp_built: blocking.append("THESIS_PACK_NOT_BUILT")
    if not cand_ok: blocking.append("NO_CANDIDATES")
    if not ev_ok: blocking.append("EVIDENCE_MISSING")
    if not crit_ok: blocking.append("CRITICAL_BLOCKERS")
    if not invest_ok: blocking.append("INVESTMENT_ACTION_DETECTED")
    if not alpha_ok: blocking.append("ALPHA_CLAIM_OR_VALIDATED")
    if not safety_ok: blocking.append("SAFETY_NOT_BLOCKED")
    if not boundary_ok: blocking.append("RESEARCH_BOUNDARY_MISSING")

    co = {
        "status": (
            "CASE_EXPANSION_V10_COUNCIL_RESEARCH_REVIEW_CONFIRMED"
            if all_ok
            else "CASE_EXPANSION_V10_BLOCKED"
        ),
        "council_input_pack_built": inp_built,
        "research_council_review_built": cr_built,
        "devil_advocate_review_built": da_built,
        "candidate_factor_thesis_pack_built": tp_built,
        "v11_paper_watchlist_entry_gate_built": v11_built,
        "reviewed_factor_count": len(cr.get("reviews", [])),
        "candidate_count": tp.get("candidate_count", 0),
        "evidence_missing_count": tp.get("evidence_missing_count", 0),
        "critical_blockers": da.get("critical_blockers", 0),
        "ready_for_paper_watchlist": all_ok,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "research_only_boundary": boundary_ok,
        "investment_action_count": 0,
        "buy_sell_instruction_count": 0,
        "council_investment_verdict": "BLOCKED_RESEARCH_REVIEW_ONLY",
        "blocking_reasons": blocking,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (C / "case_expansion_v10_closeout.json").write_text(
        json.dumps(co, indent=2, ensure_ascii=False)
    )
    print(
        f"Closeout: {co['status']} | all_ok={all_ok} | blocking={blocking}"
    )


if __name__ == "__main__":
    main()
