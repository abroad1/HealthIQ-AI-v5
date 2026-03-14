from pathlib import Path

from tools.run_golden_panel import run_golden_panel

# reference_profile.effective_from is the lab reference range effective-from date (i.e., when the lab's reference ranges changed). It is NOT the test/sample/report date. Test/sample/report dates are panel-level metadata.
#
# Canonical ID mapping used:
# TgAb (Venous) -> tgab
# Oestradiol (Venous) -> oestradiol
# Folate (Venous) -> folate
# Prolactin (Venous) -> prolactin


def _rows_by_name(analysis_result: dict) -> dict:
    out = {}
    for row in analysis_result.get("biomarkers", []):
        if isinstance(row, dict) and row.get("biomarker_name"):
            out[str(row["biomarker_name"])] = row
    return out


def test_lab_reference_profile_micro_pass_through_and_band_labels(tmp_path):
    fixture = (
        Path(__file__).parent.parent
        / "fixtures"
        / "panels"
        / "lab_reference_profile_micro.json"
    )
    _, analysis_result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-lab-reference-profile-micro",
        write_narrative=False,
    )
    rows = _rows_by_name(analysis_result if isinstance(analysis_result, dict) else {})

    expected = {
        "tgab": {
            "label": "Negative",
            "effective_from": None,
            "note": None,
            "band_count": 2,
        },
        "oestradiol": {
            "label": "Males",
            "effective_from": "2024-08-27",
            "note": "Please note new reference ranges commencing 27/08/2024",
            "band_count": 1,
        },
        "folate": {
            "label": "Normal",
            "effective_from": None,
            "note": None,
            "band_count": 3,
        },
        "prolactin": {
            "label": "Males",
            "effective_from": "2024-09-11",
            "note": "Please note reference range and unit change commencing 11/09/2024",
            "band_count": 1,
        },
    }

    for biomarker_id, cfg in expected.items():
        row = rows.get(biomarker_id)
        assert isinstance(row, dict), f"Missing row for {biomarker_id}"

        profile = row.get("reference_profile")
        assert isinstance(profile, dict), f"Missing reference_profile for {biomarker_id}"
        assert profile.get("source") == "lab"
        assert isinstance(profile.get("bands"), list)
        assert len(profile["bands"]) == cfg["band_count"]

        if cfg["effective_from"] is None:
            assert profile.get("effective_from") is None
        else:
            assert profile.get("effective_from") == cfg["effective_from"]

        if cfg["note"] is None:
            assert profile.get("note") is None
        else:
            assert profile.get("note") == cfg["note"]

        assert row.get("lab_band_label") == cfg["label"]
        assert row.get("lab_band_label") is not None

        # Guard against regressions where ranges disappear while profiles exist.
        assert isinstance(row.get("reference_range"), dict)
        assert row.get("range_source") == "lab"
