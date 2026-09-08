#!/usr/bin/env python3
"""Audit a ResolveNodeKit layout-reference JSON and print compact JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    args = parser.parse_args(argv)
    # Keep this script usable from a source checkout without installation.
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from resolve_node_kit.fusion.processing_snapshot import audit_layout_reference

    result = audit_layout_reference(args.reference)
    # ASCII output is stable across PowerShell code pages and CI subprocesses.
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
