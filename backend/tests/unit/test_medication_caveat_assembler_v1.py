"""MEDICATION-CAVEAT-B — deterministic medication/supplement interpretation caveat."""

from core.analytics.medication_caveat_assembler_v1 import (
    build_medication_supplement_interpretation_caveat,
)


def test_no_medical_history_returns_none():
    assert build_medication_supplement_interpretation_caveat(None) is None
    assert build_medication_supplement_interpretation_caveat({}) is None


def test_none_only_meds_supplements_no_flags_returns_none():
    mh = {
        "medications": ["None"],
        "supplements": ["None"],
        "long_term_medication_classes": ["None"],
    }
    assert build_medication_supplement_interpretation_caveat(mh) is None


def test_coarse_medication_band_emits_caveat():
    mh = {"medications": ["3-5 medications"], "supplements": ["None"]}
    out = build_medication_supplement_interpretation_caveat(mh)
    assert out is not None
    assert "coarse" in out.lower() or "category" in out.lower()


def test_supplement_other_does_not_echo_free_text():
    mh = {"medications": ["None"], "supplements": ["Vitamin D", "Other", "Fish oil custom brand"]}
    out = build_medication_supplement_interpretation_caveat(mh)
    assert out is not None
    assert "Fish oil custom brand" not in out
    assert "non-catalogued" in out.lower() or "free-text" in out.lower()


def test_long_term_classes_sorted_determinism():
    mh = {
        "medications": ["None"],
        "long_term_medication_classes": ["HIV/AIDS treatments", "Corticosteroids"],
    }
    a = build_medication_supplement_interpretation_caveat(mh)
    b = build_medication_supplement_interpretation_caveat(mh)
    assert a == b
    assert "Corticosteroids" in (a or "")
    assert "HIV/AIDS treatments" in (a or "")


def test_qrisk_flags_add_clause():
    mh = {"medications": ["None"], "corticosteroids": True}
    out = build_medication_supplement_interpretation_caveat(mh)
    assert out is not None
    assert "Questionnaire flags" in out
