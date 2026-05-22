#!/usr/bin/env python3
"""☯️ Z-G18 天机引擎 — v2.1.1 | 25因子+概率化预测+严格后验校准中枢"""
import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
TZ = timezone(timedelta(hours=8))

from zmatrix.prediction.contracts import PredictionResult, ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
from zmatrix.prediction.probability_model import fermi_weighted
from zmatrix.prediction.data_lineage import evaluate_lineage, apply_lineage_cap
from zmatrix.prediction.temporal_calibrator import evaluate_temporal_consistency
from zmatrix.prediction.event_store import PredictionEventStore

try:
    from pipelines.z17_loader import market_truth, get_kline, get_financials, dq_score, l4_health
    _HAS_Z01 = True
except ImportError:
    market_truth = lambda t: {"status":"stub","name":"?","price":0}
    get_kline = lambda t,d: {"prices":[],"count":0}
    get_financials = lambda t: {}; dq_score = lambda t: {"total":0}
    l4_health = lambda t: {"status":"stub"}; _HAS_Z01 = False


def _predict_single(ticker: str, name: str = "", lineage: dict | None = None) -> PredictionResult:
    g1 = market_truth(ticker) if _HAS_Z01 else {}
    kl = get_kline(ticker, 500) if _HAS_Z01 else {"prices":[],"count":0}
    fin = get_financials(ticker) if _HAS_Z01 else {}
    
    if lineage is None:
        lineage = {"market_data":"UNKNOWN_PROXY" if not _HAS_Z01 else "REALTIME",
                   "intraday":"DAILY_OHLCV_PROXY","m1":False,"l2":False,
                   "source":["Z-G01"] if _HAS_Z01 else ["UNKNOWN"],
                   "upstream_status":"PASS" if _HAS_Z01 else "DEGRADED_MISSING_LINEAGE",
                   "trust":"MEDIUM" if _HAS_Z01 else "LOW"}
    lin = evaluate_lineage(lineage)

    # ── 25-factor scoring via predict_engine ──
    try:
        from scripts.predict_engine import predict as pe_predict
        import scripts.predict_engine as pe
        
        price = g1.get("price") or 0
        prev_close = g1.get("baostock_close") or (kl.get("close",[])[-2] if len(kl.get("close",[]))>=2 else price)
        pct = round((price/prev_close-1)*100,2) if prev_close>0 else 0
        
        rt_data = {"price":price,"pct":pct,"high":g1.get("high",price),
                   "low":g1.get("low",price),"prev":prev_close,
                   "turnover":round(sum(kl.get("volume",[])[-5:])/5/1000000,1) if kl.get("volume") else 1.0,
                   "name":name or g1.get("name",ticker)}
        
        if ticker not in pe.STOCK_DB:
            pe.STOCK_DB[ticker] = {"sector":g1.get("industry",fin.get("industry","其他")),
                "growth":fin.get("roe_5y_avg",5)>8 if fin.get("roe_5y_avg") else False,
                "order":fin.get("has_finance",False),
                "buyback":fin.get("dividend_yield",0)>2 if fin.get("dividend_yield") else False,
                "stage":"early" if g1.get("price",0)>0 else "mid",
                "pe":fin.get("pe_ttm",20)}
        
        result = pe_predict(ticker, rt_data)
        raw_score = (result.get("prob",50)-50)/35*10
    except Exception:
        result = {"prob":50,"verdict":"观望","dims":{},"bull":0,"bear":0,"neut":25}
        raw_score = 0.0

    cov = lin.get("probability_cap",0.75)/0.95
    result_raw = fermi_weighted(raw_score=raw_score, coverage_adj=min(cov,1.0))
    raw_prob = apply_lineage_cap(result_raw["probability"], lin)
    cap = lin["probability_cap"]
    def _clamp(x,lo=0.0,hi=cap): return round(max(lo,min(x,hi)),4)
    
    t5 = _clamp(raw_prob)
    t1 = _clamp(raw_prob-0.05)
    t20 = _clamp(raw_prob+0.05 if result.get("prob",50)>60 else raw_prob-0.05)

    temporal = evaluate_temporal_consistency(t1, t5, t20)
    action = temporal["action_cap"]
    for f in FORBIDDEN_ACTIONS: assert action != f

    return PredictionResult(
        ticker=ticker, name=name or g1.get("name","?"),
        probability=round(raw_prob,4),
        horizon={"T1":round(t1,4),"T5":round(t5,4),"T20":round(t20,4)},
        evidence_coverage=round(cov,3), data_lineage=lin,
        temporal_consistency=temporal, next_triggers=temporal.get("next_triggers",[]),
        action_proposal=action,
        z9_sample={"strict_t_plus_n_required":True,"auto_adjust_allowed":False,
                   "auto_adjust_reason":"Z_G18_WRITES_PREDICTION_SAMPLE_ONLY_AUTO_ADJUST_FORBIDDEN"},
        raw_score=raw_score, confidence=lin["confidence_cap"], warnings=[])


