from pathlib import Path

import yaml

from core.units.registry import convert_value


def _umol_base_biomarkers() -> list[str]:
    ssot = Path(__file__).resolve().parents[2] / "ssot" / "biomarkers.yaml"
    payload = yaml.safe_load(ssot.read_text(encoding="utf-8")) or {}
    biomarkers = payload.get("biomarkers", {}) if isinstance(payload, dict) else {}
    out = [str(bid) for bid, meta in biomarkers.items() if isinstance(meta, dict) and str(meta.get("unit", "")).strip() == "µmol/L"]
    return sorted(out)


def test_umol_aliases_resolve_for_all_umol_base_biomarkers():
    biomarker_ids = _umol_base_biomarkers()
    assert biomarker_ids, "Expected at least one biomarker with base unit µmol/L in SSOT"

    for biomarker_id in biomarker_ids:
        value = 1.234
        val_umol, unit_umol = convert_value(biomarker_id, value, "umol/L")
        val_micro, unit_micro = convert_value(biomarker_id, value, "µmol/L")
        val_case, unit_case = convert_value(biomarker_id, value, "uMol/L")

        assert unit_umol == "µmol/L", f"{biomarker_id}: expected canonical unit µmol/L for umol/L input"
        assert unit_micro == "µmol/L", f"{biomarker_id}: expected canonical unit µmol/L for µmol/L input"
        assert unit_case == "µmol/L", f"{biomarker_id}: expected canonical unit µmol/L for uMol/L input"
        assert val_umol == val_micro, f"{biomarker_id}: umol/L and µmol/L should normalize identically"
        assert val_case == val_micro, f"{biomarker_id}: uMol/L and µmol/L should normalize identically"
