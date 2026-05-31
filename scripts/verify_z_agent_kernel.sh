#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-Agent Kernel Verification ═══"

python3 -m compileall -q zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/agent/

echo ""
echo "═══ Runtime Ledger Empty Check ═══"
LEDGER_DIR="data/research_db/agent/ledgers"
for f in "$LEDGER_DIR"/*.jsonl; do
    [ ! -f "$f" ] && continue
    [ -s "$f" ] && { echo "FAIL: $(wc -c < "$f") bytes in $f"; exit 1; }
done
echo "✅ All runtime ledgers EMPTY"

python3 <<'PY_EOF'
from pathlib import Path

strict = [
 "real_trade_allowed=True", "broker_order_allowed=True", "runtime_enabled=True",
 "auto_buy_allowed=True", "auto_sell_allowed=True", "production_allowed=True",
 "production_strategy_modified=True", "allowed_scopes=['*']", 'allowed_scopes=["*"]',
 "zmatrix-agent-hmac-secret",
]

code_roots = ["zmatrix/agent", "data/research_db/agent"]
code_exts = {".py", ".json", ".jsonl"}

for root in code_roots:
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix in code_exts:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in strict:
                assert token not in text, f"CODE: {token} in {p}"

print("✅ Z-Agent Kernel forbidden scan PASS")
PY_EOF

echo "═══ Z-Agent Kernel PASS ═══"
