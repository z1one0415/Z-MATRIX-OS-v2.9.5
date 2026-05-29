#!/usr/bin/env bash
set -euo pipefail

echo "═══ Post-RC1 Release Docs Consistency Audit ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 scripts/verify_post_rc1_release_docs_consistency.py

echo "═══ Post-RC1 Release Docs Consistency PASS ═══"
