"""
KB-HBA1C-GOV1 — Layer B HbA1c single analytical identity.

Runs after canonicalisation (normalize_biomarkers_with_metadata) and before
apply_unit_normalisation, per Automation Bus work package KB-HBA1C-GOV1.

Layer B analytical identity is fixed to biomarker id ``hba1c`` in ``%`` (post unit norm).
The parallel SSOT id ``hba1c_pct`` must not contribute to the same analytical path.
"""

from __future__ import annotations

import copy
from typing import Any, Dict


def arbitrate_hba1c_layer_b_input(biomarkers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic arbitration for HbA1c dual-report-line reality.

    Rules (fixed order, no randomness):
    - If ``hba1c_pct`` is present and ``hba1c`` is absent: copy ``hba1c_pct`` to ``hba1c``
      so core engine (clusters, criticality) receives the required id.
    - If both are present: keep ``hba1c`` only; ``hba1c_pct`` is dropped for this path.
    - Remove ``hba1c_pct`` from the returned dict so it does not reach unit normalisation
      or orchestrator input for Layer B.

    Args:
        biomarkers: Canonical biomarker dict from normalize_biomarkers_with_metadata.

    Returns:
        New dict (deep-copied where needed); does not mutate the input.
    """
    if not biomarkers:
        return biomarkers
    out = copy.deepcopy(biomarkers)
    has_pct = "hba1c_pct" in out
    has_main = "hba1c" in out
    if has_pct and not has_main:
        out["hba1c"] = copy.deepcopy(out["hba1c_pct"])
    if has_pct:
        del out["hba1c_pct"]
    return out
