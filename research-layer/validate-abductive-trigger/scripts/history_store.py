#!/usr/bin/env python3
"""Compatibility entry point; all History storage lives in research-history."""
import importlib.util
import json
from pathlib import Path
import sys


def load_backend():
    skill = Path(__file__).resolve().parent.parent
    candidates = [
        skill.parent / "research-history/scripts/history_store.py",
        skill.parent.parent / "research-records/research-history/scripts/history_store.py",
    ]
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("shared_research_history", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise ImportError("research-history is required for History storage; install it beside Trigger or use its actual script path. Preserve pending events; no fallback log was created.")


try:
    _backend = load_backend()
except ImportError as exc:
    if __name__ == "__main__":
        print(json.dumps({"status": "blocked", "reason": str(exc)}), file=sys.stderr)
        sys.exit(1)
    raise


def __getattr__(name):
    return getattr(_backend, name)


if __name__ == "__main__":
    sys.exit(_backend.main())
