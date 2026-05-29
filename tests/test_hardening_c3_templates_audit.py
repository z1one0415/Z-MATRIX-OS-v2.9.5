"""V4.0 Hardening-C3 — Templates + Audit ZIP export tests"""
from pathlib import Path
import json
import zipfile
import tempfile
import shutil

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "zmatrix" / "report_templates"

TEMPLATE_NAMES = [
    "single_stock_research",
    "research_council_review",
    "evidence_data_quality",
    "strategy_validation",
    "factor_validation",
    "multi_strategy_portfolio",
    "paper_execution_plan",
    "execution_route_competition",
    "portfolio_alpha_daily",
    "account_risk_weekly",
    "missed_opportunity_postmortem",
    "audit_trail",
]

REQUIRED_SECTIONS = [
    "## Data Fields",
    "## Risk Assessment",
    "## Safety Declaration",
    "## Audit Trail",
]

# ── Sub-task D1: Template file existence and structure ────────────

def test_12_template_files_exist():
    """All 12 report template .md files exist in zmatrix/report_templates/."""
    missing = []
    for name in TEMPLATE_NAMES:
        p = TEMPLATE_DIR / f"{name}.md"
        if not p.exists():
            missing.append(name)
    assert not missing, f"Missing templates: {missing}"


def test_each_template_has_sections():
    """Every template contains Data Fields, Risk Assessment, Safety Declaration, and Audit Trail."""
    failures = {}
    for name in TEMPLATE_NAMES:
        p = TEMPLATE_DIR / f"{name}.md"
        text = p.read_text(encoding="utf-8")
        missing_sections = [s for s in REQUIRED_SECTIONS if s not in text]
        if missing_sections:
            failures[name] = missing_sections
    assert not failures, f"Templates missing sections: {failures}"


# ── Sub-task D2: Renderer snapshot methods ───────────────────────

def test_renderer_snapshot():
    """render_snapshot returns a string that contains template content (not just a stub)."""
    from zmatrix.reports.renderer import ReportRenderer

    rr = ReportRenderer()
    ctx = {
        "timestamp": "2026-05-29T15:00:00Z",
        "ticker": "000001",
        "stock_name": "平安银行",
        "pipeline_id": "Z-G03",
        "run_id": "run-001",
        "input_hash": "abc123",
        "output_hash": "def456",
        "audit_event_id": "ev-001",
        "safety_gate_passed": "True",
    }
    out = rr.render_snapshot("single_stock_research", ctx)
    assert "000001" in out
    assert "平安银行" in out
    assert "PAPER-ONLY" in out
    assert "NOT ALLOWED" in out
    # Template sections present
    assert "## Data Fields" in out
    assert "## Risk Assessment" in out
    assert "## Safety Declaration" in out
    assert "## Audit Trail" in out


def test_snapshot_to_file():
    """snapshot_to_file writes rendered content to a real file."""
    from zmatrix.reports.renderer import ReportRenderer

    rr = ReportRenderer()
    ctx = {"timestamp": "2026-05-29T15:00:00Z", "ticker": "000001"}
    tmp = Path(tempfile.mkdtemp()) / "snapshot_test_output.md"
    try:
        result_path = rr.snapshot_to_file("single_stock_research", ctx, str(tmp))
        assert tmp.exists()
        assert result_path == str(tmp.resolve())
        content = tmp.read_text(encoding="utf-8")
        assert "PAPER-ONLY" in content
        assert "NOT ALLOWED" in content
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)


# ── Sub-task D3: Audit ZIP export ────────────────────────────────

def test_audit_zip_export():
    """export_to_zip generates a real .zip file on disk."""
    from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

    envelope = OutputEnvelope(
        pipeline_id="Z-G03",
        run_id="run-zip-001",
        status="COMPLETED",
    )
    events = [
        AuditEvent("ev-1", "PIPELINE_START"),
        AuditEvent("ev-2", "PIPELINE_END"),
    ]
    tmpdir = Path(tempfile.mkdtemp())
    zip_path = tmpdir / "audit_export_test.zip"
    try:
        result = AuditExportPack.export_to_zip(envelope, events, str(zip_path))
        assert zip_path.exists()
        assert zip_path.stat().st_size > 0
        assert result["real_trade_allowed"] == False
        assert result["size_bytes"] > 0
        assert result["file_count"] == 5  # manifest + envelope + 2 events + safety
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_audit_zip_contents():
    """ZIP contains manifest.json, envelope.json, events/*.json, safety_declaration.txt."""
    from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

    envelope = OutputEnvelope(pipeline_id="Z-G06", run_id="run-zip-002")
    events = [
        AuditEvent("ev-a", "REVIEW_START"),
        AuditEvent("ev-b", "REVIEW_PASS"),
        AuditEvent("ev-c", "REVIEW_END"),
    ]
    tmpdir = Path(tempfile.mkdtemp())
    zip_path = tmpdir / "contents_test.zip"
    try:
        AuditExportPack.export_to_zip(envelope, events, str(zip_path))
        with zipfile.ZipFile(str(zip_path), "r") as zf:
            names = set(zf.namelist())
        assert "manifest.json" in names
        assert "envelope.json" in names
        assert "safety_declaration.txt" in names
        assert "events/event_0000.json" in names
        assert "events/event_0001.json" in names
        assert "events/event_0002.json" in names
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_audit_zip_no_trade_in_files():
    """Every JSON file inside the ZIP has real_trade_allowed=False."""
    from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

    envelope = OutputEnvelope(pipeline_id="Z-G03", run_id="run-safety")
    events = [AuditEvent("ev-1", "SAFETY_TEST")]
    tmpdir = Path(tempfile.mkdtemp())
    zip_path = tmpdir / "safety_test.zip"
    try:
        AuditExportPack.export_to_zip(envelope, events, str(zip_path))
        with zipfile.ZipFile(str(zip_path), "r") as zf:
            for name in zf.namelist():
                if name.endswith(".json"):
                    data = json.loads(zf.read(name).decode("utf-8"))
                    assert data.get("real_trade_allowed") == False, (
                        f"{name} has real_trade_allowed={data.get('real_trade_allowed')}"
                    )
                    assert data.get("broker_order_allowed") == False, (
                        f"{name} has broker_order_allowed={data.get('broker_order_allowed')}"
                    )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_audit_zip_cleanup():
    """Temporary files are cleaned up after test (no left-over artifacts)."""
    from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

    tmpdir = Path(tempfile.mkdtemp())
    zip_path = tmpdir / "cleanup_test.zip"
    try:
        AuditExportPack.export_to_zip(
            OutputEnvelope(),
            [AuditEvent("ev-clean", "CLEANUP_TEST")],
            str(zip_path),
        )
        assert zip_path.exists()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    # After rmtree the path should not exist
    assert not zip_path.exists()
