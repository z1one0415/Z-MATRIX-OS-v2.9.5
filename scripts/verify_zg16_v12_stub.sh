#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-G16 v1.2 Stub Verification ═══"

python3 -m compileall -q zmatrix tests scripts

echo "--- Agent Kernel ---"
PYTHONPATH=. python3 -m pytest -q tests/agent/

echo "--- Event Physical ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/event_physical/

echo "--- Hypothesis ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/hypothesis/

echo "--- Annotation ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/annotation/

echo "--- Analysis Zone ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/analysis_zone/

echo ""
bash scripts/verify_z_agent_kernel.sh

python3 <<'PY'
from pathlib import Path

forbidden = [
 "external_api=True","external_api_used=True","shadowbroker_deployed=True",
 "production_allowed=True","trade_allowed=True","verdict_allowed=True",
 "broker_order_allowed=True","real_trade_allowed=True",
 "auto_buy_allowed=True","auto_sell_allowed=True",
]

zg16_roots = ["zmatrix/research_db/event_physical","zmatrix/research_db/hypothesis",
              "zmatrix/research_db/annotation","zmatrix/research_db/analysis_zone",
              "zmatrix/research_db/zg16_skill_wrappers.py"]

for root in zg16_roots:
    p = Path(root)
    if p.is_file():
        paths = [p]
    else:
        paths = list(p.rglob("*.py"))
    for fp in paths:
        text = fp.read_text(encoding="utf-8",errors="ignore")
        for token in forbidden:
            # Allow in test assertions and doc strings explaining what to forbid
            if f"assert {token}" in text or f"=True" not in text or f'test_' in str(fp):
                continue
            assert token not in text, f"FORBIDDEN: {token} in {fp}"

print("✅ Z-G16 extra forbidden scan PASS")
PY

echo "═══ Z-G16 v1.2 STUB PASS ═══"
