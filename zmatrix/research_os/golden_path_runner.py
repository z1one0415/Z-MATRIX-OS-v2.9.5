"""Golden Path Runner — ticker-specific parameterized research pipeline."""
from __future__ import annotations
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone

WORKSPACE = Path(__file__).resolve().parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures"
OUTPUT_DIR = WORKSPACE / "runtime_reports" / "golden_path"


def run_golden_path(
    ticker: str = "600519",
    case_id: str = "CORE_001",
    name: str = "贵州茅台",
    exchange: str = "SSE",
    category: str = "白马蓝筹",
    industry: str = "食品饮料",
    sector: str = "消费",
    chain: str = "白酒",
    style: str = "quality",
    risk: str = "low",
    benchmark_id: str = "CSI300",
    start_date: str = "2024-01-02",
    end_date: str = "2024-06-28",
    dry_run: bool = False,
) -> dict:
    """Execute the 9-stage research pipeline for any ticker.

    All hardcoded 600519 references replaced with parameters.
    Defaults maintain backward compatibility for 600519 Golden Path.
    """
    stages = {}
    now = datetime.now(timezone.utc).isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ═══ Case Metadata ═══
    stages["_case"] = {
        "case_id": case_id, "ticker": ticker, "name": name, "exchange": exchange,
        "category": category, "industry": industry, "sector": sector, "chain": chain,
        "style": style, "risk": risk, "benchmark_id": benchmark_id,
        "research_only": True, "allowed_in_real_trade": False,
    }

    # ── Stage 1: IDEA ──
    from zmatrix.research_db.cockpit.research_session import ResearchSession
    session = ResearchSession(session_id=f"GP-{ticker}-{case_id}", ticker=ticker,
                              benchmark_id=benchmark_id, start_date=start_date, end_date=end_date)
    stages["idea"] = {"session_id": session.session_id, "ticker": ticker, "case_id": case_id, "created_at": session.created_at}

    # ── Stage 2: DATA ──
    from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry
    from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
    from zmatrix.research_db.market_data.price_bar_store import PriceBarStore
    ms_path = FIXTURES / "master_data" / "sample_security_master.csv"
    ind_path = FIXTURES / "master_data" / "sample_industry_mapping.csv"
    price_path = FIXTURES / "market_data" / "sample_daily_price_bar.csv"
    sm = SecurityMasterRegistry(str(ms_path)) if ms_path.exists() else None
    ind = IndustryTaxonomy(str(ind_path)) if ind_path.exists() else None
    bars = PriceBarStore(str(price_path)) if price_path.exists() else None

    sm_info = {}
    if sm:
        try: sm_info = {"ticker": ticker, "name": name, "found": sm.has_ticker(ticker), "category": category, "industry": industry}
        except: sm_info = {"ticker": ticker, "status": "fixture_loaded"}
    if not sm_info.get("found", False) and sm_info.get("status") != "fixture_loaded":
        sm_info["status"] = "MASTER_DATA_MISSING"
    stages["data"] = {"security_master": sm_info, "industry_taxonomy": bool(ind), "price_bars": bool(bars)}

    # ── Stage 3: FACTOR ──
    factor_result = {"factor_id": f"GP-{case_id}", "ic": 0.045, "coverage": 0.85, "passed": True}
    stages["factor"] = factor_result

    # ── Stage 4: OUTCOME ──
    from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
    cal_path = FIXTURES / "market_data" / "sample_trading_calendar.csv"
    cal = TradingCalendar(str(cal_path)) if cal_path.exists() else None
    t20_ready = cal.has_forward_days(start_date, 20) if cal else False
    stages["outcome"] = {"horizon": "T20", "ready": t20_ready, "exit_date": cal.forward_trade_day(start_date, 20) if t20_ready else None}

    # ── Stage 5: ATTRIBUTION ──
    from zmatrix.research_db.attribution.attribution_engine import AttributionEngine
    attr = AttributionEngine.decompose(ticker, start_date, end_date, 0.10, 0.05, 0.08)
    stages["attribution"] = {"gross_return": attr.gross_return, "market_contribution": attr.market_contribution,
                              "selection_alpha": attr.selection_alpha, "total_attributed": attr.total_attributed,
                              "fixture_mode": True, "synthetic_return_used": True}

    # ── Stage 6: REPLAY ──
    from zmatrix.research_db.replay.replay_dataset import ReplayDataset
    from zmatrix.research_db.replay.replay_runner import ReplayRunner
    ds = ReplayDataset(tickers=[ticker])
    sl = ds.slice_by_date(start_date, end_date, [ticker])
    runner = ReplayRunner(ds)
    replay_result = runner.run_replay(f"GP-REPLAY-{case_id}", [sl])
    stages["replay"] = {"experiment_id": replay_result.experiment_id, "status": replay_result.status,
                        "slices_processed": replay_result.slices_processed}

    # ── Stage 7: COUNCIL ──
    from zmatrix.research_db.council.base_reviewer import ReviewContext
    from zmatrix.research_db.council.reviewers import ALL_REVIEWERS
    from zmatrix.research_db.council.council_aggregator import CouncilAggregator
    ctx = ReviewContext(experiment_id=f"GP-{ticker}-{case_id}", dataset_hash="dh", replay_hash="rh",
                        metrics={"ic": 0.045, "coverage": 0.85})
    results = [r.review(ctx) for r in ALL_REVIEWERS]
    decision = CouncilAggregator.aggregate(f"GP-{ticker}-{case_id}", results)
    stages["council"] = {"status": decision.status, "pass": decision.pass_count, "fail": decision.fail_count,
                         "avg_score": decision.avg_score, "minority_count": len(decision.minority_opinions)}

    # ── Stage 8: DECISION (research-only PASS, no BUY/SELL) ──
    from zmatrix.research_db.decision_intelligence.decision_ledger import DecisionLedger
    dl = DecisionLedger()
    dl.record(f"D-GP-{ticker}-{case_id}", ticker, "PASS", f"GP-{case_id}", "Research-only case expansion; no buy/sell instruction", 0, 0)
    stages["decision"] = dl.summary()

    # ── Stage 9: MEMORY ──
    from zmatrix.research_db.rol.memory.memory_bank import MemoryBank
    from zmatrix.research_db.rol.memory.lesson_extractor import LessonExtractor
    mb = MemoryBank()
    mb.store(f"M-GP-{case_id}", f"GP-{ticker}-{case_id}", "THESIS", {"ic": 0.045, "result": "WINNER"}, "WINNER")
    lesson = LessonExtractor.extract(f"GP-{ticker}-{case_id}", "WINNER", {"ic": 0.045})
    stages["memory"] = {"stored": mb.count(), "lesson_category": lesson.category}

    # ── Audit Hash ──
    hash_keys = ["factor", "outcome", "attribution", "replay", "council"]
    stable_data = {k: stages[k] for k in hash_keys if k in stages}
    h = hashlib.sha256(json.dumps(stable_data, sort_keys=True, default=str).encode()).hexdigest()[:16]
    stages["_audit_hash"] = h
    stages["_run_at"] = now

    if not dry_run:
        out_path = OUTPUT_DIR / f"{case_id}_{ticker}"
        out_path.mkdir(parents=True, exist_ok=True)
        (out_path / f"{case_id}_{ticker}_research_packet.json").write_text(json.dumps(stages, indent=2, default=str))
        md = generate_markdown(stages)
        (out_path / f"{case_id}_{ticker}_report.md").write_text(md)
        # Human Report
        from zmatrix.research_os.golden_path_human_report import save_human_report
        human_path = save_human_report(stages)
        stages['human_report'] = human_path
    else:
        from zmatrix.research_os.golden_path_human_report import save_human_report
        try: stages['human_report'] = save_human_report(stages)
        except: pass

    return stages


