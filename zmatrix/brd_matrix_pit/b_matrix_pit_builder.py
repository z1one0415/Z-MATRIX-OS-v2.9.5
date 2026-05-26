"""B-Matrix PIT Builder — financial quality from PIT fundamentals"""
from __future__ import annotations
from zmatrix.brd_matrix_pit.fundamentals_pit_loader import load_pit_fundamental_snapshot
from zmatrix.brd_matrix_pit.schema import DEFAULT_BRD_MATRIX_PIT_SAFETY

def _sp(x, g=20, e=30):
    if x is None: return 0
    if x>=e: return 100
    if x>=g: return 75
    if x>0: return 50
    return 0

def _si(x, g=40, b=70):
    if x is None: return 0
    if x<=g: return 100
    if x<=b: return 50
    return 0

def build_b_matrix_pit(*, ticker, replay_date, local_data_root, pit_features=None):
    fund = load_pit_fundamental_snapshot(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root)
    if fund.get("snapshot_status") != "READY":
        return {"matrix_version":"B_MATRIX_PIT_V10","status":"FAIL","base_role_eligible":False,
                "financial_hard_gate_passed":False,"quality_score":0,"growth_score":0,"valuation_score":0,
                "reason_codes":["FUNDAMENTAL_DATA_MISSING"],"source_fundamentals":fund,
                "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
    s = fund.get("snapshot",{})
    qs = int((_sp(s.get("roe"),8,15)+_sp(s.get("gross_margin"),20,35)+_si(s.get("debt_ratio"),45,75))/3)
    gs = int((_sp(s.get("revenue_yoy"),5,20)+_sp(s.get("profit_yoy"),5,20))/2)
    pe = s.get("pe"); pb = s.get("pb")
    vs = 0
    if pe is not None and 0<pe<=50: vs+=50
    if pb is not None and 0<pb<=8: vs+=50
    total = int(qs*0.45+gs*0.35+vs*0.20)
    hgp = qs>=50 and gs>=40 and vs>=30
    eligible = hgp and total>=60
    rc = []
    if not hgp: rc.append("B_MATRIX_HARD_GATE_FAILED")
    if eligible: rc.append("B_MATRIX_BASE_ELIGIBLE")
    return {"matrix_version":"B_MATRIX_PIT_V10","status":"PASS" if eligible else "FAIL",
            "base_role_eligible":eligible,"financial_hard_gate_passed":hgp,
            "quality_score":qs,"growth_score":gs,"valuation_score":vs,"b_score":total,
            "reason_codes":rc,"source_fundamentals":fund,
            "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
