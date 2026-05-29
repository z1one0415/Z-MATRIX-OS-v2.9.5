#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 RC1-E0 Evidence Lock Full Verification ═══"
echo ""

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

# E0 evidence lock
echo "[1/4] Cloud evidence lock..."
bash scripts/verify_rc1_cloud_evidence_lock.sh || { echo "❌ FAIL"; exit 1; }

# RC1 audit baseline
echo "[2/4] RC1 readiness audit baseline..."
bash scripts/verify_rc1_readiness_audit_all.sh > /dev/null 2>&1 && echo "  ✅ passed" || { echo "  ❌ FAIL"; exit 1; }

# Full audit tests
echo "[3/4] RC1 audit tests..."
PYTHONPATH=. python3 -m pytest -q tests/rc1_audit/ --ignore=tests/rc1_audit/test_full_verify_script.py || { echo "  ❌ FAIL"; exit 1; }

# Tag dry-run and release note safety
echo "[4/4] Tag dry-run + release note safety..."
python3 - <<'PY'
from pathlib import Path

combined = "\n".join([
    Path("docs/rc1_audit/RC1_TAG_DRY_RUN_MANIFEST.md").read_text(encoding="utf-8"),
    Path("docs/release/V4_0_RC1_RELEASE_NOTE_DRAFT.md").read_text(encoding="utf-8"),
])

for required in [
    "FALSE",
    "Manual approval",
    "research-only release candidate",
    "production-ready",
]:
    assert required.lower() in combined.lower(), f"Missing: {required}"

for forbidden in [
    "Production ready",
    "Broker ready",
    "Runtime ready",
    "Real trade ready",
    "Autonomous trading ready",
]:
    assert forbidden not in combined, f"Forbidden release claim: {forbidden}"

print("✅ RC1-E0 evidence lock full verification PASS")
PY

echo ""
echo "═══ V4.0 RC1-E0 Evidence Lock PASS ═══"
