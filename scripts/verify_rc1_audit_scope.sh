#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 RC1 Readiness Audit RA-0 Scope Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

PYTHONPATH=. python3 -m pytest -q tests/rc1_audit/test_rc1_audit_scope.py

# Verify manifest
python3 - <<'PY'
import json
from pathlib import Path

m = json.loads(Path("docs/rc1_audit/RC1_BASELINE_MANIFEST.json").read_text())
assert m["baseline_commit"] == "0ccf235"
assert m["rc1_status"] == "NOT_APPROVED"
assert m["production_status"] == "BLOCKED"
assert m["audit_mode"] == "READ_ONLY"
assert m["rc1_tag_allowed"] == False

s = Path("docs/rc1_audit/RC1_AUDIT_SCOPE_LOCK.md").read_text()
assert "RA-0" in s and "RA-8" in s
assert "Creating v4.0-rc1 git tag" in s and "❌" in s, "must forbid RC1 tag"

a = Path("docs/rc1_audit/RC1_AUDIT_ACCEPTANCE_MATRIX.md").read_text()
for phase in ["RA-0","RA-1","RA-2","RA-3","RA-4","RA-5","RA-6","RA-7","RA-8"]:
    assert phase in a, f"missing {phase}"
for bad in ["RC1_APPROVED", "PRODUCTION_READY"]:
    assert bad not in a or "❌" in a, f"forbidden token not marked as such: {bad}"

print("✅ RA-0: scope lock + baseline manifest verified")
PY

echo "═══ V4.0 RC1 Readiness Audit RA-0 PASS ═══"
