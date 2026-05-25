#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.7-dev Architecture Verification Gate ═══"
echo "Target: v2.9.7-dev / Batch F"

echo ""
echo "== Compile =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"

echo ""
echo "== Shared Skill Registry tests =="
python3 tests/test_shared_skill_registry.py

echo ""
echo "== Pipeline Registry tests =="
python3 tests/test_pipeline_registry.py

echo ""
echo "== Existing RC safety gate smoke =="
python3 tests/test_rc_verification_gate.py
python3 tests/test_rc_packaging.py

echo ""
echo "== Git diff check =="
git diff --check

echo ""
echo "== Git clean check =="
if [ -n "$(git status --short)" ]; then
 echo "❌ working tree not clean"
 git status --short
 exit 1
fi
echo "✅ working tree clean"

echo ""
echo "═══ Architecture verification PASS ═══"
