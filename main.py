#!/usr/bin/env python3
"""Cutest-picture entry: copy the finished entry image to the output.

The entry image (entry.png, a JPEG) sits beside this program in the repo.
The program copies it byte for byte to MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png when the variable is unset). Pure copy: no network,
no clock, no randomness, so the output is byte-identical on every run.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise SystemExit(f"missing entry image: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    if dest.read_bytes() != source.read_bytes():
        raise SystemExit("copy mismatch: output differs from source")


if __name__ == "__main__":
    main()
