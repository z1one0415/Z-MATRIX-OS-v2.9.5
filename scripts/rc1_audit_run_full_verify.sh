#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

mkdir -p runtime_reports/rc1_audit

LOG="runtime_reports/rc1_audit/full_verify_$(date +%Y%m%d_%H%M%S).log"

{
 echo "══════════════════════════════════════════"
 echo "RC1 Audit Full Verify"
 echo "══════════════════════════════════════════"
 echo "commit=$(git rev-parse HEAD)"
 echo "branch=$(git branch --show-current)"
 echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
 echo ""

 echo "═══ [1/4] Compile ═══"
 python3 -m compileall zmatrix tests scripts || true

 echo ""
 echo "═══ [2/4] Hardening-B ═══"
 bash scripts/verify_v40_hardening_b.sh || true

 echo ""
 echo "═══ [3/4] Hardening-C2 ═══"
 bash scripts/verify_v40_hardening_c2_all.sh || true

 echo ""
 echo "═══ [4/4] Hardening-C3 ═══"
 bash scripts/verify_v40_hardening_c3_all.sh || true

 echo ""
 echo "═══ [5/5] Full pytest ═══"
 PYTHONPATH=. python3 -m pytest -q tests/ 2>&1 || true

 echo ""
 echo "══════════════════════════════════════════"
 echo "RC1 Audit Full Verify Complete"
 echo "══════════════════════════════════════════"
} 2>&1 | tee "$LOG"

echo ""
echo "log_path=$LOG"
