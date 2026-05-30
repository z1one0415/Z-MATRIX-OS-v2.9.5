#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 1 Account Truth Verification ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/research_db/account_truth/ tests/research_db/account_truth/

echo ""
echo "[1] Phase 0 baseline..."
bash scripts/verify_research_db_phase0.sh

echo ""
echo "[2] Private data guardrail..."
PYTHONPATH=. python3 -m pytest -q tests/research_db/account_truth/test_private_data_guardrail.py

echo ""
echo "[3] Account truth schema..."
python3 -c "
from zmatrix.research_db.account_truth import TradeRecord, PositionRecord, AccountSnapshot, CashflowRecord, DataStatus, QualityStatus
from zmatrix.research_db.account_truth import TradeSide, CashflowType, DecisionType, WatchStatus, ExitReason
print('  ✅ all schemas importable')
"

echo ""
echo "[4] Normalizers..."
python3 -c "
from zmatrix.research_db.account_truth.trade_normalizer import normalize_trade, normalize_trades
from zmatrix.research_db.account_truth.position_normalizer import normalize_position, normalize_positions
from zmatrix.research_db.account_truth.cashflow_normalizer import normalize_cashflow, normalize_cashflows
from zmatrix.research_db.account_truth.account_snapshot_normalizer import normalize_snapshot, normalize_snapshots
print('  ✅ all normalizers')
"

echo ""
echo "[5] Reconciler + capital curve..."
python3 -c "
from zmatrix.research_db.account_truth.account_reconciler import reconcile_trade_amount, reconcile_equity
from zmatrix.research_db.account_truth.capital_curve_builder import build_capital_curve
from zmatrix.research_db.account_truth.holding_pnl_builder import build_holding_pnl
from zmatrix.research_db.account_truth.drawdown_calculator import calculate_drawdowns
print('  ✅ all builders')
"

echo ""
echo "[6] Fixtures..."
python3 -c "
from pathlib import Path
for f in ['sample_trades.csv','sample_positions.csv','sample_cashflows.csv','sample_account_snapshots.csv']:
    assert Path('tests/fixtures/account_truth',f).exists(), f'missing {f}'
print('  ✅ 4 fixtures')
"

echo ""
echo "[7] Full pytest..."
PYTHONPATH=. python3 -m pytest -q tests/research_db/account_truth/

echo ""
echo "[8] Safety scan..."
python3 - <<'PY'
from pathlib import Path
for p in Path("zmatrix/research_db/account_truth").rglob("*.py"):
    c = p.read_text(encoding="utf-8", errors="ignore")
    for f in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        if f in c and "allowlist:" not in c:
            raise SystemExit(f"FORBIDDEN {f} in {p}")
print("  ✅ 0 forbidden flags")
PY

echo ""
echo "[9] Private data not tracked..."
python3 -c "
import subprocess
r = subprocess.run(['git','ls-files'], capture_output=True, text=True)
for bad in ['.xlsx','.xls','.csv.raw']:
    tracked = [l for l in r.stdout.split(chr(10)) if l.endswith(bad)]
    assert len(tracked)==0, f'tracked {bad}'
print('  ✅ no private data tracked')
"

echo ""
echo "[10] Acceptance + Closeout..."
test -f docs/research_db/PHASE1_ACCEPTANCE_MATRIX.md && echo "  ✅ acceptance matrix"
test -f docs/research_db/PHASE1_CLOSEOUT_REPORT.md && echo "  ✅ closeout report"

echo ""
echo "═══ ResearchDB Phase 1 Account Truth PASS ═══"
