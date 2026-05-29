"""V4.0-C2-5 IRF True Chain Integration"""
from zmatrix.dataforge.forge_depth import EvidenceCard, FactExtractionStore
from zmatrix.research_council.reviewers import REVIEWERS, ReviewerOutput
from zmatrix.reports.renderer import ReportRenderer
from zmatrix.audit.cockpit_audit import OutputEnvelope, AuditEvent, AuditExportPack


def irf01_full_chain(ticker="000001"):
    card = EvidenceCard("ev1", ticker, "", "roe", 15.2, "2026-05-29")
    store = FactExtractionStore(); store.append(card)
    reviewer = REVIEWERS.get("R01_MACRO_STRATEGIST")
    output = reviewer.review({"source": "tushare", "roe": 15.2})
    renderer = ReportRenderer()
    report = renderer.render("single_stock_research", {"ticker": ticker, "roe": 15.2, "review_score": output.deterministic_score})
    envelope = OutputEnvelope(pipeline_id="IRF-01", run_id="IRF-01-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-01-evt-001", "PIPELINE_RUN", pipeline_id="IRF-01")
    export = AuditExportPack.generate(envelope, [audit])
    return {"card": card, "review": output, "report_len": len(report), "envelope": envelope.to_dict(), "audit": audit.to_dict(), "export_manifest": export["manifest"]["real_trade_allowed"]}


def irf02_monthly_selection_chain():
    """IRF-02: Monthly Full Market Selection — 月度全市场选股"""
    card = EvidenceCard("ev2", "ALL_MARKET", "2026-05-29", "market_scan", "universe_size", 3676, "2026-05-29")
    store = FactExtractionStore(); store.append(card)

    reviewer_r01 = REVIEWERS.get("R01_MACRO_STRATEGIST")
    reviewer_r07 = REVIEWERS.get("R07_CHAIN_VALUE_CAPTURE")
    r01_output = reviewer_r01.review({"source": "market_scan", "universe": 3676})
    r07_output = reviewer_r07.review({"source": "market_scan", "chain_coverage": 10})

    renderer = ReportRenderer()
    report = renderer.render("monthly_selection", {
        "ticker": "ALL_MARKET",
        "universe_size": 3676,
        "r01_score": r01_output.deterministic_score,
        "r07_score": r07_output.deterministic_score,
        "timestamp": "2026-05-29"
    })

    envelope = OutputEnvelope(pipeline_id="IRF-02", run_id="IRF-02-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-02-evt-001", "PIPELINE_RUN", pipeline_id="IRF-02")
    export = AuditExportPack.generate(envelope, [audit])

    return {
        "card": card,
        "store_size": len(store._facts),
        "r01_review": r01_output,
        "r07_review": r07_output,
        "report_len": len(report),
        "envelope": envelope.to_dict(),
        "audit": audit.to_dict(),
        "export_manifest": export,
    }


def irf03_factor_chain():
    from zmatrix.factor_factory.factory_depth import OutcomeHorizonDepth; from zmatrix.factor_factory.factory import FactorPromotionGate
    dates = [f"2026-06-{i:02d}" for i in range(1,30)]
    horizon = OutcomeHorizonDepth.check(dates, "2026-06-01", "t20")
    gate = FactorPromotionGate.check(horizon['horizon_ready'], True, True, True, 500)
    envelope = OutputEnvelope(pipeline_id="IRF-03", run_id="IRF-03-001", status="SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-03-evt-001", "FACTOR_VALIDATION", pipeline_id="IRF-03")
    return {"horizon_ready": horizon['horizon_ready'], "gate": gate, "envelope": envelope.to_dict(), "audit": audit.to_dict()}


def irf04_execution_chain():
    from zmatrix.execution_quality.execution import TransactionCostModel, LimitBoardGate, PaperOrderPreview
    cost = TransactionCostModel.compute(10, 11, 1000)
    gate = LimitBoardGate.check({'open':10,'high':10,'low':10,'close':10}, 9.09)
    preview = PaperOrderPreview.generate("000001", gate['action'], 100, cost.get('total_cost_pct', 0.15))
    envelope = OutputEnvelope(pipeline_id="IRF-04", run_id="IRF-04-001", status="SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-04-evt-001", "EXECUTION_CHECK", pipeline_id="IRF-04")
    return {"gate_action": gate['action'], "preview": preview, "envelope": envelope.to_dict(), "audit": audit.to_dict()}


def irf05_account_review_chain():
    """IRF-05: Account Review — 账户审查"""
    from zmatrix.account_governance.governance import CapitalCurve, ActionPermissionGate

    # Step 1: CapitalCurve with multiple timepoints
    curve = CapitalCurve()
    curve.add("2026-05-01", 5000, 100000)
    curve.add("2026-05-08", -2000, 98000)
    curve.add("2026-05-15", 8000, 106000)
    curve.add("2026-05-22", -1000, 105000)
    curve.add("2026-05-29", 3000, 108000)

    # Step 2: compute() and verify parameters
    curve_result = curve.compute()

    # Step 3: ActionPermissionGate.check()
    gate_result = ActionPermissionGate.check({"curve_result": curve_result})

    # Step 4: Envelope + Audit + Export
    envelope = OutputEnvelope(pipeline_id="IRF-05", run_id="IRF-05-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-05-evt-001", "ACCOUNT_REVIEW", pipeline_id="IRF-05")
    export = AuditExportPack.generate(envelope, [audit])

    return {
        "curve_result": curve_result,
        "gate_result": gate_result,
        "envelope": envelope.to_dict(),
        "audit": audit.to_dict(),
        "export_manifest": export,
    }


