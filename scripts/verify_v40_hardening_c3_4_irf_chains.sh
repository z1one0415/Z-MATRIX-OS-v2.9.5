#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-4 IRF Chain Verify ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/irf/ 2>&1 | tail -1

PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c3_irf_chains.py

# Verify all 8 chains + 8 IRF pipelines
python3 - <<'PY'
from zmatrix.irf.irf_chain import (
    irf01_full_chain, irf02_monthly_selection_chain,
    irf03_factor_chain, irf04_execution_chain,
    irf05_account_review_chain, irf06_portfolio_alpha_chain,
    irf07_multi_strategy_chain, irf08_factor_data_chain,
)
chains = [
    ("IRF-01", irf01_full_chain),
    ("IRF-02", irf02_monthly_selection_chain),
    ("IRF-03", irf03_factor_chain),
    ("IRF-04", irf04_execution_chain),
    ("IRF-05", irf05_account_review_chain),
    ("IRF-06", irf06_portfolio_alpha_chain),
    ("IRF-07", irf07_multi_strategy_chain),
    ("IRF-08", irf08_factor_data_chain),
]
assert len(chains) == 8

for irf_id, fn in chains:
    r = fn()
    env = r.get("envelope", {})
    if hasattr(env, 'to_dict'):
        env = env.to_dict()
    assert env.get("real_trade_allowed", False) == False, f"{irf_id} real_trade=t"
    assert env.get("broker_order_allowed", False) == False, f"{irf_id} broker=t"
    assert env.get("production_allowed", False) == False, f"{irf_id} production=t"
    assert env.get("human_review_required", True) == True, f"{irf_id} no human review"

from zmatrix.irf.pipelines import IRF_REGISTRY
assert len(IRF_REGISTRY) == 8
for irf_id, irf in IRF_REGISTRY.items():
    r = irf.execute()
    assert r["real_trade_allowed"] == False
    assert r["broker_order_allowed"] == False
    assert r.get("production_allowed", False) == False

print("✅ C3-4: 8 chain functions + 8 IRF pipelines, all no-trade verified")
PY

# Scan for forbidden
python3 - <<'PY'
from pathlib import Path
for p in Path("zmatrix/irf").rglob("*.py"):
    c = p.read_text()
    if "allowlist:" in c: continue
    for f in ["real_trade_allowed=True", "broker_order_allowed=True"]:
        assert f not in c, f"FORBIDDEN {f} in {p}"
print("✅ C3-4 forbidden scan: 0 violations")
PY

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-4 PASS ═══"
