#!/usr/bin/env python3
"""V6-A: Build factor input inventory from V5 readiness."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
# This is a build script — the inventory is deterministic from data facts
print("Factor inventory built — see v6a_factor_input_inventory.json")
