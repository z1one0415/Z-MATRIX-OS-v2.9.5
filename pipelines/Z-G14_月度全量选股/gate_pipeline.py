#!/usr/bin/env python3
"""☯️ Z-G14 月度全量选股 (流A) — v2.1 | 每月 | B-Matrix v2.1.1 + R-Matrix v1.1 + D-Matrix v2.2 全量评分"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import market_truth, get_kline, get_financials, dq_score, l4_health, get_sectors
except: market_truth = lambda t: {"status":"stub"}; get_kline = get_financials = dq_score = l4_health = lambda t: {"status":"stub"}; get_sectors = lambda: {}

# ============================================================
# Real B-Matrix v2.1.1 scoring
# ============================================================
_B_MATRIX = None
def _get_b_matrix():
    global _B_MATRIX
    if _B_MATRIX is None:
        try:
            from zmatrix.scoring.b_matrix import BMatrixInput, evaluate_b_matrix
            _B_MATRIX = (BMatrixInput, evaluate_b_matrix)
        except ImportError:
            _B_MATRIX = (None, None)
    return _B_MATRIX

def _build_bmatrix_input(ticker, name):
    BMatrixInput, _ = _get_b_matrix()
    if BMatrixInput is None: return None
    g1 = market_truth(ticker)
    fin = get_financials(ticker) if get_financials else {}
    dq = dq_score(ticker) if dq_score else {"total":0}
    l4 = l4_health(ticker) if l4_health else {"status":"stub"}
    return BMatrixInput(
        symbol=ticker, name=name or g1.get("name",""),
        industry=g1.get("industry", fin.get("industry", "")),
        is_state_owned=fin.get("is_state_owned", False),
        is_market_leader=g1.get("is_market_leader", False),
        is_st=g1.get("is_st", False),
        suspended=l4.get("status") == "BLOCK",
        roe_5y=fin.get("roe_5y_avg"), roic_5y=fin.get("roic_5y"),
        pe_ttm=fin.get("pe_ttm"), pb=fin.get("pb"),
        dividend_yield=fin.get("dividend_yield"),
        debt_ratio=fin.get("debt_ratio"),
        ocf_3y=fin.get("ocf_3y"), net_profit_3y=fin.get("net_profit_3y"),
        brand_premium_score=fin.get("brand_premium_score"),
        pricing_power_score=fin.get("pricing_power_score"),
        supply_constraint_score=fin.get("supply_constraint_score"),
        gross_margin=fin.get("gross_margin"),
        cost_curve_score=fin.get("cost_curve_score"),
        resource_quality_score=fin.get("resource_quality_score"),
        asset_monopoly_score=fin.get("asset_monopoly_score"),
        profit_percentile_5y=fin.get("profit_percentile_5y"),
        policy_stability_score=fin.get("policy_stability_score"),
    )

# ============================================================
# Real R-Matrix v1.1 scoring
# ============================================================
_R_MATRIX = None
def _get_r_matrix():
    global _R_MATRIX
    if _R_MATRIX is None:
        try:
            from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
            _R_MATRIX = (rank_type_a_horizontal, rank_type_b_rising_channel)
        except ImportError:
            _R_MATRIX = (None, None)
    return _R_MATRIX

# ============================================================
# Real D-Matrix v2.2 scoring
# ============================================================
_D_MATRIX = None
def _get_d_matrix():
    global _D_MATRIX
    if _D_MATRIX is None:
        try:
            from zmatrix.scoring.d_band.d_early_v22_scorer import evaluate_d_early_v22
            _D_MATRIX = evaluate_d_early_v22
        except ImportError:
            _D_MATRIX = None
    return _D_MATRIX


def _real_b_score(ticker, name):
    """True B-Matrix v2.1.1 score — structured return"""
    _, evaluate_bm = _get_b_matrix()
    if evaluate_bm is None:
        return {"score": None, "status": "DATA_GAP", "base_type": None, "rating": None,
                "traps": [], "error": "B-Matrix scorer not available"}
    inp = _build_bmatrix_input(ticker, name)
    if inp is None:
        return {"score": None, "status": "DATA_GAP", "base_type": None, "rating": None,
                "traps": [], "error": "BMatrixInput build failed"}
    try:
        bm = evaluate_bm(inp)
        return {"score": round(bm.score_final * 10, 1), "status": "PASS",
                "base_type": bm.base_type.value, "rating": bm.rating.value,
                "traps": bm.trap_flags, "error": None}
    except Exception as e:
        return {"score": None, "status": "ERROR", "base_type": None, "rating": None,
                "traps": [], "error": str(e)[:120]}


def _real_r_score(ticker, name, prices):
    """True R-Matrix v1.1 score — structured return, never silent zero"""
    rank_a, rank_b = _get_r_matrix()
    if rank_a is None:
        return {"score": None, "status": "DATA_GAP", "subtype": None,
                "error": "R-Matrix scorer not available"}
    errors = []
    s_a, s_b = 0, 0
    try:
        ra = rank_a(ticker, name, prices)
        s_a = ra.score
    except Exception as e:
        errors.append(f"TypeA: {str(e)[:80]}")
    try:
        rb = rank_b(ticker, name, prices)
        s_b = rb.score
    except Exception as e:
        errors.append(f"TypeB: {str(e)[:80]}")
    if errors and s_a == 0 and s_b == 0:
        return {"score": None, "status": "ERROR", "subtype": None,
                "error": "; ".join(errors)}
    best_type = "A" if s_a >= s_b else "B"
    status = "DEGRADED" if errors else "PASS"
    return {"score": round(max(s_a, s_b) * 10, 1), "status": status,
            "subtype": best_type, "error": "; ".join(errors) if errors else None}


def _real_d_score(ticker, name, prices, kl):
    """True D-Matrix v2.2 score — structured return, never silent zero"""
    evaluate_d = _get_d_matrix()
    if evaluate_d is None:
        return {"score": None, "status": "DATA_GAP", "lifecycle": None,
                "error": "D-Matrix scorer not available"}
    try:
        from pipelines.dmatrix_payload_builder import build_dmatrix_payload
        payload = build_dmatrix_payload(ticker, name, kl)
        result = evaluate_d(payload)
        if hasattr(result, "to_dict"):
            rd = result.to_dict()
            return {"score": round(rd.get("final_score", 0), 1), "status": "PASS",
                    "lifecycle": rd.get("stage_hint", "D1"), "error": None}
        return {"score": float(result), "status": "PASS", "lifecycle": "D1", "error": None}
    except Exception as e:
        return {"score": None, "status": "ERROR", "lifecycle": None, "error": str(e)[:120]}


def _full_scan(tickers):
    """B-R-D 全量三维评分 — 使用真 B-Matrix v2.1.1 / R-Matrix v1.1 / D-Matrix v2.2"""
    candidates = []
    for t in tickers:
        g1 = market_truth(t)
        l4 = l4_health(t)
        if g1.get("status") == "BLOCK" or l4.get("status") == "BLOCK":
            continue
        kl = get_kline(t, 500)
        prices = kl.get("prices", [])
        if len(prices) < 60:
            continue

        name = g1.get("name", "")

        # --- B-Matrix v2.1.1 ---
        b = _real_b_score(t, name)
        # --- R-Matrix v1.1 ---
        r = _real_r_score(t, name, prices)
        # --- D-Matrix v2.2 ---
        d = _real_d_score(t, name, prices, kl)

        b_final = b["score"] if b["score"] is not None else 0
        r_final = r["score"] if r["score"] is not None else 0
        d_final = d["score"] if d["score"] is not None else 0

        # Weighted total with explicit scale
        weighted_total = round(b_final * 0.34 + r_final * 0.33 + d_final * 0.33, 2)

        # --- Cross matrix ---
        b_ok = b_final > 40
        r_ok = r_final > 20
        d_ok = d_final > 30
        cross = []
        if b_ok and d_ok: cross.append("B∩D☆")
        if b_ok and r_ok: cross.append("B∩R★")
        if d_ok and r_ok: cross.append("D∩R◇")
        if b_ok and not r_ok and not d_ok: cross.append("纯B")
        if d_ok and not b_ok and not r_ok: cross.append("纯D")
        if r_ok and not b_ok and not d_ok: cross.append("纯R")
        if not cross: cross.append("观察")

        # Confidence when any scorer had errors or data gaps
        statuses = [b["status"], r["status"], d["status"]]
        if "ERROR" in statuses:
            confidence = "DEGRADED_MATRIX_ERROR"
        elif "DATA_GAP" in statuses:
            confidence = "DEGRADED_MATRIX_DATA_GAP"
        elif "DEGRADED" in statuses:
            confidence = "DEGRADED_MATRIX_PARTIAL"
        else:
            confidence = "PASS"

        candidates.append({
            "code": t, "name": name,
            "b": b_final, "r": r_final, "d": d_final,
            "b_type": b.get("base_type"), "b_rating": b.get("rating"),
            "r_subtype": r.get("subtype"), "d_lifecycle": d.get("lifecycle"),
            "b_traps": b.get("traps", []),
            "score_status": {"b": b["status"], "r": r["status"], "d": d["status"]},
            "score_scale": {"b": "0-100", "r": "0-100", "d": "0-100"},
            "weighted_total": weighted_total, "total": b_final + r_final + d_final,
            "cross": cross[0], "confidence": confidence,
            "price": g1.get("price"),
        })
    return candidates


# _scan_list() removed — use pipelines.universe_provider.load_universe() instead



def run():
    """Z-G14 月度全量选股 — 强制A_SHARE_ALL, 失败DATA_GAP, 不fallback"""
    from pipelines.universe_provider import load_universe
    
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G14_月度全量_BRD_v2.1","timestamp":now.isoformat(),"sections":{}}
    
    uni = load_universe(source="A_SHARE_ALL", allow_fallback=False, min_count=4000)
    result["universe_contract"] = uni
    
    # Sanity check: Z-G14 must have real global universe
    if uni["status"] == "DATA_GAP" or uni["count"] < 4000 or not uni.get("is_global"):
        result["status"] = "DATA_GAP"
        result["sections"]["universe"] = {
            "status": "REJECTED",
            "reason": "Z-G14 requires A_SHARE_ALL with count>=4000, is_global=True",
            "actual": uni,
        }
        result["candidates"] = []
        print(f"\n⛔ Z-G14 月度全量选股 — UNIVERSE_UNAVAILABLE")
        print(f"   {uni['source']}: {uni['count']}只 is_global={uni.get('is_global')}")
        return result
    
    tickers = uni["tickers"]

    print(f"\n☯️ Z-G14 月度全量选股 (流A) — {now.strftime('%Y-%m')}")
    print(f"    A_SHARE_ALL {uni['count']}只 → 防局部视角陷阱")
    print("⚠️ 目的: B-Matrix v2.1.1 + R-Matrix v1.1 + D-Matrix v2.2 全量评分 + 交叉矩阵 + 产业链映射")
    print("=" * 60)
    print(f"\n📡 扫描: {len(tickers)}标的 → 真实B/R/D三维评分 (非简化quick_scan)")

    candidates = _full_scan(tickers)
    candidates.sort(key=lambda x: x.get("weighted_total", x.get("total", 0)), reverse=True)

    # 交叉统计
    cross_counts = {}
    for c in candidates: cross_counts[c["cross"]] = cross_counts.get(c["cross"], 0) + 1

    print(f"\n📊 交叉矩阵:")
    for k, v in sorted(cross_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}只")

    # TOP15
    top15 = candidates[:15]
    print(f"\n🏆 TOP15终选:")
    for i, c in enumerate(top15):
        meta = f" B={c.get('b_type','')}/{c.get('b_rating','')}" if c.get("b_type") else ""
        print(f"  {i+1:2d}. {c['code']} {c['name']:<8s} B={c['b']:.0f} R={c['r']:.0f}({c.get('r_subtype','')}) D={c['d']:.0f}({c.get('d_lifecycle','')}) [{c['cross']}] w={c.get('weighted_total',0):.1f} raw={c.get('total',0):.0f}")

    # 产业链映射
    chains = {"机器人":"双环|雷赛|绿的|三花|步科|兆威|奥比|柯力",
              "AI算力":"中际|天孚|新易盛|寒武纪|海光|浪潮|华工|沪电|中贝|英维克|高澜|美格|恒玄",
              "半导体":"688|002049|603986|300782",
              "资源":"紫金|中煤|黄金|601899|601898",
              "消费":"600519|000858|002304"}
    chain_hits = {}
    for c in candidates[:50]:
        for ch, kw in chains.items():
            if any(k in c["name"] for k in kw.split("|")):
                chain_hits[ch] = chain_hits.get(ch, 0) + 1

    print(f"\n🔗 产业链浓度 (TOP50):")
    for ch in chains:
        h = chain_hits.get(ch, 0)
        flag = "⚠️盲区" if h == 0 else f"{h}只"
        print(f"  {ch}: {flag}")

    result["candidates"] = candidates[:30]
    result["sections"]["cross_matrix"] = cross_counts
    result["sections"]["chain_density"] = chain_hits
    result["sections"]["scorer_versions"] = {
        "b_matrix": "v2.1.1 (5-class heterogeneous)",
        "r_matrix": "v1.1 (Type A/B dual mode)",
        "d_matrix": "v2.2 (DEarlyV22Result)",
        "scan_tickers": len(tickers),
        "scanned": len(candidates),
    }
    return result

if __name__ == "__main__":
    run()
