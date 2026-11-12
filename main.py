"""Copy the finished entry image to the output directory.

The entry image (entry.png, a JPEG) sits beside this program in the
repository. This program copies it byte for byte to the output directory
(env MAKEFUN_OUTPUT_DIR, else /output) as entry.png. Pure copy: no
network, no clock, no randomness, so the output is identical every run.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise SystemExit(f"missing entry image: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    if dest.stat().st_size != source.stat().st_size:
        raise SystemExit("copy size mismatch")


if __name__ == "__main__":
    main()
