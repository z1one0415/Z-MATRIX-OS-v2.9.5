#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 3-A Market Baseline Verification ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/research_db/market_data/ tests/research_db/market_data/

echo ""
echo "[1] Phase 2 baseline..."
bash scripts/verify_research_db_phase2_master_data.sh

echo ""
echo "[2] Market data pytest..."
PYTHONPATH=. python3 -m pytest -q tests/research_db/market_data/

echo ""
echo "[3] Required modules..."
python3 -c "
from pathlib import Path
base = Path('zmatrix/research_db/market_data')
for name in ['market_schema.py','trading_calendar.py','price_bar_store.py','benchmark_registry.py','adjustment_factor_store.py','market_data_guardrail.py']:
    assert (base/name).exists(), f'missing {name}'
print('  ✅ 6 modules')
"

echo ""
echo "[4] Safety deep scan..."
python3 - <<'PY'
from pathlib import Path; import subprocess
base = Path("zmatrix/research_db/market_data")

for p in base.rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for forbidden in [
        "real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True",
        "auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True",
        "BUY","SELL","AUTO_EXECUTE","PLACE_ORDER","SEND_ORDER",
    ]:
        assert forbidden not in text, f"FORBIDDEN {forbidden} in {p}"

r = subprocess.run(["git","ls-files"], capture_output=True, text=True)
tracked = []
for line in r.stdout.splitlines():
    lower = line.lower()
    if "data/research_db/market_data/raw/" in lower and not lower.endswith(".gitkeep"):
        tracked.append(line)
    if "data/research_db/market_data/staging/" in lower and not lower.endswith(".gitkeep"):
        tracked.append(line)
    if "data/research_db/market_data/vendor/" in lower and not lower.endswith(".gitkeep"):
        tracked.append(line)
    if lower.endswith((".xlsx",".xls",".vendor.csv",".raw.csv")):
        tracked.append(line)
    for token in ["wind","choice","tushare","akshare","行情","日线","分钟","指数"]:
        if "data/research_db/market_data/" in lower and token in lower and not lower.endswith(".gitkeep"):
            tracked.append(line)
assert not tracked, f"private/vendor market data tracked: {tracked}"
print("  ✅ 0 violations (11 forbidden tokens + raw/staging/vendor/patterns)")
PY

echo ""
echo "[5] Documents..."
test -f docs/research_db/PHASE3_SCOPE_LOCK.md && echo "  ✅ scope lock"
test -f docs/research_db/PHASE3_ACCEPTANCE_MATRIX.md && echo "  ✅ acceptance matrix"
test -f docs/research_db/PHASE3_A_CLOSEOUT_REPORT.md && echo "  ✅ closeout"

echo ""
echo "═══ ResearchDB Phase 3-A Market Baseline PASS ═══"
