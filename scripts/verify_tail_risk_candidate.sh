#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.15-dev Tail-Risk Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_tail_risk_market_signals test_limit_down_blackhole test_domestic_liquidity_crash \
  test_hibernate_mode test_wakeup_probation test_d_matrix_freeze test_risk_isolation_unit \
  test_tail_risk_controller test_tail_risk_event_adapters test_tail_risk_policy test_tail_risk_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Prompt verify =="
bash scripts/verify_prompt_middleware_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ Tail-Risk Verification PASS ═══"
