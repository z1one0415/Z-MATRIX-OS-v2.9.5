#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 RC1 Readiness Audit Full Verification ═══"
echo ""

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

# [1/8] C3 baseline
echo "[1/8] C3 baseline..."
bash scripts/verify_v40_hardening_c3_all.sh > /dev/null 2>&1 && echo "  ✅ C3 passed" || { echo "  ❌ C3 failed"; exit 1; }

# [2/8] RA-0 scope
echo "[2/8] RA-0 audit scope..."
bash scripts/verify_rc1_audit_scope.sh > /dev/null 2>&1 && echo "  ✅ RA-0 passed" || { echo "  ❌ RA-0 failed"; exit 1; }

# [3/8] RA-3 repo hygiene
echo "[3/8] RA-3 repo hygiene..."
bash scripts/verify_rc1_repo_hygiene.sh > /dev/null 2>&1 && echo "  ✅ RA-3 passed" || { echo "  ❌ RA-3 failed"; exit 1; }

# [4/8] RA-4 safety scan
echo "[4/8] RA-4 safety scan..."
python3 scripts/verify_rc1_safety_deep_scan.py > /dev/null 2>&1 && echo "  ✅ RA-4 passed" || { echo "  ❌ RA-4 failed"; exit 1; }

# [5/8] RA-5 artifact exclusion
echo "[5/8] RA-5 artifact exclusion..."
bash scripts/verify_rc1_artifact_exclusion.sh > /dev/null 2>&1 && echo "  ✅ RA-5 passed" || { echo "  ❌ RA-5 failed"; exit 1; }

# [6/8] Full pytest
echo "[6/8] Full pytest..."
PYTHONPATH=. python3 -m pytest -q tests/rc1_audit/ > /dev/null 2>&1 && echo "  ✅ pytest passed" || { echo "  ❌ pytest failed"; exit 1; }

# [7/8] Module evidence + Scorecard
echo "[7/8] Module evidence + Scorecard..."
PYTHONPATH=. python3 scripts/generate_rc1_module_evidence.py > /dev/null 2>&1 && echo "  ✅ evidence" || { echo "  ❌ evidence"; exit 1; }
PYTHONPATH=. python3 scripts/generate_rc1_readiness_scorecard.py > /dev/null 2>&1 && echo "  ✅ scorecard" || { echo "  ❌ scorecard"; exit 1; }

# [8/8] Truth integrity
echo "[8/8] Truth report integrity..."
python3 - <<'PY'
from pathlib import Path

truth = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
score = Path("docs/rc1_audit/RC1_READINESS_SCORECARD.md").read_text(encoding="utf-8")

assert "INTEGRATION_COMPLETE_CANDIDATE" in truth
assert "RC1 status: NOT_APPROVED" in truth
assert "Production status: BLOCKED" in truth
assert "This release is not RC1" in truth
assert "RC1 tag NOT created" in score
assert "RC1_READY_RECOMMENDED" in score
assert "Human approval REQUIRED" in score
print("  ✅ all truth checks passed")
PY

echo ""
echo "═══ V4.0 RC1 Readiness Audit Full Verification PASS ═══"
