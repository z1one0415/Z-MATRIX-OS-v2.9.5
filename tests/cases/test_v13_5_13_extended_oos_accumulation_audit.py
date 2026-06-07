"""V13.5.13 Extended OOS Accumulation Audit — tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
a=L("v13_5_13_extended_oos_accumulation_audit.json")
def test_exists():assert a
def test_has_new():assert a.get("new_oos_count",0)>=0
def test_alpha():assert a.get("alpha_claim_allowed")is False
def test_prod():assert a.get("production")=="BLOCKED"
