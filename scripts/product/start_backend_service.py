#!/usr/bin/env python3
"""Start or inspect the local Z-MATRIX product backend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zmatrix.product_runtime import ProductRuntimeConfig, build_product_status, serve_product_runtime
from zmatrix.product_runtime.config_env import first_env, first_env_int, load_local_env, merged_env


def main() -> int:
    local_env = load_local_env()
    runtime_env = merged_env(local_env)
    parser = argparse.ArgumentParser(description="Z-MATRIX local product backend")
    parser.add_argument("--host", default=first_env(runtime_env, ("Z_MATRIX_PRODUCT_HOST", "ZMATRIX_BACKEND_HOST"), "127.0.0.1"))
    parser.add_argument("--port", type=int, default=first_env_int(runtime_env, ("Z_MATRIX_PRODUCT_PORT", "ZMATRIX_BACKEND_PORT"), 8765))
    parser.add_argument("--public-root", default=first_env(runtime_env, ("Z_MATRIX_COCKPIT_PUBLIC_ROOT",), "apps/cockpit_web/public/api/cockpit"))
    parser.add_argument("--registry-path", default="data/research_db/agent/registry/skill_registry.generated.json")
    parser.add_argument("--vendor-root", default=first_env(runtime_env, ("Z_MATRIX_VENDOR_ROOT",), "data/research_db/market_data/vendor/tushare_5y"))
    parser.add_argument("--workspace-id", default=first_env(runtime_env, ("Z_MATRIX_WORKSPACE_ID",), "ws_personal_z_prime"))
    parser.add_argument("--check", action="store_true", help="Print backend status and exit")
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
    if args.check:
        print(json.dumps(build_product_status(config), ensure_ascii=False, indent=2))
        return 0
    serve_product_runtime(config)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
