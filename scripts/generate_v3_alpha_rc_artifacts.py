#!/usr/bin/env python3
"""Generate v3.0-alpha RC JSON artifacts."""
from __future__ import annotations
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

from zmatrix.alpha_rc.manifest_builder import build_v3_alpha_release_manifest
from zmatrix.alpha_rc.verification_matrix import build_v3_alpha_verification_matrix
from zmatrix.alpha_rc.module_inventory import build_v3_alpha_frozen_module_inventory
from zmatrix.alpha_rc.known_limitations import build_v3_alpha_known_limitations

OUT = Path("release/alpha_rc")
OUT.mkdir(parents=True, exist_ok=True)


def write_json(name: str, data: dict):
    path = OUT / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    write_json("v3_alpha_release_manifest_v10.json", build_v3_alpha_release_manifest())
    write_json("v3_alpha_verification_matrix_v10.json", build_v3_alpha_verification_matrix())
    write_json("v3_alpha_frozen_module_inventory_v10.json", build_v3_alpha_frozen_module_inventory())
    print("✅ generated v3 alpha rc artifacts")


if __name__ == "__main__":
    main()
