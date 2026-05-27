#!/usr/bin/env python3
"""
/aibdd-kickoff layout copier (pure file copy).

Copies the invariant template tree (assets/templates/shared/) to the target
boundary codebase root. All placeholder substitution and per-stack tail
appending are handled by 02-execute-layout/SOP.md as post-copy LLM Edit ops.

Usage:
  python3 kickoff_layout.py --decisions-file <path.json>

decisions.json shape:
  {
    "project_root": "/abs/path",
    "boundary_codebase_subdir": "" | "backend" | ...
  }

Other fields (stack / tlb_id / project_spec_language / ...) are read by the SOP,
not by this script.

Emits JSON to stdout: {"ok": true, "boundary_codebase_root": "..."}.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent / "templates" / "shared"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions-file", required=True)
    args = parser.parse_args()

    decisions = json.loads(Path(args.decisions_file).read_text())
    project_root = Path(decisions["project_root"])
    subdir = decisions.get("boundary_codebase_subdir", "")
    dst = project_root / subdir if subdir else project_root

    shutil.copytree(SHARED_DIR, dst, dirs_exist_ok=True)

    # Strip seed .gitkeep at project root if present (legacy hygiene).
    seed_gitkeep = project_root / ".gitkeep"
    if seed_gitkeep.exists():
        seed_gitkeep.unlink()

    print(json.dumps({
        "ok": True,
        "boundary_codebase_root": str(dst),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
