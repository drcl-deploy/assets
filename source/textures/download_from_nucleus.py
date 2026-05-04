"""Download NVIDIA Nucleus textures into this directory.

Mirrors the path under "Materials/Base/", so
    {NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Bamboo_Planks/Bamboo_Planks_BaseColor.png
becomes
    textures/Wood/Bamboo_Planks/Bamboo_Planks_BaseColor.png

Idempotent: skips files that already exist on disk.
"""
from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX_MARKER = "/Materials/Base/"

NVIDIA_NUCLEUS_DIR = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/NVIDIA"

URLS = [
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Bamboo_Planks/Bamboo_Planks_BaseColor.png",
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Cherry/Cherry_BaseColor.png",
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Oak/Oak_BaseColor.png",
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Timber/Timber_BaseColor.png",
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Timber_Cladding/Timber_Cladding_BaseColor.png",
    f"{NVIDIA_NUCLEUS_DIR}/Materials/Base/Wood/Walnut_Planks/Walnut_Planks_BaseColor.png",
]


def local_path_for(url: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    idx = path.find(PREFIX_MARKER)
    if idx == -1:
        return ROOT / Path(path).name
    rel = path[idx + len(PREFIX_MARKER):].lstrip("/")
    return ROOT / rel


def download(url: str, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".part")
    with urllib.request.urlopen(url) as r, open(tmp, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)
    tmp.rename(dst)


def main() -> int:
    n_skip = n_get = n_fail = 0
    for url in URLS:
        dst = local_path_for(url)
        rel = dst.relative_to(ROOT)
        if dst.exists():
            print(f"  skip  {rel}")
            n_skip += 1
            continue
        print(f"  get   {rel}  <-  {url}")
        try:
            download(url, dst)
            n_get += 1
        except Exception as e:
            print(f"  FAIL  {rel}: {e}", file=sys.stderr)
            n_fail += 1

    print(f"\ndone: {n_get} downloaded, {n_skip} already present, {n_fail} failed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
