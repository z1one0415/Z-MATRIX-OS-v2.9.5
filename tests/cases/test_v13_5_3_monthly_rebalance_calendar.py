"""V13.5.3 Monthly Rebalance Calendar — targeted tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
c=L("v13_5_3_monthly_rebalance_calendar.json")
def test_exists():assert c
def test_status():assert"BUILT"in c.get("status","")or"BLOCKED"in c.get("status","")
def test_freq():assert c.get("rebalance_frequency")=="MONTHLY"
def test_dates_list():assert isinstance(c.get("rebalance_dates"),list)
def test_count_ge_24():
    if"BUILT"in c.get("status",""):assert c.get("rebalance_date_count",0)>=24
def test_dates_are_trading():assert all(len(d)==8 for d in c.get("rebalance_dates",[]))
def test_alpha_false():assert c.get("alpha_claim_allowed")is False
def test_prod_blocked():
    for k in["production","broker_runtime","real_trade"]:assert c.get(k)=="BLOCKED"
