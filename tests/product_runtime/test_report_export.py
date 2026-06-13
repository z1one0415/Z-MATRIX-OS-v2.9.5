from __future__ import annotations

import json
from pathlib import Path

from scripts.product.export_research_report_pack import EXPORT_STATUS, ReportExportOptions, build_report_export


def test_report_export_builds_manifest_and_checksums(tmp_path: Path):
    root = _make_report_root(tmp_path / "repo")
    output_dir = tmp_path / "report_pack"

    manifest = build_report_export(ReportExportOptions(root=root, output_dir=output_dir))

    manifest_from_disk = json.loads((output_dir / "RESEARCH_REPORT_EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
    copied_paths = {path.relative_to(output_dir).as_posix() for path in output_dir.rglob("*") if path.is_file()}
    assert manifest["status"] == EXPORT_STATUS
    assert manifest_from_disk["status"] == EXPORT_STATUS
    assert manifest["artifact_count"] >= 4
    assert "docs/cases/CASE.md" in copied_paths
    assert "docs/audit/AUDIT.md" in copied_paths
    assert "runtime_reports/cases/v11_6_closeout.json" in copied_paths
    assert "runtime_reports/cases/_test_v5_temp.json" not in copied_paths
    assert manifest["data_policy"]["raw_vendor_data_included"] is False
    assert manifest["safety"]["broker_runtime"] == "BLOCKED"
    assert (output_dir / "REPORT_EXPORT_CHECKSUMS.txt").read_text(encoding="utf-8").count("RESEARCH_REPORT_EXPORT_MANIFEST.json") == 1


def _make_report_root(root: Path) -> Path:
    files = {
        "docs/cases/CASE.md": "# case\n",
        "docs/audit/AUDIT.md": "# audit\n",
        "docs/release/RUNBOOK.md": "# runbook\n",
        "runtime_reports/cases/v11_6_closeout.json": "{}\n",
        "runtime_reports/cases/v13_0_quality_gate.json": "{}\n",
        "runtime_reports/cases/_test_v5_temp.json": "{}\n",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root