def irf06_portfolio_alpha_chain():
    """IRF-06: Portfolio Alpha Review — 组合Alpha审查"""
    from zmatrix.factor_factory.factory_depth import OutcomeHorizonIntegrity, NetReturnCalculator

    # Step 1: OutcomeHorizonIntegrity.check()
    forward_bars = [f"2026-06-{i:02d}" for i in range(1, 22)]
    horizon_result = OutcomeHorizonIntegrity.check(forward_bars, "t20")

    # Step 2: NetReturnCalculator.compute()
    net_return_result = NetReturnCalculator.compute(5.2, 10, 10.5, 1000)

    # Step 3: ReportRenderer.render("portfolio_alpha_daily")
    renderer = ReportRenderer()
    report = renderer.render("portfolio_alpha_daily", {
        "ticker": "PORTFOLIO_ALPHA",
        "horizon_ready": horizon_result["horizon_ready"],
        "net_return_pct": net_return_result["net_return_pct"],
        "gross_return_pct": net_return_result["gross_return_pct"],
        "cost_drag_bps": net_return_result["cost_drag_bps"],
        "timestamp": "2026-05-29"
    })

    # Step 4: Envelope + Audit + Export
    envelope = OutputEnvelope(pipeline_id="IRF-06", run_id="IRF-06-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-06-evt-001", "PORTFOLIO_ALPHA_REVIEW", pipeline_id="IRF-06")
    export = AuditExportPack.generate(envelope, [audit])

    return {
        "horizon_result": horizon_result,
        "net_return_result": net_return_result,
        "report_len": len(report),
        "envelope": envelope.to_dict(),
        "audit": audit.to_dict(),
        "export_manifest": export,
    }


def irf07_multi_strategy_chain():
    """IRF-07: Multi-Strategy Portfolio — 多策略组合"""
    from zmatrix.factor_factory.factory import FactorPromotionGate
    from zmatrix.execution_quality.execution import TransactionCostModel, PaperOrderPreview

    # Step 1: FactorPromotionGate.check()
    promotion_result = FactorPromotionGate.check(
        horizon_ready=True, net_return_ready=True,
        evidence_ready=True, pit_safe=True, sample_size=500
    )

    # Step 2: TransactionCostModel.compute()
    cost_result = TransactionCostModel.compute(10, 11, 1000)

    # Step 3: PaperOrderPreview.generate()
    preview_result = PaperOrderPreview.generate(
        "MULTI_STRAT", "PAPER_ONLY_OBSERVE", 100, cost_result.get("total_cost_pct", 0.15)
    )

    # Step 4: ReportRenderer.render("multi_strategy_portfolio")
    renderer = ReportRenderer()
    report = renderer.render("multi_strategy_portfolio", {
        "promotion_allowed": promotion_result["promotion_allowed"],
        "research_validated": promotion_result["research_validated"],
        "total_cost_pct": cost_result["total_cost_pct"],
        "preview_action": preview_result["action"],
        "timestamp": "2026-05-29"
    })

    # Step 5: Envelope + Audit + Export
    envelope = OutputEnvelope(pipeline_id="IRF-07", run_id="IRF-07-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-07-evt-001", "MULTI_STRATEGY", pipeline_id="IRF-07")
    export = AuditExportPack.generate(envelope, [audit])

    return {
        "promotion_result": promotion_result,
        "cost_result": cost_result,
        "preview_result": preview_result,
        "report_len": len(report),
        "envelope": envelope.to_dict(),
        "audit": audit.to_dict(),
        "export_manifest": export,
    }


def irf08_factor_data_chain():
    """IRF-08: Factor & Proprietary Data Factory — 因子与专有数据工厂"""
    from zmatrix.dataforge.forge import DataQualityScore
    from zmatrix.factor_factory.factory_depth import OutcomeHorizonIntegrity
    from zmatrix.factor_factory.factory import FactorPromotionGate

    # Step 1: EvidenceCard + DataQualityScore.compute()
    card = EvidenceCard("ev8", "DATA_FACTORY", "2026-05-29", "DS_R_PRICE", "close", 10.5, "2026-05-29")
    card.pit_status = "PIT_SAFE"
    card.freshness_status = "FRESH"
    quality_result = DataQualityScore.compute(card)

    # Step 2: OutcomeHorizonIntegrity.check()
    forward_bars = [f"2026-06-{i:02d}" for i in range(1, 62)]
    horizon_result = OutcomeHorizonIntegrity.check(forward_bars, "t60")

    # Step 3: FactorPromotionGate.check()
    promotion_result = FactorPromotionGate.check(
        horizon_ready=horizon_result["horizon_ready"],
        net_return_ready=True,
        evidence_ready=quality_result["quality_status"] == "READY",
        pit_safe=True,
        sample_size=500
    )

    # Step 4: Envelope + Audit + Export
    envelope = OutputEnvelope(pipeline_id="IRF-08", run_id="IRF-08-001", status="INTEGRATION_SMOKE", human_review_required=True)
    audit = AuditEvent("IRF-08-evt-001", "FACTOR_DATA", pipeline_id="IRF-08")
    export = AuditExportPack.generate(envelope, [audit])

    return {
        "quality_result": quality_result,
        "horizon_result": horizon_result,
        "promotion_result": promotion_result,
        "envelope": envelope.to_dict(),
        "audit": audit.to_dict(),
        "export_manifest": export,
    }
