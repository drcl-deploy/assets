"""Filesystem paths for tracked and per-machine generated assets."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from platformdirs import user_data_dir

PACKAGE_ROOT = Path(__file__).resolve().parent


def _package_version() -> str:
    try:
        return version("drcl-sim-assets")
    except PackageNotFoundError:
        return "dev"


GENERATED_ROOT = Path(user_data_dir("drcl-sim-assets", "drcl")) / _package_version()


def asset_path(*parts: str) -> Path:
    """Return a path below the tracked package asset root."""
    return PACKAGE_ROOT.joinpath(*parts)


def generated_path(*parts: str) -> Path:
    """Return a path below the per-machine generated asset root."""
    return GENERATED_ROOT.joinpath(*parts)


def resolve_asset(*parts: str) -> Path:
    """Resolve generated content first, then tracked package content."""
    generated = generated_path(*parts)
    if generated.exists():
        return generated
    tracked = asset_path(*parts)
    if tracked.exists():
        return tracked
    raise FileNotFoundError("Asset does not exist: " + "/".join(parts))
