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

    # ── Load G09 cycle signals via targeted adapter (not full G09 run) ──
    from zmatrix.prediction.g09_signal_adapter import load_g09_signals_for_tickers
    g09_signals = load_g09_signals_for_tickers(tickers)
    g09_signal_map = g09_signals.get("signals", {})
    if g09_signals.get("available"):
        print(f"\n📡 G09周期信号: {len(g09_signal_map)}只已加载 → 约束G18预测")
    else:
        print(f"\n⚠️ G09周期信号: 未加载 ({g09_signals.get('reason','unknown')})")

    from zmatrix.prediction.g09_signal_adapter import apply_g09_constraints

    predictions = []
    for t in tickers:
        pred = _predict_single(t)
        
        # Apply G09 cycle constraints
        if g09_signal_map:
            g09_sig = g09_signal_map.get(t, {"available": False, "reason": "no_signal_for_ticker"})
            constraint = apply_g09_constraints(
                g09_sig, pred.action_proposal, pred.probability,
                pred.data_lineage.get("probability_cap", 0.75))
            
            if constraint["action_override"] != pred.action_proposal:
                pred.action_proposal = constraint["action_override"]
                pred.warnings.extend(constraint["warnings"])
            
            prob_before = pred.probability
            cap = constraint["probability_override"]
            pred.probability = cap
            # Sync horizon when probability is constrained
            pred.horizon["T1"] = round(min(pred.horizon.get("T1", 0.5), cap), 4)
            pred.horizon["T5"] = round(min(pred.horizon.get("T5", 0.5), cap), 4)
            pred.horizon["T20"] = round(min(pred.horizon.get("T20", 0.5), cap), 4)
            pred.temporal_consistency = evaluate_temporal_consistency(
                pred.horizon["T1"], pred.horizon["T5"], pred.horizon["T20"])
            pred.next_triggers = pred.temporal_consistency.get("next_triggers", [])
            # Add G09 evidence to the prediction output
            pred.temporal_consistency["g09_cycle"] = {
                "resonance": g09_sig.get("resonance_status"),
                "exit_alert": g09_sig.get("exit_alert"),
                "position_action": g09_sig.get("position_action"),
                "constraints_applied": constraint["reason_codes"],
            }
        
        pred.validate_action()
        predictions.append(pred)
        icon = "🟢" if pred.probability>0.65 else ("🟡" if pred.probability>0.40 else "🔴")
        print(f"\n  {icon} {pred.ticker} {pred.name:<8s} {pred.probability*100:.0f}%"
              f" T1:{pred.horizon['T1']*100:.0f}% T5:{pred.horizon['T5']*100:.0f}%"
              f" {pred.action_proposal} [{pred.confidence}]")

    # ── Final decision envelope ──
    from zmatrix.prediction.upstream_evidence_aggregator import build_upstream_evidence
    from zmatrix.prediction.adapters.g08_narrative_adapter import load_g08_signal
    from zmatrix.prediction.adapters.g11_risk_adapter import load_g11_signal
    from zmatrix.prediction.adapters.g14_global_baseline_adapter import load_g14_signal
    from zmatrix.prediction.adapters.z16_price_gate_adapter import load_z16_signal
    from zmatrix.prediction.adapters.g17_account_confirm_adapter import load_g17_signal
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.paper_execution_record import build_paper_execution_record
    from zmatrix.calibration.z9_calibration_sample import build_z9_calibration_sample
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    run_id = now.strftime("%Y%m%d_%H%M%S")
    for p in predictions:
        upstream = build_upstream_evidence(
            p.ticker,
            g09_signal=g09_signal_map.get(p.ticker, {}),
            g08_signal=load_g08_signal(p.ticker),
            g11_signal=load_g11_signal(p.ticker),
            g14_signal=load_g14_signal(p.ticker),
            z16_signal=load_z16_signal(p.ticker),
            g17_signal=load_g17_signal(p.ticker),
        )
        p.upstream_evidence = upstream
        p.final_decision = build_final_decision(p, upstream)
        p.paper_execution_record = build_paper_execution_record(p, run_id=run_id)
        p.z9_calibration_sample_preview = build_z9_calibration_sample(p.paper_execution_record, run_id=run_id)
        p.z9_ingestion_queue_preview = build_z9_ingestion_queue_item(p.z9_calibration_sample_preview, enqueue_run_id=run_id)
    result["sections"]["final_decision_envelope_version"] = "v1.1"
    result["sections"]["paper_execution_record_version"] = "v1.0"
    result["sections"]["paper_execution_records_ready"] = len(predictions)
    result["sections"]["z9_calibration_sample_version"] = "v1.0"
    result["sections"]["z9_calibration_samples_ready"] = len(predictions)
    result["sections"]["z9_ingestion_queue_version"] = "v1.0"
    result["sections"]["z9_ingestion_queue_items_ready"] = len(predictions)
    result["sections"]["z9_real_write_allowed"] = False
    result["sections"]["z9_write_status"] = "DEFERRED_NOT_CONNECTED"
    result["sections"]["z9_queue_write_allowed"] = False
    result["sections"]["z9_queue_write_status"] = "DEFERRED_NOT_CONNECTED"
    result["sections"]["z9_calibration_hooks_ready"] = True

    result["predictions"] = [{"ticker":p.ticker,"name":p.name,"probability":p.probability,
        "final_decision": getattr(p, "final_decision", None),
        "upstream_evidence": getattr(p, "upstream_evidence", None),
        "upstream_evidence_available": getattr(p, "upstream_evidence", {}).get("evidence_available", {}),
        "missing_sources": getattr(p, "upstream_evidence", {}).get("missing_sources", []),
        "paper_execution_record": getattr(p, "paper_execution_record", None),
        "z9_calibration_sample_preview": getattr(p, "z9_calibration_sample_preview", None),
        "z9_ingestion_queue_preview": getattr(p, "z9_ingestion_queue_preview", None),
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
    report = _render_oracle(predictions, strict_count, universe, now)
    result["sections"]["oracle_report_path"] = _save_oracle(report, now)
    
    # ── Auto-create decision cards for high-probability stocks ──
    try:
        from hermes.memory_bank import create_card, load_bank
        high_probs = [p for p in predictions if p.probability >= 0.65]
        cards_created = 0
        for p in high_probs:
            macro_summary = "MACRO:3逆风1顺风"  # simplified
            card = create_card(
                stock=p.ticker,
                situation=f"{now.strftime('%Y-%m-%d')} | {macro_summary} | Universe:{universe}",
                your_view="用户尚未操作(等待确认)",
                my_advice=f"Z-G18: {p.probability*100:.0f}% {p.action_proposal} T1:{p.horizon['T1']*100:.0f}% T5:{p.horizon['T5']*100:.0f}% T20:{p.horizon['T20']*100:.0f}%",
                actual_action="PENDING",
                outcome=None,
                cost=None,
                lesson=None,
                tags=["天机引擎","auto",p.action_proposal],
                emotion="中性",
                priority_scene="A" if p.probability>0.70 else "C"
            )
            if card: cards_created += 1
        bank = load_bank()
        result["sections"]["decision_cards_created"] = cards_created
        result["sections"]["decision_cards_total"] = len(bank.get("cards",[]))
        print("\n📇 决策卡: +{}张 → 累计{}张".format(cards_created, len(bank.get("cards",[]))))
    except Exception as e:
        result["sections"]["decision_cards_created"] = 0
        result["sections"]["decision_cards_note"] = f"auto-create failed: {e}"
    result["sections"]["oracle_text"] = report
    
    return result


def _render_oracle(predictions, strict_count, source, now):
    """人类友好天机签 — 多维度分析 + 信号明细 + 情景推演"""
    lines = []
    sorted_preds = sorted(predictions, key=lambda p: p.probability, reverse=True)
    high = [p for p in sorted_preds if p.probability > 0.65]
    mid = [p for p in sorted_preds if 0.40 < p.probability <= 0.65]
    low = [p for p in sorted_preds if p.probability <= 0.40]
    
    # ── Header ──
    lines.append(f"# ☯️ 今日天机 — {now.strftime('%Y-%m-%d %H:%M')} CST")
    lines.append(f"")
    lines.append(f"> **管道**: Z-G18 天机引擎 v2.1.1 | **因子**: 25因子(M/I/F/T/R) + 8不变量 | **Z9**: {strict_count}/50 strict T+N")
    lines.append(f"> **Universe**: {source} | **预测标的**: {len(predictions)}只 | **高概率**: {len(high)}只 | **中概率**: {len(mid)}只 | **低概率**: {len(low)}只")
    lines.append(f"")
    
    # ── 宏观体温 ──
    lines.append("## 🌡️ 市场体温")
    lines.append(f"")
    try:
        from scripts.predict_engine import MACRO
        m_labels = {'M1':'美元指数','M2':'美联储','M3':'市场情绪','M4':'流动性','M5':'风险偏好'}
        m_icons = {-1:'🔴逆风',0:'⚪中性',1:'🟢顺风'}
        macro_str = ' | '.join(f"{m_labels.get(k,k)}: {m_icons.get(v,'?')}" for k,v in MACRO.items())
        lines.append(f"**宏观信号**: {macro_str}")
        headwinds = sum(1 for v in MACRO.values() if v < 0)
        tailwinds = sum(1 for v in MACRO.values() if v > 0)
        verdict = "偏谨慎" if headwinds > tailwinds else ("偏乐观" if tailwinds > headwinds else "中性")
        lines.append(f"")
        lines.append(f"**综合**: {headwinds}逆风 {tailwinds}顺风 → **{verdict}**。")
        lines.append(f"")
        if headwinds >= 3:
            lines.append(f"⚠️ 宏观逆风偏多({headwinds}/5)，高概率标的需额外确认。不急于开新仓。")
        elif tailwinds >= 3:
            lines.append(f"✅ 宏观顺风为主({tailwinds}/5)，可适度积极。")
        else:
            lines.append(f"↔️ 宏观信号混合，精选个股优于仓位择时。")
    except Exception:
        lines.append(f"*宏观信号数据暂不可用*")
    lines.append(f"")
    
    # ── 高概率详解 ──
    lines.append("## 🔥 高概率标的 ({n}只)".format(n=len(high)))
    if high:
        for p in high:
            lines.append(f"")
            lines.append(f"### 🟢 {p.name}({p.ticker}) — {p.probability*100:.0f}%")
            lines.append(f"")
            lines.append(f"| 维度 | T1短期 | T5中期 | T20长期 | 动作 | 置信度 |")
            lines.append(f"|------|:--:|:--:|:--:|------|:--:|")
            lines.append(f"| 概率 | {p.horizon['T1']*100:.0f}% | {p.horizon['T5']*100:.0f}% | {p.horizon['T20']*100:.0f}% | {p.action_proposal} | {p.confidence} |")
            lines.append(f"")
            # Signal analysis
            lines.append(f"**时间一致性**: {p.temporal_consistency.get('consistency','?')}")
            if p.temporal_consistency.get('consistency') == 'ALL_HORIZON_STRONG':
                lines.append(f"  → 短中长三期共振，信号可靠性较高。")
            elif p.temporal_consistency.get('consistency') == 'LONG_STRONG_SHORT_WEAK':
                lines.append(f"  → 中长期看好但短期偏弱，建议等待短期确认后再行动。典型的'好事但需要等一等'。")
            elif p.temporal_consistency.get('consistency') == 'MIXED':
                lines.append(f"  → 各周期信号不一致，需结合基本面独立判断。")
            lines.append(f"")
            # Triggers
            if p.next_triggers:
                lines.append(f"**下一步触发条件**:")
                for t in p.next_triggers:
                    lines.append(f"- 📋 **{t['trigger_id']}**: 满足 → {t['on_pass']} | 不满足 → {t['on_fail']}")
                    lines.append(f"  截止: {t.get('deadline','?')} | 来源: {t.get('source_pipeline','?')}")
                lines.append(f"")
            # Interpretation
            lines.append(f"**天师解读**:")
            try:
                from scripts.predict_engine import STOCK_DB
                pe = STOCK_DB.get(p.ticker,{}).get('pe')
            except: pe = None
            if p.probability >= 0.70:
                lines.append(f"  {p.probability*100:.0f}%概率由25因子多维共振驱动。" + (f"PE{pe:.0f}x估值合理" if pe and pe<30 else (f"PE{pe:.0f}x需关注估值" if pe else "")) + "。")
                if p.action_proposal == "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17":
                    lines.append(f"  纸面验证级别——需Z-G16确认执行计划后才能升级。")
                elif p.action_proposal == "PAPER_TRACK":
                    lines.append(f"  PAPER_TRACK级别——可纳入观察增强列表，但受MACRO逆风(3/5)限制，建议轻仓试探。")
                else:
                    lines.append(f"  当前{p.action_proposal}级别。MACRO逆风偏多，等待确认信号。")
            elif p.probability >= 0.65:
                lines.append(f"  {p.probability*100:.0f}%处于边界区间。" + (f"PE{pe:.0f}x有安全边际" if pe and pe<15 else "") + "。建议确认开盘信号后再行动。")
            else:
                lines.append(f"  当前概率偏低，不纳入主动候选池。")
    else:
        lines.append(f"")
        lines.append(f"今日无高概率(>65%)标的。市场整体偏谨慎，等待催化。")
    lines.append(f"")
    
    # ── 全量排名 ──
    lines.append("## 📊 全量预测排名")
    lines.append(f"")
    lines.append(f"| # | 标的 | 概率 | T1 | T5 | T20 | 动作 | 置信度 |")
    lines.append(f"|:--:|------|:--:|:--:|:--:|:--:|------|:--:|")
    for i, p in enumerate(sorted_preds):
        icon = "🟢" if p.probability>0.65 else ("🟡" if p.probability>0.40 else "🔴")
        lines.append(f"| {i+1} | {icon} {p.name}({p.ticker}) | {p.probability*100:.0f}% | {p.horizon['T1']*100:.0f}% | {p.horizon['T5']*100:.0f}% | {p.horizon['T20']*100:.0f}% | {p.action_proposal} | {p.confidence} |")
    lines.append(f"")
    
    # ── 情景推演 ──
    lines.append("## 🎯 情景推演")
    lines.append(f"")
    if high:
        top3 = sorted_preds[:3]
        lines.append(f"**乐观情景**: " + "、".join(f"{p.name}+{p.horizon['T5']*100:.0f}%" for p in top3) + "同时兑现 → 组合有较好表现。催化剂需持续跟踪。")
        lines.append(f"")
        lines.append(f"**基准情景**: 高概率标的震荡上行，中低概率标的维持观望。正常节奏执行持仓管理。")
        lines.append(f"")
        lines.append(f"**悲观情景**: 宏观逆风加剧(美元破99或FOMC鹰派升级) → 高概率标的也可能被拖累。做好止损准备。")
    else:
        lines.append(f"当前无高概率标的。三种情景均建议保持现金或轻仓。等待下一轮催化确认。")
    lines.append(f"")
    
    # ── 校准参考 ──
    lines.append("## 📐 校准参考")
    lines.append(f"")
    z9_status = "已可触发自动调权" if strict_count >= 50 else "不足,自动调权已冻结"
    lines.append(f"- **Z9 严格样本**: {strict_count}/50 ({z9_status})")
    lines.append(f"- **数据精度**: DAILY_OHLCV_PROXY (日线OHLCV代理，非M1/Tick)")
    lines.append(f"- **Lineage Cap**: 概率上限0.75 (因proxy数据源)")
    lines.append(f"- **下次校准**: 仅允许严格T+N历史收盘样本；当前不进行自动调权。")
    lines.append(f"")
    
    # ── 边界声明 ──
    lines.append("## ⚠️ 边界声明")
    lines.append(f"")
    lines.append(f"- 本报告为**概率预测**，非买卖建议。不输出 BUY/SELL/AUTO_TRADE/MARKET_ORDER")
    lines.append(f"- **数据精度**: DAILY_OHLCV_PROXY, M1/L2未连接。盘口级预测能力受限")
    lines.append(f"- **权重冻结**: auto_adjust_allowed=False，Z9严格样本不足50时自动调权已锁定")
    lines.append(f"- **适用场景**: 投研分析 + 候选池排序 + 纸面执行验证")
    lines.append(f"- **不适用**: 自动实盘交易、M1盘口决策、无人工确认的买卖执行")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*签章: ☯️ Z2天师 Hermes Research Kernel | Z-G18 v2.1.1*")
    
    return "\n".join(lines)


def _save_oracle(report, now):
    """落盘天机签到专属目录"""
    paths = []
    for base in [
        Path.home() / "Documents" / "openclaw memory" / "openclaw memory" / "Z2信息熔炉" / "投资记忆银行" / "超级预测系统" / "天机引擎",
        Path.home() / "Documents" / "openclaw memory" / "openclaw memory" / "Z2信息熔炉" / "投资记忆银行" / "超级预测系统" / "天机引擎",
    ]:
        try:
            base.mkdir(parents=True, exist_ok=True)
            filename = now.strftime("%Y-%m-%d_天机签.md")
            path = base / filename
            path.write_text(report)
            paths.append(str(path))
        except Exception:
            pass
    return paths[0] if paths else "save_failed"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G18 天机引擎 v2.1.1")
    p.add_argument("--tickers", type=str, default=None, help="逗号分隔代码(留空则用UniverseProvider)")
    p.add_argument("--universe", default="PRESET_DEV", help="Universe source")
    args = p.parse_args()
    tickers = args.tickers.split(",") if args.tickers else None
    run(tickers=tickers, universe=args.universe)
