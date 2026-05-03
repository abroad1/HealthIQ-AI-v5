"""
Sentinel Phase 1 — Escaped-defect regression: bilirubin canonical mismatch.

Defect class: bilirubin_canonical_mismatch
Escaped defect: The alias 'bilirubin_total_(venous)' (observed live parser / lab export
runtime key) was resolving to 'total_bilirubin' rather than the canonical 'bilirubin'.
This caused the downstream liver panel to use the wrong canonical key.

Fix: Added 'bilirubin_total_(venous)' explicitly to the bilirubin entry in
biomarker_alias_registry.yaml (commit 43e181f). The comment in the registry reads:
  # Live parser / lab export (observed trace): canonical resolves to bilirubin, not total_bilirubin

Evidence model per test:
  - trigger: this file / Sentinel regression pack
  - input: exact alias strings that caused or could cause the mismatch
  - expected: 'bilirubin'
  - actual: resolver.resolve(input)
  - customer impact: bilirubin absent or under wrong key → liver domain under-informed
  - governance escalation: no (read-only SSOT check)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.canonical.alias_registry_service import get_alias_registry_service

EXPECTED_CANONICAL = "bilirubin"


@pytest.mark.regression
class TestBilirubinCanonicalRegression:
    """Regression guard for the bilirubin canonical mismatch escaped defect."""

    @pytest.fixture(autouse=True)
    def _resolver(self):
        self.resolver = get_alias_registry_service()

    def _assert_resolves(self, alias: str) -> None:
        resolved = self.resolver.resolve(alias)
        assert resolved == EXPECTED_CANONICAL, (
            f"Bilirubin canonical regression FAIL — "
            f"input='{alias}' expected='{EXPECTED_CANONICAL}' got='{resolved}'. "
            f"This input was the original escaped-defect vector. Customer liver analysis affected."
        )

    def test_bilirubin_total_venous_exact_runtime_key(self):
        """Original failure input: runtime key as emitted by live parser / lab export."""
        self._assert_resolves("bilirubin_total_(venous)")

    def test_bilirubin_total_venous_display_form(self):
        self._assert_resolves("Bilirubin Total (Venous)")

    def test_bilirubin_total_venous_dash_form(self):
        self._assert_resolves("Bilirubin Total - venous")

    def test_bilirubin_display_name(self):
        self._assert_resolves("Bilirubin")

    def test_bilirubin_total_display(self):
        self._assert_resolves("Bilirubin Total")

    def test_total_bilirubin_display(self):
        self._assert_resolves("Total Bilirubin")

    def test_bilirubin_canonical_self_resolves(self):
        """Canonical 'bilirubin' must resolve to itself."""
        self._assert_resolves("bilirubin")

    def test_does_not_resolve_to_total_bilirubin(self):
        """Regression: must never return 'total_bilirubin' (the pre-fix wrong canonical)."""
        resolved = self.resolver.resolve("bilirubin_total_(venous)")
        assert resolved != "total_bilirubin", (
            f"Bilirubin regression FAIL — alias 'bilirubin_total_(venous)' resolved to "
            f"'total_bilirubin'. This is the pre-fix wrong canonical. Fix has regressed."
        )
