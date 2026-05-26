#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.17-dev v3.0-alpha Dry-Run Verification Gate ═══"
echo ""; echo "== Compile all =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
for t in test_v3_alpha_dry_run_rehearsal test_v3_alpha_dry_run_validator \
  test_v3_alpha_dry_run_report test_v3_alpha_dry_run_architecture; do
  echo ""; echo "== $t =="; python3 "tests/${t}.py"
done
echo ""; echo "== Readiness verify =="
bash scripts/verify_v3_alpha_readiness_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.0-alpha Dry-Run Verification PASS ═══"
