"""Bootstrap sys.path so sibling skills can import aibdd-core lib modules."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_aibdd_core_scripts_on_path() -> Path:
    scripts_dir = Path(__file__).resolve().parents[1]
    scripts_str = str(scripts_dir)
    if scripts_str not in sys.path:
        sys.path.insert(0, scripts_str)
    return scripts_dir
