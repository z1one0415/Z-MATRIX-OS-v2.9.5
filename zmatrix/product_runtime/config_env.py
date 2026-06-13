"""Safe local environment parsing for the product workstation."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

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


def load_local_env(path: Path = Path(".env")) -> dict[str, str]:
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
        values[key] = clean_env_value(value)
    return values


def clean_env_value(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        return cleaned[1:-1]
    return cleaned


def merged_env(local_env: Mapping[str, str], process_env: Mapping[str, str] | None = None) -> dict[str, str]:
    source_env = process_env if process_env is not None else os.environ
    merged = dict(local_env)
    for key in ALLOWED_DOTENV_KEYS:
        value = source_env.get(key, "")
        if value:
            merged[key] = value
    return merged


def first_env(env: Mapping[str, str], keys: tuple[str, ...], fallback: str) -> str:
    for key in keys:
        value = env.get(key, "")
        if value:
            return value
    return fallback


def first_env_int(env: Mapping[str, str], keys: tuple[str, ...], fallback: int) -> int:
    value = first_env(env, keys, "")
    if not value:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback
