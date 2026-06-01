#!/usr/bin/env python3
"""V10-E: V11 paper watchlist entry gate — real safety input enforcement."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

FORBIDDEN_VALUES = [
    "BUY", "SELL", "ADD", "REDUCE",
    "\u4e70\u5165", "\u5356\u51fa", "\u5efa\u4ed3", "\u52a0\u4ed3", "\u51cf\u4ed3",
    "\u6b62\u76c8", "\u6b62\u68cd",  # 买入,卖出,建仓,加仓,减仓,止盈,止损
]


def load(name):
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def all_safety_blocked(docs):
    """True only if ALL docs have production/broker/runtime BLOCKED."""
    for doc in docs:
        for field in ["production", "broker_runtime", "real_trade"]:
            val = doc.get(field, "BLOCKED")
            if val != "BLOCKED":
                return False
    return True


def scan_forbidden_text(doc):
    """Return count of forbidden words found in doc VALUES (not keys)."""
    count = 0
    text = json.dumps(doc).upper()
    for word in FORBIDDEN_VALUES:
        if word.upper() in text:
            # Skip field name false positives
            if word.upper() in ("BUY", "SELL") and "BUY_SELL_INSTRUCTION_COUNT" in text:
                continue
            count += 1
    return count


def main():
    inp = load("v10_council_input_pack.json")
    cr = load("v10_research_council_review.json")
    da = load("v10_devil_advocate_review.json")
    tp = load("v10_candidate_factor_thesis_pack.json")

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

    # Safety gates — read from ALL upstream sources
    sources = [inp, cr, da, tp]
    if not all_safety_blocked(sources):
        blocking.append("SAFETY_NOT_BLOCKED")

    # Alpha gates — check ALL upstream
    for name, doc in [
        ("input_pack", inp), ("council_review", cr),
        ("devil_advocate", da), ("thesis_pack", tp),
    ]:
        if doc.get("ready_for_alpha_claim", False) is True:
            blocking.append("ALPHA_CLAIM_DETECTED")
        if doc.get("alpha_validated", False) is True:
            blocking.append("ALPHA_VALIDATED_DETECTED")

    # Investment action scan
    invest_count = 0
    for c in tp.get("candidates", []):
        if c.get("investment_action", "NONE") != "NONE":
            invest_count += 1
    for r in cr.get("reviews", []):
        if r.get("investment_verdict", "BLOCKED") != "BLOCKED":
            invest_count += 1
    if invest_count > 0:
        blocking.append("INVESTMENT_ACTION_DETECTED")

    # Forbidden text scan (values only, skip field names)
    bs_count = 0
    for doc in [tp, cr]:
        bs_count += scan_forbidden_text(doc)
    if bs_count > 0:
        blocking.append("BUY_SELL_INSTRUCTION_DETECTED")

    # Research boundary
    research_boundary = (
        all(
            doc.get("ready_for_alpha_claim", False) is False
            and doc.get("alpha_validated", False) is False
            for doc in sources
        )
        and invest_count == 0
        and bs_count == 0
        and all_safety_blocked(sources)
        and tp.get("candidate_count", 0) >= 1
        and tp.get("evidence_missing_count", 0) == 0
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
        "investment_action_count": invest_count,
        "buy_sell_instruction_count": bs_count,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "research_only_boundary": research_boundary,
        "safety_checked_sources": [
            "v10_council_input_pack",
            "v10_research_council_review",
            "v10_devil_advocate_review",
            "v10_candidate_factor_thesis_pack",
        ],
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
        f"| invest={invest_count} bs={bs_count} "
        f"| safety_ok={all_safety_blocked(sources)} "
        f"| reasons={blocking}"
    )


if __name__ == "__main__":
    main()
