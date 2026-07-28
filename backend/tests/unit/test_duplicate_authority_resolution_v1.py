"""ARCH-CONV-A STOP C correction — named duplicate-authority resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.knowledge.duplicate_authority_resolution_v1 import (
    AuthorityCandidate,
    DuplicateAuthorityConflict,
    resolve_duplicate_authority,
)


def _cand(
    *,
    package_id: str,
    provenance_status: str,
    has_explicit: bool = False,
    has_canonical: bool = False,
    activation_key: str = "signal_demo::inv_demo",
    source_path: str = "",
) -> AuthorityCandidate:
    return AuthorityCandidate(
        activation_key=activation_key,
        source_spec_id="inv_demo",
        package_id=package_id,
        provenance_status=provenance_status,
        has_explicit_source_spec_id=has_explicit,
        has_validated_canonical_inv_spec=has_canonical,
        source_path=source_path,
    )


def test_canonical_inv_spec_beats_raw_pass3_derived_duplicate():
    canonical = _cand(
        package_id="pkg_zzz_canonical",
        provenance_status="SOURCE_DOCUMENT_DERIVED",
        has_canonical=True,
        source_path="zzz/path.yaml",
    )
    pass3 = _cand(
        package_id="pkg_aaa_pass3",
        provenance_status="BLOCKED",
        has_canonical=False,
        source_path="aaa/path.yaml",
    )
    assert resolve_duplicate_authority(pass3, canonical) is canonical
    assert resolve_duplicate_authority(canonical, pass3) is canonical


def test_higher_provenance_rank_beats_unratified_duplicate():
    explicit = _cand(
        package_id="pkg_b",
        provenance_status="EXPLICIT_SPEC",
        has_canonical=True,
        has_explicit=True,
    )
    inferred = _cand(
        package_id="pkg_a",
        provenance_status="LEGACY_INFERRED",
        has_canonical=True,
        has_explicit=False,
    )
    assert resolve_duplicate_authority(inferred, explicit) is explicit


def test_explicit_source_spec_id_beats_inferred_identity():
    explicit = _cand(
        package_id="pkg_later",
        provenance_status="SOURCE_DOCUMENT_DERIVED",
        has_explicit=True,
        has_canonical=True,
    )
    inferred = _cand(
        package_id="pkg_earlier",
        provenance_status="SOURCE_DOCUMENT_DERIVED",
        has_explicit=False,
        has_canonical=True,
    )
    assert resolve_duplicate_authority(inferred, explicit) is explicit
    assert resolve_duplicate_authority(explicit, inferred) is explicit


def test_equal_authority_unresolved_duplicates_fail_closed():
    left = _cand(package_id="pkg_a", provenance_status="SOURCE_DOCUMENT_DERIVED", has_canonical=True)
    right = _cand(package_id="pkg_b", provenance_status="SOURCE_DOCUMENT_DERIVED", has_canonical=True)
    with pytest.raises(DuplicateAuthorityConflict, match="equal governed authority"):
        resolve_duplicate_authority(left, right)


def test_package_names_and_source_paths_do_not_affect_winner():
    better = _cand(
        package_id="pkg_zzz",
        provenance_status="EXPLICIT_SPEC",
        has_explicit=True,
        has_canonical=True,
        source_path="zzz/late.yaml",
    )
    worse = _cand(
        package_id="pkg_aaa",
        provenance_status="BLOCKED",
        has_explicit=False,
        has_canonical=False,
        source_path="aaa/early.yaml",
    )
    assert resolve_duplicate_authority(worse, better).package_id == "pkg_zzz"
    assert resolve_duplicate_authority(better, worse).package_id == "pkg_zzz"


def test_load_order_does_not_affect_winner():
    winner = _cand(
        package_id="pkg_second",
        provenance_status="EXPLICIT_SPEC",
        has_explicit=True,
        has_canonical=True,
    )
    loser = _cand(
        package_id="pkg_first",
        provenance_status="LEGACY_INFERRED",
        has_explicit=False,
        has_canonical=False,
    )
    assert resolve_duplicate_authority(loser, winner) is winner
    assert resolve_duplicate_authority(winner, loser) is winner


def test_no_special_package_map_in_activation_identity_module():
    # Resolve from this test file so the assertion is cwd-independent.
    module_path = (
        Path(__file__).resolve().parents[2]
        / "core"
        / "knowledge"
        / "signal_activation_identity_v1.py"
    )
    text = module_path.read_text(encoding="utf-8")
    assert "_SPECIAL_PACKAGE_SOURCE_SPEC_IDS" not in text
    assert "pkg_kb52c_tsh_high_primary_hypothyroid_pattern" not in text
