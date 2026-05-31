#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-Agent Kernel Verification ═══"

python3 -m compileall -q zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/agent/

python3 <<'PY'
from pathlib import Path

forbidden = [
 "real_trade_allowed=True",
 "broker_order_allowed=True",
 "runtime_enabled=True",
 "auto_buy_allowed=True",
 "auto_sell_allowed=True",
 "production_allowed=True",
 "production_strategy_modified=True",
 "allowed_scopes=['*']",
 'allowed_scopes=["*"]',
]

scan_roots = ["zmatrix/agent", "docs/agent", "scripts", "data/research_db/agent"]
scan_exts = {".py", ".md", ".sh", ".json", ".jsonl", ".yaml", ".yml"}

for root in scan_roots:
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix in scan_exts:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                assert token not in text, f"Forbidden token {token} in {p}"

print("✅ Z-Agent Kernel forbidden scan PASS")
PY

echo "═══ Z-Agent Kernel PASS ═══"
