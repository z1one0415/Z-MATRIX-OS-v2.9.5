#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3 Full Verification ═══"
echo ""

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

# Compile check
python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

# C2 baseline
echo "[1/6] C2 baseline verify..."
bash scripts/verify_v40_hardening_c2_all.sh > /dev/null 2>&1 && echo "  ✅ C2 passed" || { echo "  ❌ C2 failed"; exit 1; }

# C3-0 scope
echo "[2/6] C3-0 scope verify..."
bash scripts/verify_v40_hardening_c3_0_scope.sh > /dev/null 2>&1 && echo "  ✅ C3-0 passed" || { echo "  ❌ C3-0 failed"; exit 1; }

# C3-1 research council
echo "[3/6] C3-1 research council verify..."
bash scripts/verify_v40_hardening_c3_1_research_council.sh > /dev/null 2>&1 && echo "  ✅ C3-1 passed" || { echo "  ❌ C3-1 failed"; exit 1; }

# C3-2 reports
echo "[4/6] C3-2 reports verify..."
bash scripts/verify_v40_hardening_c3_2_reports.sh > /dev/null 2>&1 && echo "  ✅ C3-2 passed" || { echo "  ❌ C3-2 failed"; exit 1; }

# C3-3 audit
echo "[5/6] C3-3 audit verify..."
bash scripts/verify_v40_hardening_c3_3_audit_zip.sh > /dev/null 2>&1 && echo "  ✅ C3-3 passed" || { echo "  ❌ C3-3 failed"; exit 1; }

# C3-4 IRF chains
echo "[6/6] C3-4 IRF chains verify..."
bash scripts/verify_v40_hardening_c3_4_irf_chains.sh > /dev/null 2>&1 && echo "  ✅ C3-4 passed" || { echo "  ❌ C3-4 failed"; exit 1; }

echo ""

# Full pytest
echo "Running full test suite..."
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c3_reviewers.py tests/test_hardening_c3_irf_chains.py tests/test_hardening_c3_templates_audit.py tests/test_hardening_c_integration.py tests/hardening_c3/

echo ""

# Truth report integrity
python3 - <<'PY'
from pathlib import Path

truth = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
matrix = Path("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")

# Must have correct status
assert "INTEGRATION_COMPLETE_CANDIDATE" in truth, "Truth missing INTEGRATION_COMPLETE_CANDIDATE"
assert "RC1 status: NOT_APPROVED" in truth, "Truth missing NOT_APPROVED"
assert "Production status: BLOCKED" in truth, "Truth missing BLOCKED"
assert "This release is not RC1" in truth
assert "This release is not production-ready" in truth

# Must NOT have forbidden statuses
for token in ["RC1_APPROVED", "PRODUCTION_READY", "Production status: READY", "RC1 status: APPROVED"]:
    for line in truth.split("\n") + matrix.split("\n"):
        s = line.strip()
        if token in s:
            if s.startswith("❌") or s.startswith("- ❌") or s.endswith("❌") or ": ❌" in s:
                continue
            if "Forbidden" in s or "NOT yet" in s:
                continue
            assert False, f"Forbidden token in docs: {token} → {s[:60]}"

# Scan all Python for forbidden boolean flags (skip allowlist files)
for p in Path("zmatrix").rglob("*.py"):
    c = p.read_text(encoding="utf-8", errors="ignore")
    if "allowlist: forbidden-token-definition" in c or "Allowlist: forbidden" in c:
        continue
    for f in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
    ]:
        assert f not in c, f"FORBIDDEN {f} in {p}"

print("✅ Truth report + acceptance matrix: integrity verified")
print("✅ Full forbidden scan: 0 violations")
PY

echo ""
echo "═══ V4.0 FINAL-HARDGATES Hardening-C3 Full Verification PASS ═══"
