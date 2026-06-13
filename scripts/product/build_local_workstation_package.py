#!/usr/bin/env python3
"""Build a local workstation package for Z-MATRIX-OS V4-PRO."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "build" / "product_packages" / "Z-MATRIX-OS-V4-PRO-local-workstation"
PACKAGE_STATUS = "Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_PACKAGE_BUILT"
PACKET_NAMES = (
    "holdings_packet.json",
    "selection_packet.json",
    "history_packet.json",
    "control_compass_packet.json",
    "dayan_ask_packet.json",
)
REQUIRED_FILES = (
    ".env.example",
    "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md",
    "docs/release/Z_MATRIX_OS_V4_PRO_PRODUCT_ACCEPTANCE_STANDARD.md",
    "scripts/product/start_backend_service.py",
    "scripts/product/start_local_workstation.sh",
    "scripts/verify_z_matrix_product_smoke.sh",
    "scripts/data/ingest_tushare_market_data.py",
    "apps/cockpit_web/README.md",
    "apps/cockpit_web/package.json",
    "apps/cockpit_web/package-lock.json",
    "apps/cockpit_web/.env.example",
    "apps/cockpit_web/dist/index.html",
)
SOURCE_DIRS = (
    "zmatrix",
    "scripts",
    "tests",
    "apps/cockpit_web",
)
SOURCE_FILES = (
    ".env.example",
    "AGENTS.md",
    "README.md",
)
IGNORED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}
IGNORED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".zip",
}
DENIED_SOURCE_PARTS = (
    ("data", "research_db", "account", "raw"),
    ("data", "research_db", "account", "staging"),
    ("data", "research_db", "account", "reports", "private"),
    ("data", "research_db", "market_data", "raw"),
    ("data", "research_db", "market_data", "staging"),
    ("data", "research_db", "market_data", "vendor"),
    ("data", "research_db", "master_data", "raw"),
    ("data", "research_db", "master_data", "staging"),
    ("data", "research_db", "master_data", "vendor"),
)


@dataclass(frozen=True)
class PackageOptions:
    root: Path = REPO_ROOT
    output_dir: Path = DEFAULT_OUTPUT_DIR
    version: str = "V4-PRO-local-workstation"
    include_source: bool = True
    include_archive: bool = True
    clean: bool = True


def build_package(options: PackageOptions) -> dict[str, Any]:
    root = options.root.resolve()
    output_dir = options.output_dir.resolve()
    _validate_inputs(root)
    _prepare_output(output_dir, clean=options.clean)

    docs_dir = output_dir / "docs"
    runtime_dir = output_dir / "runtime"
    cockpit_dir = output_dir / "cockpit"
    source_dir = output_dir / "source"
    for directory in (docs_dir, runtime_dir, cockpit_dir):
        directory.mkdir(parents=True, exist_ok=True)

    copied_files = _copy_runtime_files(root, output_dir)
    cockpit_dist_files = _copy_tree(root / "apps/cockpit_web/dist", cockpit_dir / "dist")
    cockpit_packet_files = _copy_tree(root / "apps/cockpit_web/public/api/cockpit", cockpit_dir / "api/cockpit")
    source_files = []
    if options.include_source:
        source_files = _copy_source_snapshot(root, source_dir)

    manifest = _build_manifest(
        options=options,
        output_dir=output_dir,
        copied_files=copied_files,
        cockpit_dist_files=cockpit_dist_files,
        cockpit_packet_files=cockpit_packet_files,
        source_files=source_files,
    )
    _write_start_here(output_dir)
    manifest_path = output_dir / "PRODUCT_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksums = _write_checksums(output_dir)
    manifest["artifact_checksums"] = {"path": "ARTIFACT_CHECKSUMS.txt", "file_count": len(checksums)}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_checksums(output_dir)

    archive_path = ""
    if options.include_archive:
        archive_path = _build_archive(output_dir).as_posix()
    manifest["archive"] = archive_path
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_checksums(output_dir)
    return manifest


def _validate_inputs(root: Path) -> None:
    missing = [path for path in REQUIRED_FILES if not (root / path).is_file()]
    missing.extend(
        f"apps/cockpit_web/public/api/cockpit/{name}"
        for name in PACKET_NAMES
        if not (root / "apps/cockpit_web/public/api/cockpit" / name).is_file()
    )
    if missing:
        joined = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(f"Product package inputs are incomplete:\n{joined}")


def _prepare_output(output_dir: Path, *, clean: bool) -> None:
    if output_dir.exists() and clean:
        if len(output_dir.parts) < 3:
            raise ValueError(f"Refusing to clean unsafe output path: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def _copy_runtime_files(root: Path, output_dir: Path) -> list[str]:
    mapping = {
        ".env.example": output_dir / ".env.example",
        "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md": output_dir
        / "docs"
        / "LOCAL_WORKSTATION_RUNBOOK.md",
        "docs/release/Z_MATRIX_OS_V4_PRO_PRODUCT_ACCEPTANCE_STANDARD.md": output_dir
        / "docs"
        / "PRODUCT_ACCEPTANCE_STANDARD.md",
        "scripts/product/start_backend_service.py": output_dir / "runtime" / "start_backend_service.py",
        "scripts/verify_z_matrix_product_smoke.sh": output_dir / "runtime" / "verify_z_matrix_product_smoke.sh",
        "scripts/data/ingest_tushare_market_data.py": output_dir / "runtime" / "ingest_tushare_market_data.py",
        "apps/cockpit_web/README.md": output_dir / "cockpit" / "README.md",
        "apps/cockpit_web/package.json": output_dir / "cockpit" / "package.json",
        "apps/cockpit_web/package-lock.json": output_dir / "cockpit" / "package-lock.json",
        "apps/cockpit_web/.env.example": output_dir / "cockpit" / ".env.example",
    }
    copied = []
    for source, destination in mapping.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / source, destination)
        copied.append(destination.relative_to(output_dir).as_posix())
    return sorted(copied)


def _copy_source_snapshot(root: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    copied = []
    for file_name in SOURCE_FILES:
        source = root / file_name
        if source.is_file():
            target = destination / file_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(target.relative_to(destination).as_posix())
    for dir_name in SOURCE_DIRS:
        source_dir = root / dir_name
        if source_dir.is_dir():
            copied.extend(_copy_tree(source_dir, destination / dir_name, source_root=source_dir))
    registry_source = root / "data/research_db/agent/registry"
    if registry_source.is_dir():
        copied.extend(_copy_tree(registry_source, destination / "data/research_db/agent/registry", source_root=registry_source))
    return sorted(copied)


def _copy_tree(source: Path, destination: Path, *, source_root: Path | None = None) -> list[str]:
    source_root = source_root or source
    copied = []
    if not source.exists():
        return copied
    for item in sorted(source.rglob("*")):
        if not item.is_file() or _is_ignored(item, source_root):
            continue
        relative = item.relative_to(source_root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied.append(target.relative_to(destination).as_posix())
    return copied


def _is_ignored(path: Path, source_root: Path) -> bool:
    relative_parts = path.relative_to(source_root).parts
    if any(part in IGNORED_DIR_NAMES for part in relative_parts):
        return True
    if path.suffix in IGNORED_FILE_SUFFIXES:
        return True
    joined = path.as_posix().split("/")
    for denied in DENIED_SOURCE_PARTS:
        if _contains_sequence(joined, denied):
            return True
    return False


def _contains_sequence(parts: list[str], sequence: tuple[str, ...]) -> bool:
    width = len(sequence)
    return any(tuple(parts[index : index + width]) == sequence for index in range(len(parts) - width + 1))


def _build_manifest(
    *,
    options: PackageOptions,
    output_dir: Path,
    copied_files: list[str],
    cockpit_dist_files: list[str],
    cockpit_packet_files: list[str],
    source_files: list[str],
) -> dict[str, Any]:
    return {
        "status": PACKAGE_STATUS,
        "version": options.version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": output_dir.as_posix(),
        "scope": "LOCAL_RESEARCH_WORKSTATION",
        "components": {
            "runtime_files": copied_files,
            "cockpit_dist_file_count": len(cockpit_dist_files),
            "cockpit_packet_file_count": len(cockpit_packet_files),
            "source_snapshot_included": bool(source_files),
            "source_file_count": len(source_files),
        },
        "operator_entrypoints": {
            "backend_check": "PYTHONPATH=. python3 scripts/product/start_backend_service.py --check",
            "backend_service": "PYTHONPATH=. python3 scripts/product/start_backend_service.py --host 127.0.0.1 --port 8765",
            "cockpit_dev": "npm --prefix apps/cockpit_web run dev -- --port 5173",
            "local_workstation": "bash scripts/product/start_local_workstation.sh",
            "product_smoke": "bash scripts/verify_z_matrix_product_smoke.sh",
        },
        "data_policy": {
            "raw_vendor_data_included": False,
            "private_account_data_included": False,
            "secret_files_included": False,
            "env_template_included": True,
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "secret_storage": "ENV_ONLY",
        },
    }


def _write_start_here(output_dir: Path) -> None:
    lines = [
        "# Z-MATRIX-OS V4-PRO Local Workstation Package",
        "",
        "This package is a local research workstation preview.",
        "",
        "## First steps",
        "",
        "1. Read `docs/LOCAL_WORKSTATION_RUNBOOK.md`.",
        "2. Copy `.env.example` to `.env` in the source workspace.",
        "3. Configure local-only environment values.",
        "4. Start the backend and cockpit from the source workspace, or run `bash scripts/product/start_local_workstation.sh`.",
        "5. Run `bash scripts/verify_z_matrix_product_smoke.sh` before using a new build.",
        "",
        "## Safety boundary",
        "",
        "- Alpha claim: BLOCKED.",
        "- Promotion: BLOCKED.",
        "- Broker runtime: BLOCKED.",
        "- Real trade: BLOCKED.",
        "- Secrets: environment variables only.",
        "",
    ]
    (output_dir / "START_HERE.md").write_text("\n".join(lines), encoding="utf-8")


def _write_checksums(output_dir: Path) -> list[tuple[str, int, str]]:
    checksums = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file() or path.name == "ARTIFACT_CHECKSUMS.txt":
            continue
        digest = _sha256_file(path)
        relative = path.relative_to(output_dir).as_posix()
        checksums.append((digest, path.stat().st_size, relative))
    lines = [
        "# Z-MATRIX-OS V4-PRO Local Workstation Checksums",
        f"# Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    for digest, size, relative in checksums:
        lines.append(f"{digest}  {relative}  ({size} bytes)")
    lines.append("")
    lines.append(f"Total files: {len(checksums)}")
    (output_dir / "ARTIFACT_CHECKSUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums


def _build_archive(output_dir: Path) -> Path:
    archive_path = output_dir.parent / f"{output_dir.name}.tar.gz"
    if archive_path.exists():
        archive_path.unlink()
    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(output_dir, arcname=output_dir.name)
    return archive_path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Z-MATRIX-OS local workstation package.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR.as_posix())
    parser.add_argument("--version", default="V4-PRO-local-workstation")
    parser.add_argument("--no-source", action="store_true", help="Skip source snapshot copy.")
    parser.add_argument("--no-archive", action="store_true", help="Skip tar.gz artifact creation.")
    parser.add_argument("--no-clean", action="store_true", help="Keep existing output directory contents.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = build_package(
        PackageOptions(
            output_dir=Path(args.output_dir),
            version=args.version,
            include_source=not args.no_source,
            include_archive=not args.no_archive,
            clean=not args.no_clean,
        )
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
