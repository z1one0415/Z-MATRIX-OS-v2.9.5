from __future__ import annotations

import json
from pathlib import Path

from scripts.product.build_local_workstation_package import PACKET_NAMES, PackageOptions, build_package


def test_workstation_package_builds_manifest_and_checksums(tmp_path: Path):
    root = _make_minimal_product_root(tmp_path / "repo")
    output_dir = tmp_path / "package"

    manifest = build_package(
        PackageOptions(root=root, output_dir=output_dir, include_archive=False, include_source=True)
    )

    manifest_path = output_dir / "PRODUCT_MANIFEST.json"
    manifest_from_disk = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_PACKAGE_BUILT"
    assert manifest_from_disk["status"] == manifest["status"]
    assert manifest_from_disk["components"]["cockpit_packet_file_count"] == len(PACKET_NAMES)
    assert manifest_from_disk["components"]["source_snapshot_included"] is True
    assert manifest_from_disk["data_policy"]["raw_vendor_data_included"] is False
    assert manifest_from_disk["safety"]["broker_runtime"] == "BLOCKED"
    assert (output_dir / "START_HERE.md").is_file()
    assert (output_dir / "ARTIFACT_CHECKSUMS.txt").read_text(encoding="utf-8").count("PRODUCT_MANIFEST.json") == 1


def test_workstation_package_excludes_private_local_data(tmp_path: Path):
    root = _make_minimal_product_root(tmp_path / "repo")
    private_file = root / "data/research_db/market_data/vendor/tushare_5y/20260613/private.csv"
    private_file.parent.mkdir(parents=True, exist_ok=True)
    private_file.write_text("local only\n", encoding="utf-8")

    output_dir = tmp_path / "package"
    build_package(PackageOptions(root=root, output_dir=output_dir, include_archive=False, include_source=True))

    copied_paths = {path.relative_to(output_dir).as_posix() for path in output_dir.rglob("*") if path.is_file()}
    assert "source/data/research_db/market_data/vendor/tushare_5y/20260613/private.csv" not in copied_paths
    assert "source/data/research_db/agent/registry/skill_registry.generated.json" in copied_paths


def _make_minimal_product_root(root: Path) -> Path:
    files = {
        ".env.example": "LOCAL_ENV_TEMPLATE=\n",
        "AGENTS.md": "agent instructions\n",
        "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md": "# runbook\n",
        "docs/release/Z_MATRIX_OS_V4_PRO_PRODUCT_ACCEPTANCE_STANDARD.md": "# standard\n",
        "scripts/product/start_backend_service.py": "def main():\n    return None\n",
        "scripts/verify_z_matrix_product_smoke.sh": "#!/usr/bin/env bash\nset -euo pipefail\n",
        "scripts/data/ingest_tushare_market_data.py": "def main():\n    return None\n",
        "apps/cockpit_web/README.md": "# cockpit\n",
        "apps/cockpit_web/package.json": "{}\n",
        "apps/cockpit_web/package-lock.json": "{}\n",
        "apps/cockpit_web/.env.example": "VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json\n",
        "apps/cockpit_web/dist/index.html": "<html></html>\n",
        "apps/cockpit_web/src/main.tsx": "export {}\n",
        "zmatrix/product_runtime/local_backend.py": "def build_product_status():\n    return {}\n",
        "tests/product_runtime/test_local_backend.py": "def test_placeholder():\n    assert True\n",
        "data/research_db/agent/registry/skill_registry.generated.json": "[]\n",
        "data/research_db/agent/registry/skill_candidate_index.json": "[]\n",
    }
    for name in PACKET_NAMES:
        files[f"apps/cockpit_web/public/api/cockpit/{name}"] = '{"paperOnly": true}\n'
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root