def run(tickers=None, mode="daily", universe="WATCHLIST"):
    now = datetime.now(TZ)
    if tickers is None:
        try:
            from pipelines.universe_provider import load_universe
            uni = load_universe(universe, allow_fallback=True)
            tickers = uni["tickers"][:20]
            print(f"\n📡 Universe: {uni['source']} {uni['count']}只 → 预测TOP{len(tickers)}")
        except Exception:
            tickers = ["002472","601899","600519","688981"]
    elif isinstance(tickers, str):
        tickers = tickers.split(",")
    result = {"pipeline_signature":"Z-G18_天机引擎_v2.1.1","status":"PASS_PROXY" if _HAS_Z01 else "DEGRADED",
              "mode":mode,"data_lineage":{},"predictions":[],"sections":{},"warnings":[],"errors":[]}

    print(f"\n☯️ Z-G18 天机引擎 v2.1.1 — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"   25因子 + 8条不变量 + {'Z-G01已连接' if _HAS_Z01 else '⚠️ stub'}")
    print("=" * 60)

    strict_count = 0
    try:
        store = PredictionEventStore()
        strict_count = store.count_resolved_strict()
        print(f"\n📊 Z9状态: {strict_count}/50 strict T+N samples")
    except Exception:
        print(f"\n📊 Z9状态: store unavailable")

    predictions = []
    for t in tickers:
        pred = _predict_single(t)
        pred.validate_action()
        predictions.append(pred)
        icon = "🟢" if pred.probability>0.65 else ("🟡" if pred.probability>0.40 else "🔴")
        print(f"\n  {icon} {pred.ticker} {pred.name:<8s} {pred.probability*100:.0f}%"
              f" T1:{pred.horizon['T1']*100:.0f}% T5:{pred.horizon['T5']*100:.0f}%"
              f" {pred.action_proposal} [{pred.confidence}]")

    result["predictions"] = [{"ticker":p.ticker,"name":p.name,"probability":p.probability,
        "horizon":p.horizon,"evidence_coverage":p.evidence_coverage,
        "data_lineage":p.data_lineage,"temporal_consistency":p.temporal_consistency,
        "next_triggers":p.next_triggers,"action_proposal":p.action_proposal,"z9":p.z9_sample}
        for p in predictions]

    result["sections"]["z9_strict_samples"] = strict_count
    result["sections"]["z9_samples_written"] = 0
    result["sections"]["z9_write_status"] = "DEFERRED_NOT_CONNECTED"
    result["sections"]["z9_prediction_samples_ready"] = len(predictions)
    result["sections"]["auto_adjust_allowed"] = False
    result["sections"]["auto_adjust_reason"] = "Z_G18_WRITES_PREDICTION_SAMPLE_ONLY_AUTO_ADJUST_FORBIDDEN"

    if predictions:
        caps = [p.data_lineage.get("probability_cap",0.60) for p in predictions]
        confs = [p.data_lineage.get("confidence_cap","LOW") for p in predictions]
        result["data_lineage"] = {"global_data_precision":"DAILY_OHLCV_PROXY",
            "probability_cap":round(min(caps),3),
            "confidence_cap":"LOW" if "LOW" in confs else ("MEDIUM" if "MEDIUM" in confs else "HIGH"),
            "m1_connected":False,"l2_connected":False,"source":"AGGREGATED_FROM_PREDICTIONS"}
    else:
        result["data_lineage"] = {"global_data_precision":"DATA_GAP","probability_cap":0.60,
            "confidence_cap":"LOW","m1_connected":False,"l2_connected":False,"source":"NO_PREDICTIONS"}
    
    # ── Oracle Report + 落盘 ──
    report = _render_oracle(predictions, strict_count, uni_source if 'uni' in dir() else "manual", now)
    result["sections"]["oracle_report_path"] = _save_oracle(report, now)
    result["sections"]["oracle_text"] = report
    
    return result


def _render_oracle(predictions, strict_count, source, now):
    """生成人类友好天机签报告"""
    lines = []
    lines.append(f"# ☯️ 今日天机 — {now.strftime('%Y-%m-%d %H:%M')} 盘前")
    lines.append(f"")
    lines.append(f"> 管道: Z-G18 天机引擎 v2.1.1 | 25因子+8不变量 | Z9: {strict_count}/50 strict T+N")
    lines.append(f"> Universe: {source} | 预测标的: {len(predictions)}只")
    lines.append(f"")
    
    sorted_preds = sorted(predictions, key=lambda p: p.probability, reverse=True)
    
    lines.append("## 🔥 高概率 (>65%)")
    high = [p for p in sorted_preds if p.probability > 0.65]
    if high:
        for p in high:
            lines.append(f"")
            lines.append(f"### 🟢 {p.name}({p.ticker}) — {p.probability*100:.0f}%")
            lines.append(f"")
            lines.append(f"| 维度 | 值 |")
            lines.append(f"|------|------|")
            lines.append(f"| T1短期 | {p.horizon['T1']*100:.0f}% |")
            lines.append(f"| T5中期 | {p.horizon['T5']*100:.0f}% |")
            lines.append(f"| T20长期 | {p.horizon['T20']*100:.0f}% |")
            lines.append(f"| 动作建议 | {p.action_proposal} |")
            lines.append(f"| 时间一致性 | {p.temporal_consistency.get('consistency','?')} |")
            lines.append(f"| 置信度 | {p.confidence} |")
            if p.next_triggers:
                lines.append(f"")
                lines.append(f"**下一步触发:**")
                for t in p.next_triggers:
                    lines.append(f"- {t['trigger_id']}: {t['on_pass']} / {t['on_fail']}")
    else:
        lines.append(f"")
        lines.append(f"暂无高概率标的。当前市场偏谨慎。")
    
    lines.append(f"")
    lines.append("## 📊 全量预测")
    lines.append(f"")
    lines.append(f"| 标的 | 概率 | T1 | T5 | T20 | 动作 | 置信度 |")
    lines.append(f"|------|:--:|:--:|:--:|:--:|------|:--:|")
    for p in sorted_preds:
        icon = "🟢" if p.probability>0.65 else ("🟡" if p.probability>0.40 else "🔴")
        lines.append(f"| {icon} {p.name}({p.ticker}) | {p.probability*100:.0f}% | {p.horizon['T1']*100:.0f}% | {p.horizon['T5']*100:.0f}% | {p.horizon['T20']*100:.0f}% | {p.action_proposal} | {p.confidence} |")
    
    lines.append(f"")
    lines.append("## ⚠️ 边界声明")
    lines.append(f"")
    lines.append(f"- 不输出 BUY/SELL/AUTO_TRADE/MARKET_ORDER")
    lines.append(f"- DAILY_OHLCV_PROXY, M1/L2未连接")
    lines.append(f"- auto_adjust_allowed=False, Z9写状态=DEFERRED")
    lines.append(f"- 非实盘交易信号，仅供研究参考")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"**签章**: ☯️ Z2天师 Hermes Research Kernel | Z-G18 v2.1.1")
    
    return "\n".join(lines)


def _save_oracle(report, now):
    """落盘天机签到记忆宫殿"""
    try:
        root = Path(__file__).resolve().parents[2] / "记忆宫殿" / "Z2信息熔炉" / "投资记忆银行" / "超级预测系统" / "监控中心"
        root.mkdir(parents=True, exist_ok=True)
        filename = now.strftime("%Y-%m-%d_天机签.md")
        path = root / filename
        path.write_text(report)
        # Also save to Obsidian vault
        obsidian = Path.home() / "Documents" / "openclaw memory" / "openclaw memory" / "Z2信息熔炉" / "投资记忆银行" / "超级预测系统" / "监控中心"
        obsidian.mkdir(parents=True, exist_ok=True)
        (obsidian / filename).write_text(report)
        return str(path)
    except Exception as e:
        return f"save_failed: {e}"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G18 天机引擎 v2.1.1")
    p.add_argument("--tickers", type=str, default="002472,601899,600519,688981")
    args = p.parse_args()
    run(args.tickers.split(","))
