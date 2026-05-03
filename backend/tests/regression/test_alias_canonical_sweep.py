"""
Sentinel Phase 1 — alias/canonical sweep.

Iterates every entry in biomarker_alias_registry.yaml and asserts that each
declared alias resolves to the declared canonical_id through AliasRegistryService.

Evidence model:
  - trigger: registry YAML path
  - input: each alias string in the registry
  - expected: canonical_id declared alongside the alias
  - actual: resolver.resolve(alias)
  - pass/fail: equality check
  - customer impact: alias miss → wrong biomarker in pipeline → wrong analytical output
  - governance escalation: no (SSOT read-only; no mutations here)
"""
import os
import sys

import pytest
import yaml

# Ensure backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.canonical.alias_registry_service import get_alias_registry_service

ALIAS_REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "ssot", "biomarker_alias_registry.yaml"
)


def _load_registry() -> dict:
    with open(ALIAS_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@pytest.mark.regression
class TestAliasCanonicSweep:
    """Full alias sweep — every registry alias must resolve to its declared canonical_id."""

    def test_registry_file_exists_and_loads(self):
        assert os.path.exists(ALIAS_REGISTRY_PATH), (
            f"SSOT alias registry not found at {ALIAS_REGISTRY_PATH}"
        )
        registry = _load_registry()
        assert len(registry) > 0, "Alias registry must not be empty"

    def test_every_alias_resolves_to_declared_canonical(self):
        """
        Evidence: each alias in the registry → AliasRegistryService.resolve() → expected canonical_id.
        Customer impact: alias miss → wrong biomarker ingested → analytical output corruption.
        """
        registry = _load_registry()
        resolver = get_alias_registry_service()

        failures: list[str] = []
        for canonical_key, definition in registry.items():
            if not isinstance(definition, dict):
                continue
            declared_canonical = definition.get("canonical_id", canonical_key)
            for alias in definition.get("aliases", []):
                resolved = resolver.resolve(alias)
                if resolved != declared_canonical:
                    failures.append(
                        f"alias='{alias}' | expected='{declared_canonical}' | got='{resolved}'"
                    )

        assert not failures, (
            f"{len(failures)} alias resolution failure(s) — first 20 shown:\n"
            + "\n".join(failures[:20])
        )

    def test_canonical_id_resolves_to_itself(self):
        """Every canonical_id must resolve to itself (identity check)."""
        registry = _load_registry()
        resolver = get_alias_registry_service()

        failures: list[str] = []
        for canonical_key, definition in registry.items():
            if not isinstance(definition, dict):
                continue
            canonical_id = definition.get("canonical_id", canonical_key)
            resolved = resolver.resolve(canonical_id)
            if resolved != canonical_id:
                failures.append(f"canonical='{canonical_id}' resolved_to='{resolved}'")

        assert not failures, (
            f"{len(failures)} canonical self-resolution failure(s):\n" + "\n".join(failures)
        )

    def test_no_alias_resolves_to_unmapped(self):
        """No declared alias should return an 'unmapped_*' result."""
        registry = _load_registry()
        resolver = get_alias_registry_service()

        unmapped: list[str] = []
        for canonical_key, definition in registry.items():
            if not isinstance(definition, dict):
                continue
            for alias in definition.get("aliases", []):
                resolved = resolver.resolve(alias)
                if resolved.startswith("unmapped_"):
                    unmapped.append(f"alias='{alias}' (under canonical '{canonical_key}') → {resolved}")

        assert not unmapped, (
            f"{len(unmapped)} alias(es) returned 'unmapped_*' — first 20:\n"
            + "\n".join(unmapped[:20])
        )
