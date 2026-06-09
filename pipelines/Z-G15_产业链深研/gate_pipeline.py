#!/usr/bin/env python3
"""☯️ Z-G15 产业链深研 — v1.1 | 实时数据 | B/R/D矩阵+同行比对+催化剂日历"""
import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
TZ = timezone(timedelta(hours=8))

try:
    from pipelines.z17_loader import market_truth, get_financials, get_kline, dq_score, l4_health
    from pipelines.bmatrix_input_builder import build_bmatrix_input
    from zmatrix.scoring.b_matrix import evaluate_b_matrix
    from pipelines.chain_taxonomy_provider import match_chain_detail
    _HAS_ALL = True
except ImportError as e:
    market_truth = lambda t: {"status":"stub","name":"?"}; get_financials = lambda t: {}
    get_kline = lambda t,d: {"prices":[],"count":0}; dq_score = lambda t: {"total":0}
    l4_health = lambda t: {"status":"stub"}; _HAS_ALL = False


def _get_sector_peers(industry):
    """获取同行业可比公司 (预置 TOP5)"""
    SECTOR_PEERS = {
        "机械设备": ["002050","300124","688017","002896","688160"],
        "有色金属": ["601899","601600","000630","600362","000807"],
        "电子":     ["002049","603986","300782","688981","300661"],
        "计算机":   ["000977","300308","300394","300502","002837"],
        "食品饮料": ["600519","000858","002304","600809","000568"],
        "电力":     ["600900","600025","600674","002039","600886"],
        "煤炭":     ["601898","601088","600188","601225","600348"],
    }
    for k, v in SECTOR_PEERS.items():
        if k in (industry or ""):
            return v
    return []


def _run_b_matrix(ticker, name):
    try:
        inp = build_bmatrix_input(ticker, name, market_truth, get_financials, dq_score, l4_health)
        bm = evaluate_b_matrix(inp)
        return {
            "score": round(bm.score_final*10, 1),
            "base_type": bm.base_type.value,
            "rating": bm.rating.value,
            "eligibility": bm.eligibility.value,
            "traps": bm.trap_flags,
        }
    except: return {"error": "B-Matrix unavailable"}


def _run_d_matrix(ticker, name, kl):
    try:
        from pipelines.dmatrix_payload_builder import build_dmatrix_payload
        from zmatrix.scoring.d_band.d_early_v22_scorer import evaluate_d_early_v22
        payload = build_dmatrix_payload(ticker, name, kl)
        r = evaluate_d_early_v22(payload)
        if hasattr(r, "to_dict"):
            rd = r.to_dict()
            return {"score": round(rd.get("final_score",0),1), "lifecycle": rd.get("stage_hint","D1")}
    except: return {"error": "D-Matrix unavailable"}


