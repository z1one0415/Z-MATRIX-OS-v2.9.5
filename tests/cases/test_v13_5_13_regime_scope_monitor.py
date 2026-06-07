"""V13.5.13 Regime Scope Monitor — tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
m=L("v13_5_13_regime_scope_monitor.json")
def test_exists():assert m
def test_monitored():assert m.get("monitored_months",0)>0
def test_alpha():assert m.get("alpha_claim_allowed")is False
def test_prod():assert m.get("production")=="BLOCKED"
