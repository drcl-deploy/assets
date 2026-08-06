"""Command-line interface for asset paths and generation."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .paths import GENERATED_ROOT, PACKAGE_ROOT


def _print_help() -> None:
    parser = argparse.ArgumentParser(prog="assets")
    parser.add_argument("command", nargs="?", choices=("path", "generated-path", "generate"))
    parser.print_help()


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        _print_help()
        return 0
    command, *rest = args
    if command == "path":
        print(PACKAGE_ROOT)
        return 0
    if command == "generated-path":
        print(GENERATED_ROOT)
        return 0
    if command == "generate":
        from .omni_objects.make_object_models import main as generate

        return generate(rest)
    print(f"assets: unknown command: {command}", file=sys.stderr)
    _print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
