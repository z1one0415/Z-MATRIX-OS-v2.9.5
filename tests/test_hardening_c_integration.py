from pathlib import Path

def test_source_registry():
    from zmatrix.dataforge.forge import SOURCE_REGISTRY
    assert len(SOURCE_REGISTRY) >= 4

def test_evidence_card():
    from zmatrix.dataforge.forge import EvidenceCard
    c = EvidenceCard("ev1", "000001", "2026-05-29")
    assert c.usable_for_production == False

def test_data_quality():
    from zmatrix.dataforge.forge import EvidenceCard, DataQualityScore
    r = DataQualityScore.compute(EvidenceCard("ev1", pit_status="PIT_BLOCKED"))
    assert r['quality_status'] != 'READY'

def test_outcome_horizon():
    from zmatrix.factor_factory.factory import OutcomeHorizonIntegrity
    r = OutcomeHorizonIntegrity.check([{}] * 20, "t20")
    assert r['horizon_ready']
    r2 = OutcomeHorizonIntegrity.check([{}] * 4, "t20")
    assert not r2['horizon_ready']

def test_promotion_gate():
    from zmatrix.factor_factory.factory import FactorPromotionGate
    r = FactorPromotionGate.check(True, True, True, True, 500)
    assert r['production_allowed'] == False

def test_net_return():
    from zmatrix.factor_factory.factory import NetReturnCalculator
    r = NetReturnCalculator.compute(5, 10, 10.5, 1000)
    assert r['net_return_pct'] < r['gross_return_pct']

def test_12_reviewers():
    from zmatrix.research_council.reviewers import REVIEWERS
    assert len(REVIEWERS) == 12

def test_reviewer_output():
    from zmatrix.research_council.reviewers import REVIEWERS
    r = REVIEWERS['R01_MACRO_STRATEGIST'].review({'source': 'tushare'})
    assert r.real_trade_allowed == False

def test_missing_evidence():
    from zmatrix.research_council.reviewers import REVIEWERS
    r = REVIEWERS['R05_SHORT_SELLER_FORENSIC'].review({})
    assert r.review_status == 'DATA_INSUFFICIENT'

def test_report_renderer():
    from zmatrix.reports.renderer import ReportRenderer
    r = ReportRenderer()
    out = r.render("single_stock_research", {"ticker": "000001", "b_score": 80})
    assert "PAPER-ONLY" in out
    assert "NOT ALLOWED" in out

def test_12_templates():
    from zmatrix.reports.renderer import TEMPLATE_NAMES
    assert len(TEMPLATE_NAMES) == 12

def test_missing_field():
    from zmatrix.reports.renderer import MissingFieldPolicy
    r = MissingFieldPolicy.handle("roe", None)
    assert r['rendered'] == 'DATA_INSUFFICIENT'

def test_cost_model():
    from zmatrix.execution_quality.execution import TransactionCostModel
    r = TransactionCostModel.compute(10, 11, 1000)
    assert r['real_trade_allowed'] == False

def test_limit_board():
    from zmatrix.execution_quality.execution import LimitBoardGate
    r = LimitBoardGate.check({'open': 10, 'high': 10, 'low': 10, 'close': 10}, 9.09)
    assert r['action'] == 'NOT_FILLABLE'

def test_paper_preview():
    from zmatrix.execution_quality.execution import PaperOrderPreview
    r = PaperOrderPreview.generate("000001", "PAPER_ONLY_OBSERVE", 100, 10)
    assert r['real_trade_allowed'] == False

def test_capital_curve():
    from zmatrix.account_governance.governance import CapitalCurve
    c = CapitalCurve()
    c.add("2026-01", 1000, 100000)
    r = c.compute()
    assert r['production_allowed'] == False

def test_permission_gate():
    from zmatrix.account_governance.governance import ActionPermissionGate
    r = ActionPermissionGate.check({})
    assert r['action'] == 'PAPER_ONLY'

def test_output_envelope():
    from zmatrix.audit.cockpit_audit import OutputEnvelope
    e = OutputEnvelope()
    assert e.real_trade_allowed == False

def test_audit_event():
    from zmatrix.audit.cockpit_audit import AuditEvent
    e = AuditEvent("ev1", "PIPELINE_RUN")
    assert e.real_trade_allowed == False

def test_forbidden_scan():
    from zmatrix.audit.cockpit_audit import ForbiddenOutputScan
    r = ForbiddenOutputScan.scan("BUY")
    assert not r['passed']

def test_audit_export():
    from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent
    r = AuditExportPack.generate(OutputEnvelope(), [AuditEvent("ev1", "test")])
    assert r['manifest']['real_trade_allowed'] == False

def test_8_irfs():
    from zmatrix.irf.pipelines import IRF_REGISTRY
    assert len(IRF_REGISTRY) == 8

def test_irf_output():
    from zmatrix.irf.pipelines import IRF_REGISTRY
    r = IRF_REGISTRY['IRF-01'].execute()
    assert r['real_trade_allowed'] == False

def test_all_irf_no_trade():
    from zmatrix.irf.pipelines import IRF_REGISTRY
    for irf_id, irf in IRF_REGISTRY.items():
        r = irf.execute()
        assert r['real_trade_allowed'] == False
        assert r['broker_order_allowed'] == False
        assert not r.get('production_allowed', True)

def test_dispatcher_clean():
    t = Path("zmatrix/scoring/dispatcher.py").read_text(encoding="utf-8")
    for b in ["real_trade_allowed=r_mode", "real_trade_allowed=d_mode", "real_trade_allowed=True"]:
        assert b not in t
