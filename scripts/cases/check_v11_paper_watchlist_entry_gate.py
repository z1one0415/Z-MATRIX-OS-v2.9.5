#!/usr/bin/env python3
"""V10-E: V11 paper watchlist entry gate — explicit safety fields, value-only scan."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

SAFETY_FIELDS = ["production", "broker_runtime", "real_trade"]
ALPHA_FIELDS = ["ready_for_alpha_claim", "alpha_validated"]
FORBIDDEN = [
    "BUY", "SELL", "ADD", "REDUCE",
    "\u4e70\u5165", "\u5356\u51fa", "\u5efa\u4ed3", "\u52a0\u4ed3", "\u51cf\u4ed3",
    "\u6b62\u76c8", "\u6b62\u635f",  # 止损 (fixed: was 止棍)
]


def load(name):
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def check_explicit_fields(docs, fields, block_missing, block_true):
    """Return (ok, missing_list, violation_list)."""
    missing = []
    violations = []
    for name, doc in docs.items():
        for f in fields:
            if f not in doc:
                missing.append(f"{name}.{f}")
            elif block_true and doc[f] is True:
                violations.append(f"{name}.{f}=True")
            elif not block_true and doc[f] != "BLOCKED":
                violations.append(f"{name}.{f}={doc[f]}")
    return len(missing) == 0 and len(violations) == 0, missing, violations


def iter_values(obj):
    """Recursively yield all string VALUES (not keys)."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from iter_values(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_values(item)
    elif isinstance(obj, str):
        yield obj


def scan_forbidden(docs):
    """Value-only scan for forbidden action markers."""
    violations = []
    for name, doc in docs.items():
        for value in iter_values(doc):
            v_upper = value.upper()
            for marker in FORBIDDEN:
                if marker.upper() in v_upper:
                    violations.append({
                        "source": name,
                        "marker": marker,
                        "value_excerpt": value[:160],
                    })
    return violations


def scan_investment_actions(tp, cr, da):
    violations = []
    for c in tp.get("candidates", []):
        a = c.get("investment_action", "NONE")
        if a != "NONE":
            violations.append({
                "source": "candidate_factor_thesis_pack",
                "factor_id": c.get("factor_id"),
                "field": "investment_action", "value": a,
            })
    for r in cr.get("reviews", []):
        v = r.get("investment_verdict", "BLOCKED")
        if v != "BLOCKED":
            violations.append({
                "source": "research_council_review",
                "factor_id": r.get("factor_id"),
                "field": "investment_verdict", "value": v,
            })
    for r in da.get("factor_failure_reviews", []):
        v = r.get("investment_verdict", "BLOCKED")
        if v is not None and v != "BLOCKED":
            violations.append({
                "source": "devil_advocate_review",
                "factor_id": r.get("factor_id"),
                "field": "investment_verdict", "value": v,
            })
    return violations


