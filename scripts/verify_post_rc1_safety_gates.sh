#!/usr/bin/env bash
set -euo pipefail

echo "═══ Post-RC1 Safety Gate Re-Scan ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

bash scripts/verify_rc1_safety_deep_scan.sh
bash scripts/verify_v40_rc1_tag_and_release.sh

python3 - <<'PY'
from pathlib import Path

SKIP_DIRS = {"scripts", "docs", "tests", "data", ".github", "runtime_reports"}
for p in Path("zmatrix").rglob("*.py"):
    c = p.read_text(encoding="utf-8", errors="ignore")
    if "allowlist: forbidden" in c or "Allowlist: forbidden" in c:
        continue
    for token in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
    ]:
        if token in c:
            raise AssertionError(f"FORBIDDEN {token} in {p}")

print("✅ Post-RC1 safety gates PASS — zmatrix/ clean")
PY

echo "═══ Post-RC1 Safety Gate Re-Scan PASS ═══"
