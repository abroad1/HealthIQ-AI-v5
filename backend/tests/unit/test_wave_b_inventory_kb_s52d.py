"""KB-S52D Wave B package inventory must match KB-S52B governance only."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2].parent
GOV_PATH = (
    REPO_ROOT
    / "knowledge_bus"
    / "governance"
    / "translation_contract_v3_to_package_KB-S52B_v1.yaml"
)
PACKAGES_ROOT = REPO_ROOT / "knowledge_bus" / "packages"

_SPEC_FROM_DESC = re.compile(r"for (inv_[a-z0-9_]+)\s*[\(\n]")

# Ratified directory names (canonical non_hdl_cholesterol naming — not spec_id slug cut).
_EXPECTED_WAVE_B_DIRS = frozenset(
    {
        "pkg_kb52d_hba1c_pct_high_chronic_hyperglycemia_diabetes",
        "pkg_kb52d_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency",
        "pkg_kb52d_non_hdl_cholesterol_high_atherogenic_lipoprotein_burden",
        "pkg_kb52d_non_hdl_cholesterol_low_reduced_atherogenic_lipoprotein_pool",
    }
)


def _load_gov() -> dict:
    return yaml.safe_load(GOV_PATH.read_text(encoding="utf-8"))


def _kb52d_dirs():
    return sorted(PACKAGES_ROOT.glob("pkg_kb52d_*"))


def test_kb_s52d_package_dirs_count_matches_wave_b() -> None:
    gov = _load_gov()
    rws = gov["readiness_waves_spec_ids"]
    wave_a = set(rws["wave_a_resolver_clean_no_remap_needed"]["spec_ids"])
    wave_b = {
        e["spec_id"]
        for e in rws["wave_b_remap_only_subset_of_kb_s52b_approved_tokens"]["entries"]
    }
    wave_c = set(rws["wave_c_blocked_prerequisite"]["spec_ids"])

    dirs = _kb52d_dirs()
    assert len(dirs) == 4 == len(wave_b)
    assert {d.name for d in dirs} == _EXPECTED_WAVE_B_DIRS

    non_hdl_dirs = [d for d in dirs if "non_hdl" in d.name]
    assert len(non_hdl_dirs) == 2
    for d in non_hdl_dirs:
        assert "non_hdl_cholesterol" in d.name

    found_specs: set[str] = set()
    kbp_ids: list[str] = []

    for d in dirs:
        manifest_path = d / "package_manifest.yaml"
        sig_path = d / "signal_library.yaml"
        assert manifest_path.is_file(), d
        assert sig_path.is_file(), d
        assert (d / "research_brief.yaml").is_file(), d

        man = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        assert man.get("package_id") == d.name
        assert man.get("behavioural_impact") == "NONE"

        desc = man.get("description") or ""
        m = _SPEC_FROM_DESC.search(desc.replace("\n", " "))
        assert m is not None, f"No spec_id in description: {desc!r}"
        sid = m.group(1)
        found_specs.add(sid)

        lib = yaml.safe_load(sig_path.read_text(encoding="utf-8"))
        kbp = lib["library"]["package_id"]
        assert kbp.startswith("KBP-")
        kbp_ids.append(kbp)

    assert found_specs == wave_b
    assert not found_specs & wave_a
    assert not found_specs & wave_c

    nums = sorted(int(x.split("-")[1]) for x in kbp_ids)
    assert nums == list(range(4787, 4791))
