"""B-Matrix PIT Builder v3.5 — valuation downgrade system, no hard vs gate"""
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

def _compute_pe_pb(s, pit_features):
    """Compute PE/PB from close + eps/bps when not directly available."""
    pe = s.get("pe"); pb = s.get("pb")
    valuation_method = "DIRECT_PE_PB" if (pe is not None or pb is not None) else "NONE"
    derived = False
    if (pe is None or pb is None) and pit_features:
        close = None
        feat = pit_features.get("features",{}) if isinstance(pit_features,dict) else {}
        close = feat.get("close")
        if close is None:
            ps = pit_features.get("price_snapshot",{}) if isinstance(pit_features,dict) else {}
            close = ps.get("close")
        eps = s.get("eps")
        bps_val = s.get("bps")
        if close and eps and eps > 0:
            pe = round(close / eps, 2)
            derived = True
        if close and bps_val and bps_val > 0:
            pb = round(close / bps_val, 2)
            derived = True
    if derived:
        valuation_method = "DERIVED_FROM_EPS_BPS"
    elif pe is None and pb is None:
        valuation_method = "MISSING"
    return pe, pb, valuation_method


def build_b_matrix_pit(*, ticker, replay_date, local_data_root, pit_features=None):
    fund = load_pit_fundamental_snapshot(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root)
    if fund.get("snapshot_status") != "READY":
        return {"matrix_version":"B_MATRIX_PIT_V10","status":"FAIL","base_role_eligible":False,
                "financial_hard_gate_passed":False,"quality_score":0,"growth_score":0,"valuation_score":0,
                "b_score":0,"role_cap":"D_REJECT",
                "valuation_data_status":"MISSING","valuation_confidence":"NONE","valuation_method":"UNAVAILABLE",
                "reason_codes":["FUNDAMENTAL_DATA_MISSING"],"downgrade":{"downgraded":True,"downgrade_reason":"FUNDAMENTAL_DATA_MISSING","from_role_cap":"A_LONG_CORE","to_role_cap":"D_REJECT"},
                "source_fundamentals":fund,"safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}

    s = fund.get("snapshot",{})
    qs = int((_sp(s.get("roe"),8,15)+_sp(s.get("gross_margin"),20,35)+_si(s.get("debt_ratio"),45,75))/3)
    gs = int((_sp(s.get("revenue_yoy"),5,20)+_sp(s.get("profit_yoy"),5,20))/2)

    pe, pb, valuation_method = _compute_pe_pb(s, pit_features)
    vs = 0
    if pe is not None and 0<pe<=50: vs+=50
    if pb is not None and 0<pb<=8: vs+=50

    # Data quality assessment
    has_quality = s.get("roe") is not None or s.get("gross_margin") is not None or s.get("debt_ratio") is not None
    has_growth = s.get("revenue_yoy") is not None or s.get("profit_yoy") is not None
    has_valuation = pe is not None or pb is not None
    valuation_confidence = "HIGH" if has_valuation else ("MEDIUM" if valuation_method=="DERIVED_FROM_EPS_BPS" else "NONE")

    total = int(qs*0.45+gs*0.35+vs*0.20)

    # Gate logic: removed vs>=30 hard gate
    quality_gate = qs >= 50
    growth_gate = gs >= 40
    hgp = quality_gate and growth_gate

    # Role cap based on data completeness
    if not has_quality:
        status = "FAIL"; role_cap = "D_REJECT"; reason = "QUALITY_DATA_MISSING"
        eligible = False
    elif not hgp:
        status = "FAIL"; role_cap = "D_REJECT"; reason = "B_MATRIX_HARD_GATE_FAILED"
        eligible = False
    elif not has_valuation:
        status = "DEGRADED"; role_cap = "B_MID_ROTATION"; reason = "VALUATION_DATA_MISSING"
        eligible = True
    elif valuation_method == "DERIVED_FROM_EPS_BPS":
        status = "PASS"; role_cap = "A_LONG_CORE"; reason = "B_MATRIX_BASE_ELIGIBLE"
        eligible = True
    else:
        status = "PASS"; role_cap = "A_LONG_CORE"; reason = "B_MATRIX_BASE_ELIGIBLE"
        eligible = True

    # Downgrade record
    downgraded = role_cap != "A_LONG_CORE"
    rc = [reason]
    if valuation_method == "DERIVED_FROM_EPS_BPS": rc.append("VALUATION_DERIVED_FROM_EPS_BPS")
    if not has_valuation: rc.append("VALUATION_DATA_MISSING_FALLBACK")

    return {"matrix_version":"B_MATRIX_PIT_V10","status":status,"base_role_eligible":eligible,
            "financial_hard_gate_passed":hgp,"quality_score":qs,"growth_score":gs,"valuation_score":vs,
            "b_score":total,"role_cap":role_cap,
            "valuation_data_status":"READY" if has_valuation else ("PARTIAL" if valuation_method!="MISSING" else "MISSING"),
            "valuation_confidence":valuation_confidence,"valuation_method":valuation_method,
            "reason_codes":rc,
            "downgrade":{"downgraded":downgraded,"downgrade_reason":reason if downgraded else None,
                         "from_role_cap":"A_LONG_CORE","to_role_cap":role_cap if downgraded else None},
            "data_quality":{"has_quality_fields":has_quality,"has_growth_fields":has_growth,
                            "has_direct_pe_pb":has_valuation and valuation_method!="DERIVED_FROM_EPS_BPS",
                            "has_derived_pe_pb":valuation_method=="DERIVED_FROM_EPS_BPS",
                            "potential_pit_weakness":fund.get("potential_pit_weakness",False)},
            "source_fundamentals":fund,"safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
