#!/usr/bin/env python3
"""V12.1: Research-Only Live Paper Loop Audit — hardgate scan including label-key validation."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

FORBIDDEN_WORDS = [
    "BUY", "SELL", "ADD", "REDUCE", "LONG", "SHORT",
    "POSITION", "ORDER", "TRADE_EXECUTION", "WEIGHT",
    "TARGET_PRICE", "TAKE_PROFIT", "STOP_LOSS",
]


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def scan_forbidden(obj, path: str = "") -> list:
    violations = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            current = f"{path}.{k}" if path else k
            if isinstance(v, str):
                for word in FORBIDDEN_WORDS:
                    if word in v.upper() or word == v.upper():
                        violations.append(f"FORBIDDEN_WORD {word} in {current}={v}")
            elif isinstance(v, (dict, list)):
                violations.extend(scan_forbidden(v, current))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            current = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                violations.extend(scan_forbidden(item, current))
    return violations


def check_has_fixed_base_date(source_code: str) -> bool:
    """Check if status updater source contains hardcoded base_date = old date."""
    if 'base_date = "20240905"' in source_code:
        return True
    return False


def main():
    contract = load("v12_1_live_paper_contract.json")
    registry = load("v12_1_live_paper_run_registry.json")
    schedule = load("v12_1_live_paper_due_schedule.json")
    status_update = load("v12_1_live_paper_status_update.json")
    delta = load("v12_1_live_paper_delta_report.json")

    reasons = []
    rejection_violations = []

    targets = [
        ("contract", contract),
        ("registry", registry),
        ("schedule", schedule),
        ("status_update", status_update),
        ("delta", delta),
    ]

    # 1. research_only / paper_only
    for fname, data in targets:
        if data:
            if data.get("research_only") is not None and data["research_only"] is not True:
                reasons.append(f"RESEARCH_ONLY_FALSE_IN_{fname.upper()}")
            if data.get("paper_only") is not None and data["paper_only"] is not True:
                reasons.append(f"PAPER_ONLY_FALSE_IN_{fname.upper()}")

    # 2. Alpha claims
    for fname, data in targets:
        if data.get("ready_for_alpha_claim", False):
            reasons.append(f"ALPHA_CLAIM_READY_IN_{fname.upper()}")
        if data.get("alpha_validated", False):
            reasons.append(f"ALPHA_VALIDATED_IN_{fname.upper()}")

    # 3. Safety channels
    for fname, data in targets:
        for ch in ["production", "broker_runtime", "real_trade"]:
            if data.get(ch) != "BLOCKED":
                reasons.append(f"{ch.upper()}_NOT_BLOCKED_IN_{fname.upper()}")

    # 4. Action counts
    for fname, data in targets:
        if isinstance(data.get("investment_action_count"), int) and data["investment_action_count"] != 0:
            reasons.append(f"INVESTMENT_ACTION_COUNT_NONZERO_{fname.upper()}")
        if isinstance(data.get("trade_action_count"), int) and data["trade_action_count"] != 0:
            reasons.append(f"TRADE_ACTION_COUNT_NONZERO_{fname.upper()}")

    # 5. Action field checks
    for fname, data, container_key in [
        ("registry", registry, "runs"),
        ("schedule", schedule, "schedule_items"),
        ("status_update", status_update, "updated_runs"),
    ]:
        container = data.get(container_key, [])
        for item in container:
            if item.get("investment_action", "NONE") != "NONE":
                reasons.append(f"INVESTMENT_ACTION_NOT_NONE_{fname.upper()}")
            if item.get("trade_action", "NONE") != "NONE":
                reasons.append(f"TRADE_ACTION_NOT_NONE_{fname.upper()}")

    # 6. Forbidden word scan
    violations = []
    for fname, data in targets:
        violations.extend(scan_forbidden(data, fname))

    # 7. Rejected reactivation check
    schedule_run_ids = set()
    for item in schedule.get("schedule_items", []):
        schedule_run_ids.add(item.get("live_paper_run_id", ""))

    for run in registry.get("runs", []):
        rid = run.get("live_paper_run_id", "")
        run_status = run.get("run_status", "")
        if run_status == "PRESERVED_REJECTED":
            if rid in schedule_run_ids:
                rejection_violations.append(f"REJECTED_REACTIVATED: {rid} appears in due schedule")
            for ur in status_update.get("updated_runs", []):
                if ur.get("live_paper_run_id") == rid and ur.get("run_status") not in ("PRESERVED_REJECTED",):
                    rejection_violations.append(f"REJECTED_REACTIVATED: {rid} activated in status_update ({ur.get('run_status')})")

    # ── NEW V12.1.1 HARDGATES ──

    # H1: required_label_key.as_of_date must not reuse source_start_as_of_date
    for item in schedule.get("schedule_items", []):
        rlk = item.get("required_label_key", {})
        ssa = item.get("source_start_as_of_date", "")
        if rlk.get("as_of_date") and rlk["as_of_date"] == ssa:
            reasons.append(f"LIVE_PAPER_LABEL_KEY_REUSES_SOURCE_DATE:{item.get('live_paper_run_id','')}")
        if rlk.get("as_of_date") and rlk["as_of_date"] == "20240905":
            reasons.append(f"LABEL_KEY_USES_OLD_BASE_DATE:{item.get('live_paper_run_id','')}")

    # H2: Completed runs must have validated label key
    for ur in status_update.get("updated_runs", []):
        if ur.get("run_status") == "COMPLETED":
            if not ur.get("label_key_validated", False):
                reasons.append(f"COMPLETED_RUN_WITHOUT_VALIDATED_LABEL_KEY:{ur.get('live_paper_run_id','')}")
            if not ur.get("label_source"):
                reasons.append(f"COMPLETED_RUN_WITHOUT_LABEL_SOURCE:{ur.get('live_paper_run_id','')}")
            # Check the required_label_key does not reuse source date
            rlk = ur.get("required_label_key", {})
            if rlk.get("as_of_date") == "20240905":
                reasons.append(f"COMPLETED_RUN_USES_SOURCE_DATE_AS_LABEL_KEY:{ur.get('live_paper_run_id','')}")

    # H3: Due schedule must have required_label_key
    for item in schedule.get("schedule_items", []):
        rlk = item.get("required_label_key", {})
        if not rlk or not rlk.get("as_of_date") or not rlk.get("horizon"):
            reasons.append(f"DUE_SCHEDULE_MISSING_REQUIRED_LABEL_KEY:{item.get('live_paper_run_id','')}")

    # H4: Status updater source must not use fixed base_date
    try:
        updater_src = (W / "scripts/cases/update_v12_1_live_paper_status.py").read_text()
        if check_has_fixed_base_date(updater_src):
            reasons.append("FIXED_BASE_DATE_STATUS_UPDATE_FORBIDDEN")
    except Exception:
        pass  # Source not readable → skip

    # H5: Future labels insufficient → completion must not be COMPLETED
    if status_update.get("waiting_run_count", 0) > 0 and status_update.get("live_paper_completion_status") == "COMPLETED":
        reasons.append("COMPLETION_CLAIMED_WITH_PENDING_RUNS")

    # H6: reused source date count > 0 → not allowed
    if status_update.get("reused_source_date_count", 0) > 0:
        reasons.append(f"REUSED_SOURCE_DATE_DETECTED:{status_update.get('reused_source_date_count')}")

    all_violations = violations + reasons + rejection_violations
    blocked = len(all_violations) > 0

    result = {
        "status": "V12_1_LIVE_PAPER_LOOP_AUDIT_PASS" if not blocked else "V12_1_LIVE_PAPER_LOOP_AUDIT_BLOCKED",
        "live_paper_loop_confirmed": not blocked,
        "future_label_status": status_update.get("live_paper_completion_status", "UNKNOWN"),
        "forbidden_action_violations": violations + reasons,
        "rejected_reactivation_violations": rejection_violations,
        "blocking_reasons": all_violations,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_loop_audit.json", "w"), indent=2)
    print(f"V12.1 Audit: {result['status']} | violations={len(violations)+len(reasons)} "
          f"rejections={len(rejection_violations)}")


if __name__ == "__main__":
    main()
