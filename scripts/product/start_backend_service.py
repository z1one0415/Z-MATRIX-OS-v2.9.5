#!/usr/bin/env python3
"""Start or inspect the local Z-MATRIX product backend."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping
from pathlib import Path

from zmatrix.product_runtime import ProductRuntimeConfig, build_product_status, serve_product_runtime

ALLOWED_DOTENV_KEYS = {
    "Z_MATRIX_PRODUCT_HOST",
    "Z_MATRIX_PRODUCT_PORT",
    "Z_MATRIX_WORKSPACE_ID",
    "Z_MATRIX_COCKPIT_PUBLIC_ROOT",
    "Z_MATRIX_VENDOR_ROOT",
    "TUSHARE_TOKEN",
    "DEEPSEEK_API_KEY",
    "ZMATRIX_BACKEND_HOST",
    "ZMATRIX_BACKEND_PORT",
}


def main() -> int:
    local_env = _load_local_env()
    merged_env = _merged_env(local_env)
    parser = argparse.ArgumentParser(description="Z-MATRIX local product backend")
    parser.add_argument("--host", default=_first_env(merged_env, ("Z_MATRIX_PRODUCT_HOST", "ZMATRIX_BACKEND_HOST"), "127.0.0.1"))
    parser.add_argument("--port", type=int, default=_first_env_int(merged_env, ("Z_MATRIX_PRODUCT_PORT", "ZMATRIX_BACKEND_PORT"), 8765))
    parser.add_argument("--public-root", default=_first_env(merged_env, ("Z_MATRIX_COCKPIT_PUBLIC_ROOT",), "apps/cockpit_web/public/api/cockpit"))
    parser.add_argument("--registry-path", default="data/research_db/agent/registry/skill_registry.generated.json")
    parser.add_argument("--vendor-root", default=_first_env(merged_env, ("Z_MATRIX_VENDOR_ROOT",), "data/research_db/market_data/vendor/tushare_5y"))
    parser.add_argument("--workspace-id", default=_first_env(merged_env, ("Z_MATRIX_WORKSPACE_ID",), "ws_personal_z_prime"))
    parser.add_argument("--check", action="store_true", help="Print backend status and exit")
    args = parser.parse_args()

    config = ProductRuntimeConfig(
        host=args.host,
        port=args.port,
        public_root=Path(args.public_root),
        registry_path=Path(args.registry_path),
        vendor_root=Path(args.vendor_root),
        workspace_id=args.workspace_id,
        env=merged_env,
    )
    if args.check:
        print(json.dumps(build_product_status(config), ensure_ascii=False, indent=2))
        return 0
    serve_product_runtime(config)
    return 0


def _load_local_env(path: Path = Path(".env")) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in ALLOWED_DOTENV_KEYS:
            continue
        values[key] = _clean_env_value(value)
    return values


def _clean_env_value(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        return cleaned[1:-1]
    return cleaned


def _merged_env(local_env: Mapping[str, str], process_env: Mapping[str, str] | None = None) -> dict[str, str]:
    source_env = process_env if process_env is not None else os.environ
    merged = dict(local_env)
    for key in ALLOWED_DOTENV_KEYS:
        value = source_env.get(key, "")
        if value:
            merged[key] = value
    return merged


def _first_env(env: Mapping[str, str], keys: tuple[str, ...], fallback: str) -> str:
    for key in keys:
        value = env.get(key, "")
        if value:
            return value
    return fallback


def _first_env_int(env: Mapping[str, str], keys: tuple[str, ...], fallback: int) -> int:
    value = _first_env(env, keys, "")
    if not value:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback


if __name__ == "__main__":
    raise SystemExit(main())
