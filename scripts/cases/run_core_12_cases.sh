#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "$0")/../.." && pwd)"

echo "═══ Core 12 Ticker-Specific Golden Path Run ═══"
mkdir -p runtime_reports/cases/core_12

completed=0; failed=0

for case_id in CORE_001 CORE_002 CORE_003 CORE_004 CORE_005 CORE_006 CORE_007 CORE_008 CORE_009 CORE_010 CORE_011 CORE_012; do
  if PYTHONPATH=. python3 scripts/cases/run_golden_path_case.py --case-id "$case_id" --dry-run 2>/dev/null; then
    completed=$((completed+1))
  else
    failed=$((failed+1))
    echo "  $case_id: PIPELINE_ERROR"
  fi
done

echo ""
echo "═══ Core 12 Summary ═══"
echo "  Attempted: 12 | Completed: $completed | Failed: $failed"
echo "═══ Core 12 Complete ═══"
