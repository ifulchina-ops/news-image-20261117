#!/usr/bin/env python3
"""Entry point for the news-image-20261117 competition.

Copies the pre-rendered front page (art.png, sitting next to this
file) to $MAKEFUN_OUTPUT_DIR/entry.png, defaulting to /output.
The copy is checked before it is trusted: the source must be a real
PNG no larger than 1 MiB and no bigger than 1024x1024, and the
destination must hash identically to the source. No network access.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1 * 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) parsed from the PNG IHDR chunk."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError(f"{path} is not a PNG file")
    length, kind = struct.unpack(">I4s", head[8:16])
    if kind != b"IHDR" or length != 13:
        raise ValueError(f"{path} has no valid IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "art.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(source)
    if not os.path.isfile(source):
        raise SystemExit(f"art.png not found next to main.py ({source})")
    if size > MAX_BYTES:
        raise SystemExit(f"art.png is {size} bytes, over the 1 MiB limit")
    width, height = read_png_size(source)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"art.png is {width}x{height}, over 1024x1024")

    os.makedirs(out_dir, exist_ok=True)
    with open(source, "rb") as src, open(dest, "wb") as dst:
        for chunk in iter(lambda: src.read(65536), b""):
            dst.write(chunk)

    if sha256_of(source) != sha256_of(dest):
        raise SystemExit("entry.png does not match art.png (SHA-256 mismatch)")
    print(f"wrote {dest} ({width}x{height}, {size} bytes, "
          f"sha256 {sha256_of(dest)[:16]}...)")


if __name__ == "__main__":
    main()
