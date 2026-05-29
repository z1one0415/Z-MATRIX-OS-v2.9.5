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
