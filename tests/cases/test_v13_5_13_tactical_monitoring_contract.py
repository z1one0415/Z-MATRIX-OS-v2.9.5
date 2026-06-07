"""V13.5.13 Tactical Monitoring Contract — tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
c=L("v13_5_13_tactical_monitoring_contract.json")
def test_exists():assert c
def test_horizons():assert c.get("monitoring_horizons")==["20D"]
def test_no_trade():assert c.get("trade_signal_generation_prohibited")is True
def test_alpha():assert c.get("alpha_claim_allowed")is False
def test_prod():assert c.get("production")=="BLOCKED"
