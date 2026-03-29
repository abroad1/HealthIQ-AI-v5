"""KB-S52C: Wave A package inventory must match KB-S52B governance only."""

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


def _load_gov() -> dict:
    return yaml.safe_load(GOV_PATH.read_text(encoding="utf-8"))


def _kb52c_dirs():
    return sorted(PACKAGES_ROOT.glob("pkg_kb52c_*"))


def test_kb_s52c_package_dirs_count_matches_wave_a() -> None:
    gov = _load_gov()
    wave_a = set(
        gov["readiness_waves_spec_ids"]["wave_a_resolver_clean_no_remap_needed"]["spec_ids"]
    )
    wave_b = {
        e["spec_id"]
        for e in gov["readiness_waves_spec_ids"][
            "wave_b_remap_only_subset_of_kb_s52b_approved_tokens"
        ]["entries"]
    }
    wave_c = set(gov["readiness_waves_spec_ids"]["wave_c_blocked_prerequisite"]["spec_ids"])

    dirs = _kb52c_dirs()
    assert len(dirs) == 67 == len(wave_a)

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

        expected_slug = sid[4:] if sid.startswith("inv_") else sid
        assert d.name == f"pkg_kb52c_{expected_slug}", f"{d.name} vs {sid}"

        lib = yaml.safe_load(sig_path.read_text(encoding="utf-8"))
        kbp = lib["library"]["package_id"]
        assert kbp.startswith("KBP-")
        kbp_ids.append(kbp)

    assert found_specs == wave_a
    assert not found_specs & wave_b
    assert not found_specs & wave_c

    nums = sorted(int(x.split("-")[1]) for x in kbp_ids)
    assert nums == list(range(4720, 4787))
