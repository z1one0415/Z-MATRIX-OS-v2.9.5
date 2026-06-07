"""V13.5.13 Tactical Monitoring Closeout Safety — tests."""
import json,os;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
co=L("v13_5_13_tactical_monitoring_closeout.json")
def test_exists():assert co
def test_executed():assert co.get("v13_5_13_executed")is True
def test_no_v13_6():assert co.get("v13_6_prep_allowed")is False
def test_no_paper():assert co.get("paper_trading_allowed")is False
def test_alpha():assert co.get("alpha_claim_allowed")is False
def test_prod():assert co.get("production")=="BLOCKED"
def test_no_forbidden():
    for p in["v13_6_","paper_trading_","production_","broker_","real_trade_","alpha_"]:
        assert not any(f.startswith(p)for f in os.listdir(C)),f"found:{[f for f in os.listdir(C)if f.startswith(p)]}"
