#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "$0")/../.." && pwd)"

echo "═══ Core 12 Ticker-Specific Golden Path Run ═══"
mkdir -p runtime_reports/cases/core_12

for case_id in CORE_001 CORE_002 CORE_003 CORE_004 CORE_005 CORE_006 CORE_007 CORE_008 CORE_009 CORE_010 CORE_011 CORE_012; do
  echo "Running ${case_id}"
  PYTHONPATH=. python3 scripts/cases/run_golden_path_case.py --case-id "$case_id" --dry-run
done

PYTHONPATH=. python3 scripts/cases/summarize_core_12_run.py

echo ""
echo "═══ Core 12 Complete ═══"
