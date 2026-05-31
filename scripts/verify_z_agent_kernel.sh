#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-Agent Kernel Verification ═══"

python3 -m compileall -q zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/agent/

python3 <<'PY_EOF'
from pathlib import Path

strict_forbidden = [
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

broad_forbidden = [
 "real_trade_allowed=True",
 "broker_order_allowed=True",
 "runtime_enabled=True",
 "auto_buy_allowed=True",
 "auto_sell_allowed=True",
 "production_allowed=True",
 "production_strategy_modified=True",
 "zmatrix-agent-hmac-secret",
]

code_roots = ["zmatrix/agent", "data/research_db/agent"]
code_exts = {".py", ".json", ".jsonl"}

doc_roots = ["docs/agent"]
doc_exts = {".md", ".yaml", ".yml"}

for root in code_roots:
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix in code_exts:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in strict_forbidden:
                assert token not in text, f"CODE: {token} in {p}"

for root in doc_roots:
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix in doc_exts:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in broad_forbidden:
                assert token not in text, f"DOC: {token} in {p}"

print("✅ Z-Agent Kernel forbidden scan PASS")
PY_EOF

echo "═══ Z-Agent Kernel PASS ═══"
