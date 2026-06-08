#!/usr/bin/env python3
"""V13.F2.3.2 — Stage E: validate F06 extended sample readiness."""
import csv, json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_json(name):
    p = RUNTIME / name
    return json.loads(p.read_text()) if p.exists() else {}

mat = load_json("f06_fundamental_quality_extended_materialization.json")

sample_month_count = mat.get("sample_month_count_after_extension", 0)
minimum_required = mat.get("minimum_month_count_required", 12)
preferred_required = mat.get("preferred_month_count_required", 24)

pit_passed = mat.get("null_known_at_row_count", 999) == 0 and mat.get("strict_pit_filter_applied", False)
coverage_passed = mat.get("coverage_ratio", 0) > 0.5
minimum_sample_passed = sample_month_count >= minimum_required
preferred_sample_passed = sample_month_count >= preferred_required

blocked_reasons = []
if not pit_passed:
    blocked_reasons.append("PIT_check_failed")
if not coverage_passed:
    blocked_reasons.append("coverage_below_threshold")
if not minimum_sample_passed:
    blocked_reasons.append(f"sample_month_count_{sample_month_count}_below_minimum_{minimum_required}")

ready_for_revalidation = pit_passed and coverage_passed and minimum_sample_passed

validation = {
    "pipeline_signature": "Z2-V13-F2-3-2-F06-EXTENDED-READINESS",
    "status": "F06_EXTENDED_SAMPLE_READINESS_PASS" if ready_for_revalidation else "F06_EXTENDED_SAMPLE_READINESS_BLOCKED",
    "factor_id": "F06",
    "pit_passed": pit_passed,
    "coverage_passed": coverage_passed,
    "sample_month_count": sample_month_count,
    "minimum_month_count_required": minimum_required,
    "preferred_month_count_required": preferred_required,
    "minimum_sample_passed": minimum_sample_passed,
    "preferred_sample_passed": preferred_sample_passed,
    "ready_for_revalidation": ready_for_revalidation,
    "blocked_reasons": blocked_reasons,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f06_extended_sample_readiness_validation.json"
dst.write_text(json.dumps(validation, indent=2))
print(f"[F2.3.2-E] Sample readiness -> {dst}")
print(f"  Sample months: {sample_month_count}/{minimum_required}")
print(f"  PIT: {'PASS' if pit_passed else 'FAIL'}")
print(f"  Ready for revalidation: {ready_for_revalidation}")
sys.exit(0)
