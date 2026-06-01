#!/usr/bin/env python3
"""V10-F: Closeout — reads V11 gate + upstream audit, no hardcoded safety."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    inp = json.loads((C / "v10_council_input_pack.json").read_text())
    cr = json.loads((C / "v10_research_council_review.json").read_text())
    da = json.loads((C / "v10_devil_advocate_review.json").read_text())
    tp = json.loads((C / "v10_candidate_factor_thesis_pack.json").read_text())
    upstream = json.loads((C / "v10_upstream_safety_alpha_audit.json").read_text())
    v11 = json.loads((C / "v11_paper_watchlist_entry_gate.json").read_text())

    # Built status
    inp_b = inp.get("status") == "V10_COUNCIL_INPUT_PACK_BUILT"
    cr_b = cr.get("status") == "V10_RESEARCH_COUNCIL_REVIEW_BUILT"
    da_b = da.get("status") == "V10_DEVIL_ADVOCATE_REVIEW_BUILT"
    tp_b = tp.get("status") == "V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT"

    # V11
    v11_b = v11.get("status") in {
        "V11_PAPER_WATCHLIST_ENTRY_ALLOWED",
        "V11_PAPER_WATCHLIST_ENTRY_BLOCKED",
    }
    v11_a = (
        v11.get("status") == "V11_PAPER_WATCHLIST_ENTRY_ALLOWED"
        and v11.get("ready_for_paper_watchlist") is True
        and v11.get("blocking_reasons", ["X"]) == []
    )

    # Upstream audit
    up_ok = (
        upstream.get("status") == "V10_UPSTREAM_SAFETY_ALPHA_AUDIT_PASS"
        and upstream.get("ready_for_v11_gate") is True
        and upstream.get("safety_missing_fields", ["X"]) == []
        and upstream.get("safety_unblocked_fields", ["X"]) == []
        and upstream.get("alpha_missing_fields", ["X"]) == []
        and upstream.get("alpha_true_fields", ["X"]) == []
    )

    # V11 violation arrays
    safety_ok = up_ok and v11.get("safety_ok", False)
    alpha_ok = (
        len(v11.get("alpha_missing_fields", ["X"])) == 0
        and len(v11.get("alpha_true_fields", ["X"])) == 0
    )
    invest_ok = (
        v11.get("investment_action_count", 999) == 0
        and len(v11.get("investment_action_violations", ["X"])) == 0
    )
    bs_ok = (
        v11.get("buy_sell_instruction_count", 999) == 0
        and len(v11.get("forbidden_action_violations", ["X"])) == 0
    )
    boundary_ok = v11.get("research_only_boundary", False) is True

    # Independent
    cand_ok = tp.get("candidate_count", 0) >= 1
    ev_ok = tp.get("evidence_missing_count", 0) == 0
    crit_ok = da.get("critical_blockers", 0) == 0

    all_ok = (
        inp_b and cr_b and da_b and tp_b and v11_b and v11_a
        and up_ok and cand_ok and ev_ok and crit_ok
        and safety_ok and alpha_ok and invest_ok and bs_ok and boundary_ok
    )

    blocking = []
    if not inp_b: blocking.append("INPUT_PACK_NOT_BUILT")
    if not cr_b: blocking.append("COUNCIL_REVIEW_NOT_BUILT")
    if not da_b: blocking.append("DEVIL_ADVOCATE_NOT_BUILT")
    if not tp_b: blocking.append("THESIS_PACK_NOT_BUILT")
    if not v11_b: blocking.append("V11_GATE_NOT_BUILT")
    if not v11_a: blocking.append("V11_NOT_ALLOWED")
    if not up_ok: blocking.append("UPSTREAM_AUDIT_NOT_PASS")
    if not safety_ok: blocking.append("SAFETY_VIOLATION")
    if not alpha_ok: blocking.append("ALPHA_VIOLATION")
    if not invest_ok: blocking.append("INVESTMENT_ACTION")
    if not bs_ok: blocking.append("FORBIDDEN_ACTION")
    if not boundary_ok: blocking.append("RESEARCH_BOUNDARY_MISSING")

    co = {
        "status": (
            "CASE_EXPANSION_V10_COUNCIL_RESEARCH_REVIEW_CONFIRMED"
            if all_ok else "CASE_EXPANSION_V10_BLOCKED"
        ),
        "council_input_pack_built": inp_b,
        "research_council_review_built": cr_b,
        "devil_advocate_review_built": da_b,
        "candidate_factor_thesis_pack_built": tp_b,
        "v11_paper_watchlist_entry_gate_built": v11_b,
        "v11_paper_watchlist_entry_allowed": v11_a,
        "upstream_safety_alpha_audit_pass": up_ok,
        "reviewed_factor_count": len(cr.get("reviews", [])),
        "candidate_count": tp.get("candidate_count", 0),
        "evidence_missing_count": tp.get("evidence_missing_count", 0),
        "critical_blockers": da.get("critical_blockers", 0),
        "ready_for_paper_watchlist": all_ok,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "safety_ok": safety_ok,
        "safety_missing_fields": upstream.get("safety_missing_fields", []),
        "safety_unblocked_fields": upstream.get("safety_unblocked_fields", []),
        "alpha_missing_fields": upstream.get("alpha_missing_fields", []),
        "alpha_true_fields": upstream.get("alpha_true_fields", []),
        "investment_action_count": v11.get("investment_action_count", 0),
        "investment_action_violations": v11.get("investment_action_violations", []),
        "buy_sell_instruction_count": v11.get("buy_sell_instruction_count", 0),
        "forbidden_action_violations": v11.get("forbidden_action_violations", []),
        "research_only_boundary": boundary_ok,
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
        f"Closeout: {co['status']} | all_ok={all_ok} "
        f"| upstream_audit={up_ok} | v11_allowed={v11_a}"
    )


if __name__ == "__main__":
    main()
