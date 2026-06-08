#!/usr/bin/env python3
"""V13.F2.3 — Stage C: validate label isolation."""
import csv, json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def check_factor_panel_clean(fname: str) -> tuple[bool, list[str]]:
    """Check that factor panel doesn't contain forward_return columns."""
    fpath = RUNTIME / fname
    if not fpath.exists():
        return False, ["file_not_found"]
    with open(fpath) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    forbidden = ["forward_return_20d", "forward_return_60d", "future_return", "target_return", "label"]
    found = [h for h in headers if h in forbidden]
    return len(found) == 0, found

# Check label panel exists
label_panel_path = RUNTIME / "single_factor_outcome_label_panel.csv"
label_panel_exists = label_panel_path.exists()

# Check label role
label_role_valid = False
label_known_after_rebalance = False
if label_panel_exists:
    with open(label_panel_path) as f:
        reader = csv.DictReader(f)
        roles = set()
        knowns = set()
        for row in reader:
            roles.add(row.get("label_role", ""))
            knowns.add(row.get("label_known_after_rebalance", ""))
    label_role_valid = roles == {"OUTCOME_LABEL_ONLY"}
    label_known_after_rebalance = knowns == {"true"}

# Check factor panels clean
f03_clean, f03_forbidden = check_factor_panel_clean("f03_industry_relative_strength_panel.csv")
f06_clean, f06_forbidden = check_factor_panel_clean("f06_fundamental_quality_panel.csv")
factor_panels_clean = f03_clean and f06_clean

all_forbidden = f03_forbidden + f06_forbidden
feature_panel_write_detected = not factor_panels_clean
factor_panels_contain_outcome_labels = not factor_panels_clean

blocked_reasons = []
if not label_panel_exists:
    blocked_reasons.append("label_panel_not_found")
if not label_role_valid:
    blocked_reasons.append("label_role_not_OUTCOME_LABEL_ONLY")
if not label_known_after_rebalance:
    blocked_reasons.append("label_not_known_after_rebalance")
if feature_panel_write_detected:
    blocked_reasons.append(f"factor_panels_contain_forbidden_columns: {all_forbidden}")

isolation_passed = label_panel_exists and label_role_valid and label_known_after_rebalance and factor_panels_clean

result = {
    "pipeline_signature": "Z2-V13-F2-3-LABEL-ISOLATION",
    "status": "V13_F2_3_OUTCOME_LABEL_ISOLATION_VALIDATION_PASS" if isolation_passed else "V13_F2_3_OUTCOME_LABEL_ISOLATION_VALIDATION_BLOCKED",
    "label_isolation_passed": isolation_passed,
    "feature_panel_write_detected": feature_panel_write_detected,
    "factor_panels_contain_outcome_labels": factor_panels_contain_outcome_labels,
    "label_role_valid": label_role_valid,
    "label_known_after_rebalance": label_known_after_rebalance,
    "blocked_reasons": blocked_reasons,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_outcome_label_isolation_validation.json"
dst.write_text(json.dumps(result, indent=2))
print(f"[F2.3-C] Label isolation validation -> {dst} {'PASS' if isolation_passed else 'BLOCKED'}")
sys.exit(0)
