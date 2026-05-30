#!/usr/bin/env bash
set -euo pipefail
echo "═══ ResearchDB Phase 3-B Outcome Horizon Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 -m compileall zmatrix/research_db/market_data/ tests/research_db/market_data/
bash scripts/verify_research_db_phase3a_market_baseline.sh
PYTHONPATH=. python3 -m pytest -q tests/research_db/market_data/

python3 - <<'PY'
from pathlib import Path
base = Path("zmatrix/research_db/market_data")
for name in ["outcome_schema.py","outcome_horizon_engine.py","outcome_readiness_gate.py","outcome_fixture_builder.py"]:
    assert (base/name).exists(), f"missing {name}"
combined = "\n".join((base/n).read_text() for n in ["outcome_schema.py","outcome_horizon_engine.py","outcome_readiness_gate.py"])
for tok in ["T1","T5","T10","T20","T60","INSUFFICIENT_FORWARD_DAYS","MISSING_ENTRY_BAR","MISSING_EXIT_BAR","SUSPENDED_ENTRY","SUSPENDED_EXIT","fallback_used"]:
    assert tok in combined, f"missing: {tok}"
for forbidden in ["return_pct","benchmark_relative_return","commission","stamp_duty","slippage","real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","production_allowed=True","BUY","SELL","AUTO_EXECUTE","PLACE_ORDER","SEND_ORDER"]:
    assert forbidden not in combined, f"FORBIDDEN {forbidden}"
print("✅ Phase 3-B outcome horizon static scan PASS")
PY
test -f docs/research_db/PHASE3_B_CLOSEOUT_REPORT.md
echo "═══ ResearchDB Phase 3-B Outcome Horizon PASS ═══"
