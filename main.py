#!/usr/bin/env python3
"""Copy the entry image to the output directory, byte for byte.

The image lives next to this program in the repository. The output is a
pure copy, so it is deterministic by construction: the same bytes out
every run.
"""

import os
import shutil
from pathlib import Path

SOURCE_NAME = "entry.png"


def main() -> None:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    if not source.is_file():
        raise SystemExit(f"missing entry image: {source}")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / SOURCE_NAME
    shutil.copyfile(source, destination)
    if destination.stat().st_size != source.stat().st_size:
        raise SystemExit("incomplete copy: output size differs from source")


if __name__ == "__main__":
    main()
