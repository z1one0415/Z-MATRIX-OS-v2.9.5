#!/usr/bin/env bash
set -euo pipefail

echo "═══ RC1 Cloud Evidence Lock Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 scripts/verify_rc1_cloud_evidence_lock.py

echo "═══ RC1 Cloud Evidence Lock PASS ═══"
