#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "$0")/../.." && pwd)"
echo "═══ Core 12 Ticker-Specific Golden Path Run ═══"
completed=0; data_gap=0; error=0
results="["
for case_id in CORE_001 CORE_002 CORE_003 CORE_004 CORE_005 CORE_006 CORE_007 CORE_008 CORE_009 CORE_010 CORE_011 CORE_012; do
  output=$(PYTHONPATH=. python3 scripts/cases/run_golden_path_case.py --case-id "$case_id" --dry-run 2>&1)
  ticker=$(echo "$output" | sed -n 's/.*Ticker: //p' | awk '{print $1}')
  status=$(echo "$output" | sed -n 's/.*Status: //p' | awk '{print $1}')
  hash=$(echo "$output" | sed -n 's/.*Hash: //p' | awk '{print $1}')
  echo "  $case_id: ticker=$ticker status=$status hash=$hash"
  case "$status" in
    COMPLETED) completed=$((completed+1)) ;;
    DATA_GAP) data_gap=$((data_gap+1)) ;;
    *) error=$((error+1)) ;;
  esac
  results="${results}{\"case_id\":\"$case_id\",\"ticker\":\"$ticker\",\"status\":\"$status\",\"hash\":\"$hash\"},"
done
results="${results%,}]"
mkdir -p runtime_reports/cases/core_12
cat > runtime_reports/cases/core_12_summary.json << JSONEOF
{
 "status": "CORE_12_TICKER_SPECIFIC_ATTEMPTED",
 "attempted": 12,
 "completed": $completed,
 "data_gap": $data_gap,
 "pipeline_error": $error,
 "ticker_specific": true,
 "runner_parameterized": true,
 "results": $results,
 "production": "BLOCKED",
 "broker_runtime": "BLOCKED",
 "real_trade": "BLOCKED"
}
JSONEOF
echo ""
echo "═══ Core 12 Summary: Attempted=12 Completed=$completed Error=$error ═══"
