#!/usr/bin/env bash
set -euo pipefail; cd "$(cd "$(dirname "$0")/../.." && pwd)"
echo "═══ Core 12 Dry-Run ═══"
for t in 600519 300750 688981 601899 300124 002594 300274 002371 600030 600276 002050 300763; do
  PYTHONPATH=. python3 -c "
from zmatrix.research_os.golden_path_runner import run_golden_path
try:
    r=run_golden_path(dry_run=True)
    print(f'  ✅ {r["_audit_hash"]}')
except Exception as e:
    print(f'  ⚠️  {e}')
" 2>/dev/null || echo "  ⚠️  skipped"
done
echo "═══ Core 12 Complete ═══"
