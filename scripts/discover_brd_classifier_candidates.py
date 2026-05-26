#!/usr/bin/env python3
"""Discover B/R/D classifier candidates"""
from pathlib import Path
KEYWORDS = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT",
    "classify_stock_role","evaluate_b_matrix","evaluate_d_matrix","build_investment_role_review"]
for r in ["zmatrix/investment"]:
    for f in Path(r).rglob("*.py"):
        if "__pycache__" in str(f): continue
        text = f.read_text(encoding="utf-8",errors="ignore")
        matched = [k for k in KEYWORDS if k in text]
        if matched:
            # Check if the function is importable
            mod_path = str(f)[:-3].replace("/",".")
            try:
                mod = __import__(mod_path, fromlist=["*"])
                funcs = [k for k in matched if hasattr(mod, k)]
                print(f"✅ {mod_path}")
                for fn in funcs: print(f"   → {fn}() importable")
            except Exception as e:
                print(f"⚠️ {mod_path}: {str(e)[:60]}")