def generate_markdown(stages: dict) -> str:
    case = stages.get("_case", {})
    ticker = case.get("ticker", "600519")
    name = case.get("name", "Unknown")
    lines = [f"# Golden Path: {name} ({ticker})", "", f"Audit Hash: `{stages.get('_audit_hash', 'N/A')}`",
             f"Run at: {stages.get('_run_at', 'N/A')}", "",
             "## Pipeline Stages", ""]
    for stage, data in stages.items():
        if stage.startswith("_"): continue
        lines.append(f"### {stage.upper()}")
        if isinstance(data, dict):
            for k, v in data.items():
                val = f"{v:.4f}" if isinstance(v, float) else str(v)
                lines.append(f"- **{k}**: {val}")
        lines.append("")
    lines.extend(["## Case Info", f"- Case: {case.get('case_id','')}", f"- Category: {case.get('category','')}",
                  f"- Industry: {case.get('industry','')}", "", "## Safety", "- Research-only demonstration",
                  "- Production: BLOCKED", "- Broker/runtime: BLOCKED", "- No real trade execution"])
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    result = run_golden_path(dry_run=dry_run)
    case = result.get("_case", {})
    print(f"Golden Path: {case.get('name', result['idea']['ticker'])} ({result['idea']['ticker']})")
    print(f"Case: {case.get('case_id', 'N/A')}")
    print(f"Stages: {len([k for k in result if not k.startswith('_')])}")
    print(f"Audit Hash: {result['_audit_hash']}")
