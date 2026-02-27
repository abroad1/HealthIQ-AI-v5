"""
Sprint 19 Layer 2 — Lifestyle Registry Loader.

Minimal loader: loads lifestyle_registry.yaml and returns a dict.
Engine must accept pre-loaded registry; no file I/O inside the engine.
"""

from pathlib import Path
from typing import Any, Dict

import yaml


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "lifestyle_registry.yaml"


def load_lifestyle_registry() -> Dict[str, Any]:
    """Load lifestyle_registry.yaml and return the parsed dict."""
    path = _registry_path()
    if not path.exists():
        raise FileNotFoundError(f"lifestyle_registry_loader: registry missing: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("lifestyle_registry_loader: invalid registry payload")
    return payload
