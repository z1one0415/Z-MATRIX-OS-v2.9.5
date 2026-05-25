#!/usr/bin/env python3
"""
☯️ Build Architecture Package Checksum Manifest — v2.9.7-arch-RC1
"""
import hashlib
import sys
from pathlib import Path

RC_DIR = Path(__file__).resolve().parent.parent / "release" / "v2.9.7-arch-RC1"
OUTPUT = RC_DIR / "ARTIFACT_CHECKSUMS.txt"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not RC_DIR.exists():
        print(f"❌ directory not found: {RC_DIR}")
        sys.exit(1)

    files = sorted(RC_DIR.iterdir())
    checksums = []
    for f in files:
        if f.is_file() and f.name != "ARTIFACT_CHECKSUMS.txt":
            checksums.append((sha256_file(f), f.stat().st_size, f.name))

    lines = [
        "# Z-MATRIX-OS v2.9.7-arch-RC1 — Architecture Artifact Checksums",
        f"# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST",
        "",
    ]
    for digest, size, name in checksums:
        lines.append(f"{digest}  {name}  ({size} bytes)")
    lines.append("")
    lines.append(f"Total files: {len(checksums)}")

    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"✅ checksums written: {OUTPUT}")
    print(f"   {len(checksums)} files indexed")


if __name__ == "__main__":
    main()