def run(tickers=None):
    now = datetime.now(TZ)
    tickers = tickers or ["002472","601899"]

    chain_detail = match_chain_detail(tickers[0], "", "") if _HAS_ALL else {}
    
    result = {"pipeline_signature":"Z-G15_产业链深研_v1.1","timestamp":now.isoformat(),
              "data_available": _HAS_ALL, "analyses":[], "sections":{}}

    print(f"\n☯️ Z-G15 产业链深研 — {', '.join(tickers)}")
    print(f"   数据源: {'B/R/D矩阵+同行比对+催化剂' if _HAS_ALL else '⚠️ stub'}")
    print("=" * 60)
    
    for t in tickers:
        g1 = market_truth(t); dq = dq_score(t); l4 = l4_health(t)
        fin = get_financials(t); kl = get_kline(t, 500)
        prices = kl.get("prices", [])
        name = g1.get("name", "?")
        industry = g1.get("industry", fin.get("industry", ""))
        chain = match_chain_detail(t, name, industry) if _HAS_ALL else {}
        
        analysis = {"ticker": t, "name": name, "industry": industry}
        
        print(f"\n{'='*60}")
        print(f"📋 {t} {name}")
        print(f"  行业: {industry} | 产业链: {chain.get('primary_chain','?')}")
        print(f"  价格: {g1.get('price','?')} | DQ: {dq.get('total',0)} | L4: {l4.get('status','?')}")
        
        # ── 1. B-Matrix 底仓评价 ──
        bm = _run_b_matrix(t, name)
        if "error" not in bm:
            print(f"\n  🔵 B-Matrix: {bm['base_type']} 评分{bm['score']} {bm['rating']}级 {bm['eligibility']}")
            if bm["traps"]:
                print(f"    🚩 质量陷阱: {', '.join(bm['traps'])}")
        analysis["b_matrix"] = bm
        
        # ── 2. D-Matrix 黑马基因 ──
        dm = _run_d_matrix(t, name, kl)
        if dm and "error" not in dm:
            print(f"  🟣 D-Matrix: 评分{dm['score']} 阶段{dm.get('lifecycle','?')}")
        analysis["d_matrix"] = dm
        
        # ── 3. R-Matrix 技术形态 ──
        if len(prices) >= 60:
            try:
                from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
                ra = rank_type_a_horizontal(t, name, prices)
                rb = rank_type_b_rising_channel(t, name, prices)
                best = ra if ra.score>=rb.score else rb
                print(f"  🟠 R-Matrix: {best.oscillation_type} 评分{best.score:.1f} {best.allowed_action}")
                analysis["r_matrix"] = {"score": round(best.score,1), "type": best.oscillation_type, "action": best.allowed_action}
            except Exception as e:
                analysis["r_matrix"] = {"error": str(e)[:80]}
        else:
            analysis["r_matrix"] = {"error": f"K线不足({len(prices)}日)"}
        
        # ── 4. 同行比对 ──
        peers = _get_sector_peers(industry)
        if peers:
            print(f"\n  📊 同行比对 ({len(peers)}家):")
            peer_data = []
            for pt in peers[:5]:
                pg = market_truth(pt) if _HAS_ALL else {}
                print(f"    {pt} {pg.get('name','?'):<8s} @{pg.get('price','?')}")
                peer_data.append({"ticker":pt,"name":pg.get("name","?"),"price":pg.get("price")})
            analysis["peers"] = peer_data
        
        # ── 5. 催化剂日历 ──
        catalysts = []
        evt_path = WORKSPACE.parent / "hermes" / "event_calendar.json"
        if evt_path.exists():
            try:
                events = json.loads(open(evt_path).read())
                end = now + timedelta(days=30)
                for date_str, evt in events.items():
                    try:
                        d = datetime.strptime(date_str, "%Y-%m-%d")
                        if now <= d <= end:
                            if evt.get("code") == t or evt.get("type") == "macro":
                                catalysts.append({"date":date_str,"event":evt.get("name",evt.get("type","?")),
                                                 "impact":evt.get("impact","?")})
                    except: pass
            except: pass
        if catalysts:
            print(f"\n  📅 未来30天催化剂 ({len(catalysts)}个):")
            for c in catalysts[:5]:
                print(f"    {c['date']}: {c['event']} ({c['impact']})")
        analysis["catalysts"] = catalysts
        
        # ── 6. 证据分层 ──
        fin_data = get_financials(t) if _HAS_ALL else {}
        evidence = {"A_确证":[],"B_佐证":[],"C_传闻":[],"D_风险":[]}
        
        if fin_data.get("has_finance"):
            evidence["A_确证"].append("财报可用")
        if fin_data.get("roe_5y_avg") and fin_data["roe_5y_avg"] > 10:
            evidence["A_确证"].append(f"ROE 5年均{fin_data['roe_5y_avg']:.1f}%>10%")
        if fin_data.get("pe_ttm") and fin_data["pe_ttm"] < 20:
            evidence["B_佐证"].append(f"PE {fin_data['pe_ttm']:.1f}x<20x")
        if dq.get("total",0) > 70:
            evidence["B_佐证"].append(f"DQ {dq['total']}分>70")
        if bm.get("traps"):
            evidence["D_风险"].extend(bm["traps"])
        if l4.get("status") == "BLOCK":
            evidence["D_风险"].append("L4 BLOCK")
        
        print(f"\n  📋 证据分层:")
        for level, items in evidence.items():
            if items:
                print(f"    {level}: {', '.join(items[:4])}")
        analysis["evidence"] = evidence

        # ── 7. 产业链深度分析 (L1-L5 + 拓扑 + 手工) ──
        try:
            from zmatrix.research.industry_chain_analyzer import analyze_industry_chain
            chain_analysis = analyze_industry_chain(
                ticker=t, name=name, industry=industry,
                financials=fin_data, peers=peer_data if peers else [],
                catalysts=catalysts, existing_evidence=evidence,
                chain_detail=chain,
            )
            ca = chain_analysis.to_dict()
            analysis["chain_analysis"] = ca
            print(f"\n  🔗 产业链深度:")
            print(f"    链位置: {ca['chain_position']} | 利润捕获: {ca['profit_capture_point']}")
            print(f"    研究置信: {ca['research_confidence']} | 瓶颈: {ca['bottleneck_status']}")
            print(f"    G18交接: 论点{ca['g18_handoff']['thesis_strength']} "
                  f"证据{ca['g18_handoff']['evidence_level']} "
                  f"催化{ca['g18_handoff']['catalyst_distance']} "
                  f"链风险{ca['g18_handoff']['chain_risk_score']}")
        except Exception as e:
            analysis["chain_analysis"] = {"error": str(e)[:120]}
            print(f"\n  ⚠️ 产业链深度分析失败: {e}")

        result["analyses"].append(analysis)
    
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G15 产业链深研 v1.1")
    p.add_argument("--tickers", type=str, default="002472,601899", help="逗号分隔代码")
    args = p.parse_args()
    run(args.tickers.split(","))
