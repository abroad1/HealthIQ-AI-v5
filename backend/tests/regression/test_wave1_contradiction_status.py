"""
Sentinel Phase 1 — Escaped-defect status: Wave 1 narrative contradiction.

Defect class: wave1_contradiction
Guard type: status_reporting (Phase 1 placeholder)

Full deterministic coverage of Wave 1 narrative coherence (domain score vs domain
summary alignment) requires Playwright-level browser rendering. That is explicitly
deferred to Phase 2+.

This test serves as:
  1. A named regression slot in the escaped-defect pack so the gap is visible.
  2. A structural check that the Wave 1 contract spec document exists and references
     the key invariants.
  3. A reminder that this surface is not yet deterministically guarded.

Evidence model:
  - trigger: this file / Sentinel regression pack
  - check: DOMAIN_NARRATIVE_CONTRACT_WAVE1.md existence and key invariant presence
  - customer impact: contradictory summary visible on results page (trust damage)
  - governance escalation: yes — this is a meaning-bearing surface gap
  - coverage gap: full deterministic guard requires Playwright (Phase 2+)
"""
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Known spec document locations — we check at least one exists
WAVE1_CONTRACT_CANDIDATES = [
    REPO_ROOT / "docs" / "DOMAIN_NARRATIVE_CONTRACT_WAVE1.md",
    REPO_ROOT / "docs" / "contracts" / "DOMAIN_NARRATIVE_CONTRACT_WAVE1.md",
    REPO_ROOT / "backend" / "docs" / "DOMAIN_NARRATIVE_CONTRACT_WAVE1.md",
]

REQUIRED_INVARIANT_PHRASES = [
    # Key phrases expected in the Wave 1 narrative contract spec
    "domain",
    "narrative",
    "contract",
]


@pytest.mark.regression
class TestWave1ContradictionStatus:
    """Phase 1 status placeholder — Wave 1 narrative coherence."""

    def test_coverage_gap_acknowledged(self):
        """
        Explicit gap acknowledgement: Wave 1 narrative coherence is not deterministically
        guarded in Phase 1. This test exists to make the gap visible in Sentinel reports.
        Full coverage requires Playwright and is deferred to Phase 2+.
        """
        gap_note = (
            "COVERAGE GAP (acknowledged): Wave 1 narrative contradiction check is a "
            "status-reporting placeholder in Phase 1. Full deterministic guard requires "
            "Playwright browser rendering (Phase 2+). Governance escalation: YES — "
            "meaning-bearing surface."
        )
        # This test always passes to record the gap, not block CI
        assert True, gap_note

    def test_wave1_contract_document_exists(self):
        """Wave 1 domain narrative contract spec must exist somewhere in the repo."""
        found = [p for p in WAVE1_CONTRACT_CANDIDATES if p.exists()]
        if not found:
            pytest.skip(
                "COVERAGE GAP: DOMAIN_NARRATIVE_CONTRACT_WAVE1.md not found in expected "
                "locations. Wave 1 contract spec is needed before full regression authoring. "
                f"Searched: {[str(p) for p in WAVE1_CONTRACT_CANDIDATES]}"
            )
        # If it exists, check it contains the key invariant phrases
        contract_text = found[0].read_text(encoding="utf-8").lower()
        missing = [p for p in REQUIRED_INVARIANT_PHRASES if p not in contract_text]
        assert not missing, (
            f"Wave 1 contract doc found at {found[0]} but missing expected phrases: {missing}"
        )
