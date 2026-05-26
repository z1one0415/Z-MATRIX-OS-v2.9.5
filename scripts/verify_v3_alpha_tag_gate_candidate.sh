#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v2.9.19-dev v3.0-alpha Tag Gate Verification ═══"
echo ""; echo "== Compile all =="
PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"
echo ""; echo "== Generate tag artifacts =="
PYTHONPATH=. python3 scripts/generate_v3_alpha_tag_artifacts.py
for t in test_alpha_tag_artifact_consistency test_alpha_tag_readiness_validator \
  test_alpha_tag_release_notes test_alpha_tag_architecture; do
  echo ""; echo "== $t =="; PYTHONPATH=. python3 "tests/${t}.py"
done
echo ""; echo "== RC verify =="
PYTHONPATH=. bash scripts/verify_v3_alpha_rc_candidate.sh
echo ""; echo "== Git check =="
if [ -n "$(git status --short)" ]; then echo "❌ dirty"; git status --short; exit 1; fi
echo "✅ clean"
echo ""; echo "═══ v3.0-alpha Tag Gate Verification PASS ═══"
