#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.16-dev v3.0-alpha Readiness Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_integration_readiness_map test_integration_capability_audit \
  test_integration_workflow_alignment test_integration_event_chain_validator \
  test_integration_safety_matrix test_integration_readiness_report \
  test_v3_alpha_readiness_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Tail-risk verify =="
bash scripts/verify_tail_risk_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.0-alpha Readiness Verification PASS ═══"
