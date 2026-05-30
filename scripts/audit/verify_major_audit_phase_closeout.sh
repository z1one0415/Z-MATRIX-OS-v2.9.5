#!/usr/bin/env bash
set -euo pipefail

echo "═══ Major Audit Phase Closeout Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/audit/test_major_audit_phase_closeout.py
PYTHONPATH=. python3 -m pytest -q tests/audit/

bash scripts/run_golden_path_600519.sh --dry-run

python3 - <<'PY'
import json
from pathlib import Path

docs = [
    Path("docs/audit/MAJOR_AUDIT_PHASE_CLOSEOUT.md"),
    Path("docs/audit/MAJOR_AUDIT_FINAL_VERDICT.md"),
    Path("docs/audit/RESEARCH_OS_V3_AUDIT_FREEZE_MANIFEST.md"),
]
for p in docs:
    assert p.exists(), f"missing {p}"

verdict = json.loads(Path("runtime_reports/audit/major_audit_final_verdict.json").read_text())

assert verdict["status"] == "RESEARCH_OS_V3_MAJOR_AUDIT_PHASE_FROZEN"
assert verdict["architecture_freeze"] == "MAINTAINED"
assert verdict["p0"] == 0
assert verdict["p1_blocking"] == 0
assert verdict["production"] == "BLOCKED"
assert verdict["broker_runtime"] == "BLOCKED"
assert verdict["real_trade"] == "BLOCKED"

combined = "\n".join(p.read_text() for p in docs)
for forbidden in [
    "Production Ready", "Broker Ready", "Runtime Ready", "Real Trade Ready", "Phase 6 Approved",
]:
    assert forbidden not in combined, f"forbidden marker: {forbidden}"

print("✅ Major Audit Phase Closeout static check PASS")
PY

echo "═══ Major Audit Phase Closeout PASS ═══"
