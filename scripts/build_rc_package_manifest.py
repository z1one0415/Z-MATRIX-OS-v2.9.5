#!/usr/bin/env python3
"""
☯️ Build RC Package Checksum Manifest — v2.9.6-RC1

Generates SHA256 checksums for all files in release/v2.9.6-RC1/.
Output: release/v2.9.6-RC1/ARTIFACT_CHECKSUMS.txt

No compression, no upload, no tag.
"""
import hashlib
import os
import sys
from pathlib import Path

RC_DIR = Path(__file__).resolve().parent.parent / "release" / "v2.9.6-RC1"
OUTPUT = RC_DIR / "ARTIFACT_CHECKSUMS.txt"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not RC_DIR.exists():
        print(f"❌ RC package directory not found: {RC_DIR}")
        sys.exit(1)

    files = sorted(RC_DIR.iterdir())
    checksums = []

    for f in files:
        if f.is_file() and f.name != "ARTIFACT_CHECKSUMS.txt":
            digest = sha256_file(f)
            size = f.stat().st_size
            checksums.append((digest, size, f.name))

    lines = [
        "# Z-MATRIX-OS v2.9.6-RC1 — Artifact Checksums",
        f"# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST",
        f"# Directory: {RC_DIR}",
        "",
    ]

    for digest, size, name in checksums:
        lines.append(f"{digest}  {name}  ({size} bytes)")

    lines.append("")
    lines.append(f"Total files: {len(checksums)}")

    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"✅ Checksums written to {OUTPUT}")
    print(f"   {len(checksums)} files indexed")

    # 验证: 读取并校验
    print()
    print("   Verifying...")
    all_ok = True
    for digest, size, name in checksums:
        actual = sha256_file(RC_DIR / name)
        if actual == digest:
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name}: checksum mismatch!")
            all_ok = False

    if all_ok:
        print(f"\n✅ All {len(checksums)} checksums verified.")
    else:
        print(f"\n❌ Checksum verification failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
