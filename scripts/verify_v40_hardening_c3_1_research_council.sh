#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-1 Research Council Verify ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/research_council/ 2>&1 | tail -1

PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c3_reviewers.py
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c_integration.py -k "reviewer"

python3 - <<'PY'
from pathlib import Path
import json, importlib, pkgutil
import zmatrix.research_council.reviewers as pkg

# 1. 12 reviewers via registry
from zmatrix.research_council.reviewers.reviewer_registry import get_registry, count_reviewers
r = get_registry()
assert count_reviewers() == 12, f"expected 12, got {count_reviewers()}"
ids = sorted(r.keys())
assert len(set(ids)) == 12, "duplicate reviewer IDs"

# 2. Scoring configs unique
configs = []
for _, mn, _ in pkgutil.iter_modules(pkg.__path__):
    if mn.startswith("r") and not mn.startswith("r0") and "_" not in mn[:4]:
        mod = importlib.import_module(f"zmatrix.research_council.reviewers.{mn}")
        if hasattr(mod, "SCORING_CONFIG"):
            configs.append(json.dumps(mod.SCORING_CONFIG, sort_keys=True))
assert len(set(configs)) == len(configs), f"not unique: {len(set(configs))}/{len(configs)}"

# 3. CouncilAggregator no trade output
from zmatrix.research_council.reviewers.council_aggregator import CouncilAggregator
result = CouncilAggregator.aggregate([])
assert result["real_trade_allowed"] == False
assert result["broker_order_allowed"] == False
assert result["council_status"] in ["DATA_INSUFFICIENT", "RESEARCH_SUPPORT", "RESEARCH_CONFLICT", "RISK_REVIEW_REQUIRED"]

# 4. Forbidden scan: only boolean flags
for p in Path("zmatrix/research_council/reviewers").rglob("*.py"):
    c = p.read_text()
    for bad in ["real_trade_allowed=True","broker_order_allowed=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        if bad in c and "allowlist:" not in c:
            raise AssertionError(f"FORBIDDEN {bad} in {p}")

# 5. Each r*.py must have real_trade_allowed=False in review()
for p in Path("zmatrix/research_council/reviewers").rglob("r*.py"):
    if p.name.startswith("r0") or p.name in ("reviewer_registry.py",):
        continue
    c = p.read_text()
    if "def review" in c:
        assert "real_trade_allowed=False" in c, f"{p}: missing real_trade_allowed=False"

print("✅ C3-1: 12 reviewers + unique scoring + council aggregator + 0 forbidden flags")
PY

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-1 PASS ═══"
