"""Pre-Trade Checklist v1.0 tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.pre_trade_checklist import validate_pre_trade_checklist

def test_complete():
    r = validate_pre_trade_checklist({"stock_role":"B_MID_ROTATION","buy_logic_type":"ROTATION","sector_stage":"CONFIRMATION","financial_gate_passed":True,"valuation_overheated":False,"max_loss_after_entry":8,"invalidation_condition":"板块退潮","lower_risk_validation_action":"等回调"})
    assert r["checklist_complete"] is True; assert r["paper_trade_allowed"] is True
    print("✅ checklist: complete → paper_trade_allowed")

def test_missing_all_fields():
    r = validate_pre_trade_checklist({})
    assert r["checklist_complete"] is False; assert r["paper_trade_allowed"] is False; assert len(r["missing_items"]) >= 3
    print(f"✅ checklist: incomplete ({len(r['missing_items'])} missing)")

def test_valuation_overheated_blocks():
    r = validate_pre_trade_checklist({"stock_role":"A_LONG_CORE","buy_logic_type":"FUNDAMENTAL","sector_stage":"CONFIRMATION","financial_gate_passed":True,"valuation_overheated":True,"max_loss_after_entry":10,"invalidation_condition":"业绩miss","lower_risk_validation_action":"等Q3"})
    assert r["paper_trade_allowed"] is False; assert r["checklist_complete"] is False
    print("✅ checklist: valuation overheated blocks")

def test_no_forbidden():
    import json; r = validate_pre_trade_checklist({"stock_role":"A_LONG_CORE","buy_logic_type":"FUNDAMENTAL","sector_stage":"CONFIRMATION","financial_gate_passed":True,"valuation_overheated":False,"max_loss_after_entry":10,"invalidation_condition":"业绩miss","lower_risk_validation_action":"等Q3"})
    for t in ["BUY","SELL","AUTO_TRADE","MARKET_ORDER","BROKER_ORDER","REAL_TRADE"]:
        assert t not in json.dumps(r)
    print("✅ checklist: no forbidden tokens")

if __name__ == "__main__":
    test_complete(); test_missing_all_fields(); test_valuation_overheated_blocks(); test_no_forbidden()
    print("\n🏁 Pre-Trade Checklist — tests PASS")
