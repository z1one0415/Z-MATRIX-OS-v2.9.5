#!/usr/bin/env python3
"""Check local product readiness for Z-MATRIX-OS V4-PRO."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, replace
from pathlib import Path

from zmatrix.product_runtime.config_env import first_env, first_env_int, load_local_env, merged_env
from zmatrix.product_runtime.local_backend import (
    READINESS_BLOCKED,
    READINESS_PASS,
    ProductRuntimeConfig,
    build_runtime_product_readiness,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ReadinessOptions:
    root: Path = REPO_ROOT
    config: ProductRuntimeConfig = ProductRuntimeConfig()


def build_product_readiness(options: ReadinessOptions = ReadinessOptions()) -> dict:
    root = options.root
    config = replace(options.config, repo_root=root)
    return build_runtime_product_readiness(config, root)


def main() -> int:
    local_env = load_local_env(REPO_ROOT / ".env")
    runtime_env = merged_env(local_env)
    parser = argparse.ArgumentParser(description="Check Z-MATRIX local product readiness")
    parser.add_argument("--host", default=first_env(runtime_env, ("Z_MATRIX_PRODUCT_HOST", "ZMATRIX_BACKEND_HOST"), "127.0.0.1"))
    parser.add_argument("--port", type=int, default=first_env_int(runtime_env, ("Z_MATRIX_PRODUCT_PORT", "ZMATRIX_BACKEND_PORT"), 8765))
    parser.add_argument("--workspace-id", default=first_env(runtime_env, ("Z_MATRIX_WORKSPACE_ID",), "ws_personal_z_prime"))
    parser.add_argument("--public-root", default=first_env(runtime_env, ("Z_MATRIX_COCKPIT_PUBLIC_ROOT",), "apps/cockpit_web/public/api/cockpit"))
    parser.add_argument("--registry-path", default="data/research_db/agent/registry/skill_registry.generated.json")
    parser.add_argument("--vendor-root", default=first_env(runtime_env, ("Z_MATRIX_VENDOR_ROOT",), "data/research_db/market_data/vendor/tushare_5y"))
    args = parser.parse_args()
    config = ProductRuntimeConfig(
        host=args.host,
        port=args.port,
        public_root=Path(args.public_root),
        registry_path=Path(args.registry_path),
        vendor_root=Path(args.vendor_root),
        workspace_id=args.workspace_id,
        env=runtime_env,
    )
    packet = build_product_readiness(ReadinessOptions(config=config))
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0 if packet["status"] == READINESS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
