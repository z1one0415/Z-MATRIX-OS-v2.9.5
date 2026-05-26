#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.18-dev v3.0-alpha RC Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
echo ""; echo "== Generate RC artifacts =="
python3 scripts/generate_v3_alpha_rc_artifacts.py
for t in test_alpha_rc_manifest test_alpha_rc_verification_matrix \
  test_alpha_rc_module_inventory test_alpha_rc_known_limitations \
  test_alpha_rc_gate_validator test_alpha_rc_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Dry-run verify =="
bash scripts/verify_v3_alpha_dry_run_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.0-alpha RC Verification PASS ═══"
