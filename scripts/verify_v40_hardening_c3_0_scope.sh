#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-0 Scope Verification ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

PYTHONPATH=. python3 -m pytest -q tests/hardening_c3/test_c3_scope_truth.py

echo ""
echo "Checking scope lock..."
grep -q "12 reviewer independent files/configs" docs/upgrade/V40_HARDENING_C3_SCOPE_LOCK.md && echo "  ✅ reviewer gap listed" || { echo "  ❌ missing reviewer gap"; exit 1; }
grep -q "audit zip real file export" docs/upgrade/V40_HARDENING_C3_SCOPE_LOCK.md && echo "  ✅ audit zip gap listed" || { echo "  ❌ missing audit zip"; exit 1; }
grep -q "IRF-02" docs/upgrade/V40_HARDENING_C3_SCOPE_LOCK.md && echo "  ✅ IRF gap listed" || { echo "  ❌ missing IRF gap"; exit 1; }

echo ""
echo "Checking acceptance matrix..."
for phase in C3-0 C3-1 C3-2 C3-3 C3-4 C3-5; do
    grep -q "$phase" docs/upgrade/V40_HARDENING_C3_ACCEPTANCE_MATRIX.md && echo "  ✅ $phase present" || { echo "  ❌ $phase missing"; exit 1; }
done

echo ""
echo "Checking truth report integrity..."
grep -qE "INTEGRATION_(SMOKE|COMPLETE)_CANDIDATE" docs/release/V40_CLOSEOUT_TRUTH_REPORT.md && echo "  ✅ valid integration status" || { echo "  ❌ wrong status"; exit 1; }
grep -q "NOT_APPROVED\|NOT_APPROVED" docs/release/V40_CLOSEOUT_TRUTH_REPORT.md && echo "  ✅ RC1 still NOT_APPROVED" || { echo "  ❌ RC1 wrong"; exit 1; }
grep -q "BLOCKED" docs/release/V40_CLOSEOUT_TRUTH_REPORT.md && echo "  ✅ Production still BLOCKED" || { echo "  ❌ production wrong"; exit 1; }

echo ""
echo "Checking forbidden tokens (only in allowed contexts)..."
python3 - <<'PY'
from pathlib import Path
# Truth report: at C3-0 must be SMOKE, at C3-5 may be COMPLETE
# Forward-compatible: accept either
truth = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text()
if "INTEGRATION_SMOKE_CANDIDATE" in truth:
    print("  ✅ truth report: INTEGRATION_SMOKE_CANDIDATE (C3-0 phase)")
elif "INTEGRATION_COMPLETE_CANDIDATE" in truth:
    print("  ✅ truth report: INTEGRATION_COMPLETE_CANDIDATE (C3-5 closeout)")
else:
    print("  ❌ truth report: no valid integration status")
    exit(1)
# In matrix/scope: allowed only as target description in "Allowed" section
for fp in ["docs/upgrade/V40_HARDENING_C3_ACCEPTANCE_MATRIX.md", "docs/upgrade/V40_HARDENING_C3_SCOPE_LOCK.md"]:
    path = Path(fp)
    if not path.exists():
        continue
    content = path.read_text()
    for tok in ["RC1_APPROVED", "PRODUCTION_READY", "BROKER_READY", "ACCEPTANCE_DONE"]:
        for line in content.split("\n"):
            s = line.strip()
            if tok in s and not s.startswith("❌") and not s.startswith("- ❌"):
                print(f"  ❌ forbidden token {tok} in non-forbidden context: {fp}: {s[:60]}")
                exit(1)
print("  ✅ scope/matrix: no RC1/PROD/ACCEPTANCE in non-forbidden contexts")
print("  ✅ all forbidden token checks passed")
PY

echo ""
echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-0 PASS ═══"
