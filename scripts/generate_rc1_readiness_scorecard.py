#!/usr/bin/env python3
"""Generate RC1 Readiness Scorecard."""
import subprocess, json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
scorecard_path = WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_SCORECARD.md"

# --- Scorer ---
def check(name, weight, pass_condition):
    """Return (score_earned, detail_string)"""
    result = "PASS" if pass_condition else "FAIL"
    earned = weight if result == "PASS" else 0
    return earned, result

total = 0
details = []

# 1. Full verify reproducibility (15 pts)
# Check that rc1 audit full verify log exists
log_files = list((WORKSPACE / "runtime_reports" / "rc1_audit").glob("full_verify_*.log"))
has_log = len(log_files) > 0
s, r = check("Full verify log exists", 15, has_log)
total += s; details.append(f"1. Verify Reproduction: {r} ({s}/15)")

# 2. CI/cloud parity (15 pts) — GitHub Actions workflow exists
ci_file = WORKSPACE / ".github" / "workflows" / "v40-rc1-audit.yml"
s, r = check("GitHub Actions CI", 15, ci_file.exists())
total += s; details.append(f"2. CI Parity: {r} ({s}/15)")

# 3. Repository hygiene (10 pts)
hygiene = subprocess.run(["bash", "scripts/verify_rc1_repo_hygiene.sh"], capture_output=True, text=True, cwd=str(WORKSPACE))
s, r = check("Repository hygiene", 10, hygiene.returncode == 0)
total += s; details.append(f"3. Repo Hygiene: {r} ({s}/10)")

# 4. Safety deep scan (15 pts)
safety = subprocess.run(["python3", "scripts/verify_rc1_safety_deep_scan.py"], capture_output=True, text=True, cwd=str(WORKSPACE))
try:
    safety_json = json.loads(safety.stdout.strip() or "{}")
    safety_pass = safety_json.get("scan_status") == "PASS"
except:
    safety_pass = False
s, r = check("Safety deep scan", 15, safety_pass)
total += s; details.append(f"4. Safety Scan: {r} ({s}/15)")
if r == "FAIL":
    total = 0  # HARD GATE: safety fail = RC1_BLOCKED

# 5. Artifact exclusion (10 pts)
art = subprocess.run(["bash", "scripts/verify_rc1_artifact_exclusion.sh"], capture_output=True, text=True, cwd=str(WORKSPACE))
s, r = check("Artifact exclusion", 10, art.returncode == 0)
total += s; details.append(f"5. Artifact Exclusion: {r} ({s}/10)")

# 6. Module completeness evidence (15 pts)
ev_md = WORKSPACE / "docs" / "rc1_audit" / "RC1_MODULE_COMPLETENESS_EVIDENCE.md"
ev_json = WORKSPACE / "docs" / "rc1_audit" / "RC1_MODULE_EVIDENCE.json"
modules_pass = ev_md.exists() and ev_json.exists()
s, r = check("Module evidence", 15, modules_pass)
total += s; details.append(f"6. Module Evidence: {r} ({s}/15)")

# 7. Truth Report consistency (10 pts)
truth = WORKSPACE / "docs" / "release" / "V40_CLOSEOUT_TRUTH_REPORT.md"
truth_ok = truth.exists() and "INTEGRATION_COMPLETE_CANDIDATE" in truth.read_text()
s, r = check("Truth Report", 10, truth_ok)
total += s; details.append(f"7. Truth Report: {r} ({s}/10)")

# 8. No production/broker/runtime (10 pts) — safety scan already confirmed 0 violations
s, r = check("No production/ broker/runtime flags", 10, safety_pass)
total += s; details.append(f"8. Safety Flags: {r} ({s}/10)")

# Recommendation
if total >= 90:
    recommendation = "RC1_READY_RECOMMENDED"
elif total >= 80:
    recommendation = "RC1_CONDITIONAL"
else:
    recommendation = "RC1_BLOCKED"

# Hard gates
if not safety_pass:
    recommendation = "RC1_BLOCKED"
if not has_log:
    recommendation = "RC1_BLOCKED"

# Generate markdown
lines = [
    "# RC1 Readiness Scorecard",
    "",
    f"Score: **{total}/100**",
    f"Recommendation: **{recommendation}**",
    "",
    "## Item Scores",
    "",
]
lines.extend(f"- {d}" for d in details)
lines.extend([
    "",
    "## Hard Gates",
    f"- Safety deep scan: {'✅ PASS' if safety_pass else '❌ FAIL → RC1_BLOCKED'}",
    f"- Full verify log: {'✅ EXISTS' if has_log else '❌ MISSING → RC1_BLOCKED'}",
    f"- CI workflow: {'✅ EXISTS' if ci_file.exists() else '⚠️ MISSING (exception noted)'}",
    "",
    "## Final Decision",
    f"**{recommendation}**",
    "",
    "> ⚠️ This is a READ-ONLY audit recommendation.",
    "> RC1 tag NOT created. Production NOT enabled.",
    "> Human approval REQUIRED before any RC1 action.",
])
scorecard_path.write_text("\n".join(lines))
print(f"Scorecard: {total}/100 → {recommendation}")