def main():
    inp = load("v10_council_input_pack.json")
    cr = load("v10_research_council_review.json")
    da = load("v10_devil_advocate_review.json")
    tp = load("v10_candidate_factor_thesis_pack.json")
    upstream_audit = load("v10_upstream_safety_alpha_audit.json")


    docs = {
        "v10_council_input_pack": inp,
        "v10_research_council_review": cr,
        "v10_devil_advocate_review": da,
        "v10_candidate_factor_thesis_pack": tp,
    }

    blocking = []

    # Status gates
    for name, expected, doc in [
        ("INPUT_PACK_NOT_BUILT", "V10_COUNCIL_INPUT_PACK_BUILT", inp),
        ("COUNCIL_REVIEW_NOT_BUILT", "V10_RESEARCH_COUNCIL_REVIEW_BUILT", cr),
        ("DEVIL_ADVOCATE_NOT_BUILT", "V10_DEVIL_ADVOCATE_REVIEW_BUILT", da),
        ("THESIS_PACK_NOT_BUILT", "V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT", tp),
    ]:
        if doc.get("status") != expected:
            blocking.append(name)

    # Evidence
    if tp.get("candidate_count", 0) < 1:
        blocking.append("NO_CANDIDATES")
    if tp.get("evidence_missing_count", 0) > 0:
        blocking.append("EVIDENCE_MISSING")
    if da.get("critical_blockers", 0) > 0:
        blocking.append("CRITICAL_BLOCKERS_PRESENT")


    # Upstream audit — must pass before anything else
    upstream_ok = (
        upstream_audit.get("status") == "V10_UPSTREAM_SAFETY_ALPHA_AUDIT_PASS"
        and upstream_audit.get("ready_for_v11_gate") is True
        and upstream_audit.get("safety_missing_fields", ["X"]) == []
        and upstream_audit.get("safety_unblocked_fields", ["X"]) == []
        and upstream_audit.get("alpha_missing_fields", ["X"]) == []
        and upstream_audit.get("alpha_true_fields", ["X"]) == []
    )
    if not upstream_ok:
        blocking.append("UPSTREAM_SAFETY_ALPHA_AUDIT_NOT_PASS")
    if upstream_audit.get("safety_missing_fields"):
        blocking.append("UPSTREAM_SAFETY_FIELD_MISSING")
    if upstream_audit.get("alpha_missing_fields"):
        blocking.append("UPSTREAM_ALPHA_FIELD_MISSING")

    # Safety — explicit fields required
    safety_ok, safety_missing, safety_unblocked = check_explicit_fields(
        docs, SAFETY_FIELDS, block_missing=True, block_true=False
    )
    if safety_missing:
        blocking.append("SAFETY_FIELD_MISSING")
    if safety_unblocked:
        blocking.append("SAFETY_NOT_BLOCKED")

    # Alpha — explicit fields required
    alpha_ok, alpha_missing, alpha_true = check_explicit_fields(
        docs, ALPHA_FIELDS, block_missing=True, block_true=True
    )
    if alpha_missing:
        blocking.append("ALPHA_FIELD_MISSING")
    if alpha_true:
        for f in alpha_true:
            if "ready_for_alpha_claim" in f:
                blocking.append("ALPHA_CLAIM_DETECTED")
            elif "alpha_validated" in f:
                blocking.append("ALPHA_VALIDATED_DETECTED")

    # Investment actions
    invest_violations = scan_investment_actions(tp, cr, da)
    if invest_violations:
        blocking.append("INVESTMENT_ACTION_DETECTED")

    # Forbidden action scan (value-only, all 4 sources)
    forbidden_violations = scan_forbidden(docs)
    if forbidden_violations:
        blocking.append("BUY_SELL_INSTRUCTION_DETECTED")

    # Research boundary
    research_boundary = (
        alpha_ok and safety_ok
        and len(invest_violations) == 0
        and len(forbidden_violations) == 0
        and tp.get("candidate_count", 0) >= 1
        and tp.get("evidence_missing_count", 0) == 0
        and da.get("critical_blockers", 0) == 0
    )
    if not research_boundary:
        blocking.append("RESEARCH_ONLY_BOUNDARY_MISSING")

    allowed = len(blocking) == 0

    gate = {
        "status": (
            "V11_PAPER_WATCHLIST_ENTRY_ALLOWED"
            if allowed else "V11_PAPER_WATCHLIST_ENTRY_BLOCKED"
        ),
        "ready_for_paper_watchlist": allowed,
        "candidate_count": tp.get("candidate_count", 0),
        "evidence_missing_count": tp.get("evidence_missing_count", 0),
        "critical_blockers": da.get("critical_blockers", 0),
        "safety_ok": safety_ok,
        "safety_checked_sources": list(docs.keys()),
        "safety_missing_fields": safety_missing,
        "safety_unblocked_fields": safety_unblocked,
        "alpha_missing_fields": alpha_missing,
        "alpha_true_fields": alpha_true,
        "investment_action_count": len(invest_violations),
        "investment_action_violations": invest_violations,
        "buy_sell_instruction_count": len(forbidden_violations),
        "forbidden_action_violations": forbidden_violations,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "research_only_boundary": research_boundary,
        "upstream_safety_alpha_audit_required": True,
        "upstream_safety_alpha_audit_pass": upstream_ok,
        "upstream_audit_status": upstream_audit.get("status", "MISSING"),
        "blocking_reasons": blocking,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (C / "v11_paper_watchlist_entry_gate.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False)
    )
    print(
        f"V11: {'ALLOWED' if allowed else 'BLOCKED'} "
        f"| safety_miss={len(safety_missing)} alpha_miss={len(alpha_missing)} "
        f"| invest={len(invest_violations)} forbid={len(forbidden_violations)} "
        f"| reasons={blocking}"
    )


if __name__ == "__main__":
    main()
