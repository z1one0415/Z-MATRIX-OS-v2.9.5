#!/usr/bin/env python3
"""Export a local research report pack for the product cockpit."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "build" / "research_report_exports" / "Z-MATRIX-research-report-pack"
EXPORT_STATUS = "Z_MATRIX_RESEARCH_REPORT_EXPORT_PACK_BUILT"
DOC_SOURCE_DIRS = (
    Path("docs/cases"),
    Path("docs/audit"),
    Path("docs/release"),
)
RUNTIME_CASE_PATTERNS = (
    "case_expansion_*closeout.json",
    "v10_*audit.json",
    "v10_*pack.json",
    "v11*_*.json",
    "v12*_*.json",
    "v13*_*.json",
)
DENIED_PARTS = {
    "raw",
    "staging",
    "vendor",
    "private",
    "__pycache__",
}


@dataclass(frozen=True)
class ReportExportOptions:
    root: Path = REPO_ROOT
    output_dir: Path = DEFAULT_OUTPUT_DIR
    include_runtime: bool = True


def build_report_export(options: ReportExportOptions = ReportExportOptions()) -> dict[str, Any]:
    root = options.root
    output_dir = options.output_dir
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for source_dir in DOC_SOURCE_DIRS:
        copied.extend(_copy_doc_reports(root / source_dir, output_dir / "docs" / source_dir.name, root=root))
    if options.include_runtime:
        copied.extend(_copy_runtime_reports(root / "runtime_reports" / "cases", output_dir / "runtime_reports" / "cases", root=root))

    manifest = {
        "status": EXPORT_STATUS,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "LOCAL_RESEARCH_REPORT_EXPORT",
        "output_dir": output_dir.as_posix(),
        "artifact_count": len(copied),
        "artifacts": copied,
        "data_policy": {
            "raw_vendor_data_included": False,
            "private_account_data_included": False,
            "secret_files_included": False,
            "local_files_only": True,
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
        },
    }
    _write_json(output_dir / "RESEARCH_REPORT_EXPORT_MANIFEST.json", manifest)
    _write_checksums(output_dir)
    _write_readme(output_dir)
    return manifest


def _copy_doc_reports(source_dir: Path, destination: Path, *, root: Path) -> list[str]:
    if not source_dir.exists():
        return []
    copied = []
    for source in sorted(source_dir.glob("*.md")):
        relative = source.relative_to(root)
        if _is_denied(relative):
            continue
        target = destination / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(relative.as_posix())
    return copied


def _copy_runtime_reports(source_dir: Path, destination: Path, *, root: Path) -> list[str]:
    if not source_dir.exists():
        return []
    copied = []
    seen = set()
    for pattern in RUNTIME_CASE_PATTERNS:
        for source in sorted(source_dir.glob(pattern)):
            relative = source.relative_to(root)
            if source in seen or not source.is_file() or _is_denied(relative):
                continue
            seen.add(source)
            target = destination / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(relative.as_posix())
    return copied


def _is_denied(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & DENIED_PARTS) or path.suffix in {".pyc", ".pyo"}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_checksums(output_dir: Path) -> None:
    lines = []
    for path in sorted(item for item in output_dir.rglob("*") if item.is_file()):
        if path.name == "REPORT_EXPORT_CHECKSUMS.txt":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(output_dir).as_posix()}")
    (output_dir / "REPORT_EXPORT_CHECKSUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_readme(output_dir: Path) -> None:
    lines = [
        "# Z-MATRIX Research Report Export",
        "",
        "This folder contains local research report artifacts for review.",
        "",
        "Safety: alpha claim blocked, promotion blocked, broker runtime blocked, real trade blocked.",
        "Raw vendor data, private account data, and secret files are not included.",
        "",
        "Start with `RESEARCH_REPORT_EXPORT_MANIFEST.json`.",
        "",
    ]
    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export local Z-MATRIX research report artifacts")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR.as_posix())
    parser.add_argument("--no-runtime", action="store_true", help="Skip runtime_reports/cases artifacts")
    args = parser.parse_args()
    manifest = build_report_export(
        ReportExportOptions(output_dir=Path(args.output_dir), include_runtime=not args.no_runtime)
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
