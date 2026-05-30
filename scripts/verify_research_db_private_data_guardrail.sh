#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Private Data Guardrail ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

echo "[1] git ls-files scan..."
VIOLATIONS=0

# Check raw/ staging/ paths
check_path() {
    local pattern="$1"
    local hits
    hits=$(git ls-files | grep "$pattern" || true)
    # Allow sample fixtures and templates
    hits=$(echo "$hits" | grep -v "tests/fixtures/" | grep -v "templates/" | grep -v "schema/" | grep -v ".gitkeep" || true)
    if [ -n "$hits" ]; then
        echo "  ❌ found: $pattern"
        echo "$hits" | head -5
        VIOLATIONS=1
    fi
}

for pattern in \
    "data/research_db/account/raw/" \
    "data/research_db/account/staging/" \
    ".xlsx" \
    ".xls" \
    ".csv.raw" \
    "broker" \
    "export_20" \
; do
    check_path "$pattern"
done

# Check Chinese-named broker exports
for kw in "交易" "成交" "持仓" "资金"; do
    hits=$(git ls-files | grep "$kw" | grep -v "tests/fixtures/" | grep -v "templates/" || true)
    if [ -n "$hits" ]; then
        echo "  ❌ found: *${kw}*"
        echo "$hits" | head -5
        VIOLATIONS=1
    fi
done

if [ "$VIOLATIONS" -eq 0 ]; then
    echo "  ✅ all patterns clean"
    echo "═══ ResearchDB Private Data Guardrail PASS ═══"
else
    echo "═══ ResearchDB Private Data Guardrail FAILED ═══"
    exit 1
fi
