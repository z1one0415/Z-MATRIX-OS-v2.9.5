"""月度轮动扫描 — Rotation King monthly trend classifier integrated with R-Matrix"""
from __future__ import annotations
import baostock as bs


def scan_monthly_rotation(tickers: list[str], names: dict | None = None) -> list[dict]:
    """扫描月度轮动信号"""
    from zmatrix.scoring.r_matrix.rotation_king_monthly import classify_monthly_trend
    if names is None: names = {}
    
    bs.login()
    results = []
    
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}",
            "date,close", start_date="2024-01-01", end_date=end_date or _today(),
            frequency="m", adjustflag="2")
        closes = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1] != '':
                closes.append(float(r[1]))
        
        if len(closes) < 6:
            results.append({"ticker": t, "name": names.get(t, "?"), "type": "DATA_INSUFFICIENT",
                           "beta_norm": 0, "channel_amp": 0, "position": 0.5, "action": "WAIT"})
            continue
        
        analysis = classify_monthly_trend(closes)
        results.append({
            "ticker": t,
            "name": names.get(t, "?"),
            **analysis,
        })
    
    bs.logout()
    return results


def _today(): from datetime import datetime; return datetime.now().strftime("%Y-%m-%d")

def scan_oscillation_king(tickers: list[str], end_date=None) -> list[dict]:
    """波动天王: 5日线 BOX hunter (17% BOX optimal)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date=end_date or _today(),frequency="d",adjustflag="2")
        all_c = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': all_c.append(float(r[1]))
        sampled = all_c[::5]
        if len(sampled)>=20:
            r = classify_rhythm(sampled, beta_threshold=0.002, box_amp_min=5, box_amp_max=200)
            results.append({"ticker":t,"king":"波动天王",**r})
    bs.logout()
    return results


def scan_rhythm_king(tickers: list[str], end_date=None) -> list[dict]:
    """律动天王: 周线 mid-term swing (30% BOX)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date=end_date or _today(),frequency="w",adjustflag="2")
        closes = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': closes.append(float(r[1]))
        if len(closes)>=20:
            r = classify_rhythm(closes, beta_threshold=0.004, box_amp_min=10, box_amp_max=150)
            results.append({"ticker":t,"king":"律动天王",**r})
    bs.logout()
    return results


def scan_rotation_king(tickers: list[str], end_date=None) -> list[dict]:
    """轮动天王: 双周线 rotation entry (13% BOX, 3x monthly entries)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date=end_date or _today(),frequency="d",adjustflag="2")
        all_c = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': all_c.append(float(r[1]))
        sampled = all_c[::10]
        if len(sampled)>=20:
            r = classify_rhythm(sampled, beta_threshold=0.004, box_amp_min=8, box_amp_max=200)
            results.append({"ticker":t,"king":"轮动天王",**r})
        else:
            results.append({"ticker":t,"king":"轮动天王","type":"DATA_INSUFFICIENT","position":0.5,"action":"WAIT"})
    bs.logout()
    return results


def scan_impulse_king(tickers: list[str], end_date=None) -> list[dict]:
    """冲动天王: 日线500K Type A/B oscillation — 日内超买超卖警报"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date=end_date or _today(),frequency="d",adjustflag="2")
        closes = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': closes.append(float(r[1]))
        if len(closes)>=260:
            ra = rank_type_a_horizontal(t,"",closes)
            rb = rank_type_b_rising_channel(t,"",closes)
            best = ra if ra.score>=rb.score else rb
            results.append({"ticker":t,"king":"冲动天王","type":best.oscillation_type,
                           "score":best.score,"action":best.allowed_action})
    bs.logout()
    return results
