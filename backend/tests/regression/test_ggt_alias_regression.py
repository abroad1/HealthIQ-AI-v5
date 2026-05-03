"""
Sentinel Phase 1 — Escaped-defect regression: GGT alias miss.

Defect class: ggt_alias_miss
Escaped defect: The runtime key 'Gamma-GlutamilTransferase GGT (Venous)' (misspelling:
glutamil vs glutamyl) was not resolving to canonical 'ggt'. This caused GGT to drop out
of the analytical pipeline entirely for affected uploads.

Fix: Added the misspelled variant explicitly to biomarker_alias_registry.yaml (commit 43e181f).

Evidence model per test:
  - trigger: this file / Sentinel regression pack
  - input: exact alias string(s) that caused the original failure
  - expected: 'ggt'
  - actual: resolver.resolve(input)
  - customer impact: GGT absent from liver panel → liver domain underpowered
  - governance escalation: no (read-only SSOT check)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.canonical.alias_registry_service import get_alias_registry_service

EXPECTED_CANONICAL = "ggt"


@pytest.mark.regression
class TestGGTAliasRegression:
    """Regression guard for the GGT alias miss escaped defect."""

    @pytest.fixture(autouse=True)
    def _resolver(self):
        self.resolver = get_alias_registry_service()

    def _assert_resolves(self, alias: str) -> None:
        resolved = self.resolver.resolve(alias)
        assert resolved == EXPECTED_CANONICAL, (
            f"GGT alias regression FAIL — "
            f"input='{alias}' expected='{EXPECTED_CANONICAL}' got='{resolved}'. "
            f"This is the original escaped-defect input. Customer-facing liver analysis is affected."
        )

    def test_ggt_misspelled_glutamil_venous_alias(self):
        """Original failure input: misspelling 'glutamil' in venous variant."""
        self._assert_resolves("Gamma-GlutamilTransferase GGT (Venous)")

    def test_ggt_misspelled_lowercase_normalised(self):
        """Normalised form of the misspelled variant as the parser would produce."""
        self._assert_resolves("gamma-glutamiltransferase_ggt_(venous)")

    def test_ggt_standard_display_name(self):
        """Standard display name must continue to resolve correctly."""
        self._assert_resolves("GGT")

    def test_ggt_venous_standard(self):
        self._assert_resolves("GGT (Venous)")

    def test_ggt_venous_dash_form(self):
        self._assert_resolves("GGT - venous")

    def test_ggt_gamma_gt_short(self):
        self._assert_resolves("Gamma GT")

    def test_ggt_spelled_out_transferase(self):
        self._assert_resolves("Gamma-Glutamyl Transferase")

    def test_ggt_correctly_spelled_venous_variant(self):
        """Correctly-spelled venous variant must also hold."""
        self._assert_resolves("Gamma-GlutamylTransferase GGT (Venous)")

    def test_ggt_canonical_self_resolves(self):
        """Canonical id 'ggt' must resolve to itself."""
        self._assert_resolves("ggt")
