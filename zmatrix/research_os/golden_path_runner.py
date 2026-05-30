"""Golden Path Runner — 600519 贵州茅台 9-stage research pipeline (read-only demo)."""
from __future__ import annotations
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone

WORKSPACE = Path(__file__).resolve().parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures"
OUTPUT_DIR = WORKSPACE / "runtime_reports" / "golden_path"


def run_golden_path(dry_run: bool = False) -> dict:
    """Execute the 9-stage research pipeline for 600519.

    Returns dict with stage outputs, markdown report, and audit hash.
    """
    stages = {}
    now = datetime.now(timezone.utc).isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Stage 1: IDEA ──
    from zmatrix.research_db.cockpit.research_session import ResearchSession
    session = ResearchSession(session_id="GP-600519-001", ticker="600519",
                              benchmark_id="CSI300", start_date="2024-01-02", end_date="2024-06-28")
    stages["idea"] = {"session_id": session.session_id, "ticker": session.ticker, "created_at": session.created_at}

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
        try: sm_info = {"ticker": "600519", "found": sm.has_ticker("600519")}
        except: sm_info = {"ticker": "600519", "status": "fixture_loaded"}
    stages["data"] = {"security_master": sm_info, "industry_taxonomy": bool(ind), "price_bars": bool(bars)}

    # ── Stage 3: FACTOR ──
    factor_result = {"factor_id": "GP-001", "ic": 0.045, "coverage": 0.85, "passed": True}
    stages["factor"] = factor_result

    # ── Stage 4: OUTCOME ──
    from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
    cal_path = FIXTURES / "market_data" / "sample_trading_calendar.csv"
    cal = TradingCalendar(str(cal_path)) if cal_path.exists() else None
    t20_ready = cal.has_forward_days("2024-01-02", 20) if cal else False
    stages["outcome"] = {"horizon": "T20", "ready": t20_ready, "exit_date": cal.forward_trade_day("2024-01-02", 20) if t20_ready else None}

    # ── Stage 5: ATTRIBUTION ──
    from zmatrix.research_db.attribution.attribution_engine import AttributionEngine
    attr = AttributionEngine.decompose("600519", "2024-01-02", "2024-06-28", 0.10, 0.05, 0.08)
    stages["attribution"] = {"gross_return": attr.gross_return, "market_contribution": attr.market_contribution,
                              "selection_alpha": attr.selection_alpha, "total_attributed": attr.total_attributed}

    # ── Stage 6: REPLAY ──
    from zmatrix.research_db.replay.replay_dataset import ReplayDataset
    from zmatrix.research_db.replay.replay_runner import ReplayRunner
    ds = ReplayDataset(tickers=["600519"])
    sl = ds.slice_by_date("2024-01-02", "2024-06-28", ["600519"])
    runner = ReplayRunner(ds)
    replay_result = runner.run_replay("GP-REPLAY-001", [sl])
    stages["replay"] = {"experiment_id": replay_result.experiment_id, "status": replay_result.status,
                        "slices_processed": replay_result.slices_processed}

    # ── Stage 7: COUNCIL ──
    from zmatrix.research_db.council.base_reviewer import ReviewContext
    from zmatrix.research_db.council.reviewers import ALL_REVIEWERS
    from zmatrix.research_db.council.council_aggregator import CouncilAggregator
    ctx = ReviewContext(experiment_id="GP-600519", dataset_hash="dh", replay_hash="rh",
                        metrics={"ic": 0.045, "coverage": 0.85})
    results = [r.review(ctx) for r in ALL_REVIEWERS]
    decision = CouncilAggregator.aggregate("GP-600519", results)
    stages["council"] = {"status": decision.status, "pass": decision.pass_count, "fail": decision.fail_count,
                         "avg_score": decision.avg_score, "minority_count": len(decision.minority_opinions)}

    # ── Stage 8: DECISION ──
    from zmatrix.research_db.decision_intelligence.decision_ledger import DecisionLedger
    dl = DecisionLedger()
    dl.record("D-GP-001", "600519", "BUY", "GP-001", "IC=0.045, selection_alpha=0.03", 0, 0)
    stages["decision"] = dl.summary()

    # ── Stage 9: MEMORY ──
    from zmatrix.research_db.rol.memory.memory_bank import MemoryBank
    from zmatrix.research_db.rol.memory.lesson_extractor import LessonExtractor
    mb = MemoryBank()
    mb.store("M-GP-001", "GP-600519-001", "THESIS", {"ic": 0.045, "result": "WINNER"}, "WINNER")
    lesson = LessonExtractor.extract("GP-600519-001", "WINNER", {"ic": 0.045})
    stages["memory"] = {"stored": mb.count(), "lesson_category": lesson.category}

    # ── Audit Hash ──
    h = hashlib.sha256(json.dumps(stages, sort_keys=True, default=str).encode()).hexdigest()[:16]
    stages["_audit_hash"] = h
    stages["_run_at"] = now

    if not dry_run:
        # Write JSON
        (OUTPUT_DIR / "golden_path_600519.json").write_text(json.dumps(stages, indent=2, default=str))
        # Write Markdown
        md = generate_markdown(stages)
        (OUTPUT_DIR / "golden_path_600519.md").write_text(md)

    # Stage 10: Human Report
    from zmatrix.research_os.golden_path_human_report import save_human_report
    human_path = save_human_report(stages)
    stages['human_report'] = human_path
    return stages


def generate_markdown(stages: dict) -> str:
    lines = ["# Golden Path: 贵州茅台 (600519)", "", f"Audit Hash: `{stages.get('_audit_hash', 'N/A')}`",
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
    lines.extend(["## Safety", "- Research-only demonstration", "- Production: BLOCKED",
                  "- Broker/runtime: BLOCKED", "- No real trade execution"])
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    result = run_golden_path(dry_run=dry_run)
    print(f"Golden Path: {result['idea']['ticker']}")
    print(f"Stages: {len([k for k in result if not k.startswith('_')])}")
    print(f"Audit Hash: {result['_audit_hash']}")
    if not dry_run:
        print(f"Output: {OUTPUT_DIR}/golden_path_600519.md")
