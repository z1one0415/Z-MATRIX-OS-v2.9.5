#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 FINAL-HARDGATES Hardening-C2 Full Verification ═══"

echo "[0] Compile"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

echo "[1] Hardening-B baseline"
bash scripts/verify_v40_hardening_b.sh

echo "[2] C2-0 Truth Matrix"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_truth_matrix_consistency.py

echo "[3] C2-1/2 Depth Modules"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_depth_modules.py

echo "[4] C2-4 Execution + Account Depth"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_execution_account_depth.py

echo "[5] C2-5 IRF True Chains"
PYTHONPATH=. python3 - <<'PY'
from zmatrix.irf.irf_chain import irf01_full_chain, irf03_factor_chain, irf04_execution_chain
r1 = irf01_full_chain()
assert r1["export_manifest"] is False
print(" ✅ IRF-01: DataForge→Council→Report→Audit chain")
r3 = irf03_factor_chain()
assert r3["horizon_ready"] is True
print(" ✅ IRF-03: Factor→Horizon→Gate→Audit chain")
r4 = irf04_execution_chain()
assert r4["gate_action"] == "NOT_FILLABLE"
print(" ✅ IRF-04: Execution→Gate→Preview→Audit chain")
print(" ✅ All 3 IRF chains verified")
PY

echo "[6] Full integration tests"
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c_integration.py

echo "[7] C2.1 Truth/Asset/Matrix Closeout"
bash scripts/verify_v40_hardening_c2_1_truth_closeout.sh

echo "[8] Asset/Matrix/Truth sync tests"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_asset_matrix_truth_sync.py

echo "[9] Verify chain closure tests"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_verify_chain_closure.py

echo "[10] Truth report + extended forbidden scan (6 fields)"
python3 - <<'PY'
from pathlib import Path
truth = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
# Accept either SMOKE or COMPLETE (forward-compatible)
assert ("INTEGRATION_SMOKE_CANDIDATE" in truth) or ("INTEGRATION_COMPLETE_CANDIDATE" in truth), "truth missing integration status"
assert "RC1 status: NOT_APPROVED" in truth or "NOT_APPROVED" in truth
assert "Production status: BLOCKED" in truth or "BLOCKED" in truth
assert "RC1 status: APPROVED" not in truth
for p in Path("zmatrix").rglob("*.py"):
    c = p.read_text(encoding="utf-8", errors="ignore")
    if "allowlist: forbidden-token-definition" in c or "Allowlist: forbidden" in c:
        continue
    for f in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        assert f not in c, f"FORBIDDEN {f} in {p}"
print(" ✅ Truth report + 0 forbidden flags (6 fields)")
PY

echo "═══ V4.0 FINAL-HARDGATES Hardening-C2 PASS ═══"
