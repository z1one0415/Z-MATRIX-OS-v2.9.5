#!/usr/bin/env python3
"""Load Core 12 market data — delegates to readiness checker (V4 read-only)."""
import subprocess, sys
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
from scripts.cases.check_core12_real_market_data_readiness import main
main()
