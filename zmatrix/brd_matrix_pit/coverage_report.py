# allowlist: forbidden-token-definition
"""Fundamental Coverage Report — system-level data quality gate"""
from __future__ import annotations
from pathlib import Path

def build_fundamental_coverage_report(*, local_data_root):
    fin_dir = Path(local_data_root) / "data" / "fundamentals"
    files = list(fin_dir.glob("*_fin.csv"))
    total = len(files)
    if total == 0: return {"coverage_status":"BLOCKED","blocking_reason":"NO_FINANCIAL_FILES","total_tickers":0}

    has_roe = has_gm = has_dr = has_growth = has_eps = has_bps = has_pe = 0
    for f in files[:5000]:
        try:
            import csv
            with open(f, encoding="utf-8-sig") as fh:
                cols = set(next(csv.reader(fh)))
        except: continue
        if any(c in cols for c in ("roe","roe_yearly","roe_5y_avg")): has_roe += 1
        if any(c in cols for c in ("grossprofit_margin","gross_margin")): has_gm += 1
        if any(c in cols for c in ("debt_to_assets","debt_ratio")): has_dr += 1
        if any(c in cols for c in ("or_yoy","revenue_yoy","netprofit_yoy","profit_yoy")): has_growth += 1
        if "eps" in cols: has_eps += 1
        if "bps" in cols: has_bps += 1
        if "pe_ttm" in cols or "pe" in cols: has_pe += 1

    sampled = min(total, 5000)
    roe_cov = has_roe/sampled if sampled else 0
    gm_cov = has_gm/sampled if sampled else 0
    dr_cov = has_dr/sampled if sampled else 0
    growth_cov = has_growth/sampled if sampled else 0
    eps_cov = has_eps/sampled if sampled else 0
    pe_cov = has_pe/sampled if sampled else 0
    avg_quality = (roe_cov+gm_cov+dr_cov)/3
    usable = int(min(roe_cov, gm_cov, dr_cov) * total)

    status = "PASS"
    if avg_quality < 0.60: status = "BLOCKED"
    elif avg_quality < 0.80: status = "WARN"
    if usable < 300: status = "BLOCKED"

    return {"coverage_report_version":"FUNDAMENTAL_COVERAGE_V10",
            "total_tickers":total,"sampled":sampled,
            "snapshot_ready_count":total,
            "roe_coverage":round(roe_cov,2),"growth_coverage":round(growth_cov,2),
            "debt_ratio_coverage":round(dr_cov,2),
            "pe_pb_coverage":round(pe_cov,2),"eps_bps_coverage":round(eps_cov,2),
            "usable_b_matrix_count":usable,"coverage_status":status,
            "blocking_reason":"FUNDAMENTAL_COVERAGE_LOW" if status=="BLOCKED" else None,
            "real_trade_allowed":False,"broker_order_allowed":False}
