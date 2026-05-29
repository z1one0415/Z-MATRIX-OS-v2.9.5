#!/usr/bin/env bash
set -euo pipefail
echo "═══ RC1 Safety Gate Deep Scan ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"
python3 scripts/verify_rc1_safety_deep_scan.py
