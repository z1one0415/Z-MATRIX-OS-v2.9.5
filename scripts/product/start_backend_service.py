#!/usr/bin/env python3
"""Start or inspect the local Z-MATRIX product backend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zmatrix.product_runtime import ProductRuntimeConfig, build_product_status, serve_product_runtime


def main() -> int:
    parser = argparse.ArgumentParser(description="Z-MATRIX local product backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--public-root", default="apps/cockpit_web/public/api/cockpit")
    parser.add_argument("--registry-path", default="data/research_db/agent/registry/skill_registry.generated.json")
    parser.add_argument("--vendor-root", default="data/research_db/market_data/vendor/tushare_5y")
    parser.add_argument("--workspace-id", default="ws_personal_z_prime")
    parser.add_argument("--check", action="store_true", help="Print backend status and exit")
    args = parser.parse_args()

    config = ProductRuntimeConfig(
        host=args.host,
        port=args.port,
        public_root=Path(args.public_root),
        registry_path=Path(args.registry_path),
        vendor_root=Path(args.vendor_root),
        workspace_id=args.workspace_id,
    )
    if args.check:
        print(json.dumps(build_product_status(config), ensure_ascii=False, indent=2))
        return 0
    serve_product_runtime(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
