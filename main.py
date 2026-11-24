#!/usr/bin/env python3
"""news-23 b56 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

EXPECTED_W, EXPECTED_H = 1024, 1024
MAX_BYTES = 1024 * 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is empty", file=sys.stderr)
        return 1
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == repo_dir or os.path.abspath(out_dir).startswith(repo_dir + os.sep):
        print("error: MAKEFUN_OUTPUT_DIR must be outside the repo", file=sys.stderr)
        return 1
    src = os.path.join(repo_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: not a PNG", file=sys.stderr)
        return 1
    if data[12:16] != b"IHDR":
        print("error: missing IHDR", file=sys.stderr)
        return 1
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        print(f"error: expected {EXPECTED_W}x{EXPECTED_H}, got {w}x{h}", file=sys.stderr)
        return 1
    if depth != 8 or ctype not in (2, 6):
        print("error: unexpected bit depth / colour type", file=sys.stderr)
        return 1
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("error: malformed IEND trailer", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        print("error: output differs from source", file=sys.stderr)
        return 1
    print("wrote", dst)
    print("source sha256", hashlib.sha256(data).hexdigest())
    print("source bytes", len(data))
    print("output sha256", hashlib.sha256(back).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
