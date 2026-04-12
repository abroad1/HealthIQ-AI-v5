"""Bounded tests for BE-W1-PR3 audit: primary reference bounds vs footnote / LLM fields."""

import json

import pytest

from services.parsing.llm_parser import LLMParser


def _parse_json_response(payload: dict) -> str:
    return json.dumps(payload)


def test_primary_reference_wins_over_footnote_text_for_bounds():
    """Footnote must not override main row threshold when primary line parses."""
    p = LLMParser()
    # Main row: upper bound only; footnote contains a different inequality that must not win first pass.
    text = _parse_json_response(
        {
            "biomarkers": [
                {
                    "id": "prolactin",
                    "name": "Prolactin",
                    "value": 12.0,
                    "unit": "mIU/L",
                    "reference": "< 25",
                    "raw_reference_text": "> 0.5\nSee pregnancy table",
                    "confidence": 0.9,
                }
            ]
        }
    )
    r = p._parse_gemini_response(text)
    assert len(r.biomarkers) == 1
    b = r.biomarkers[0]
    assert b.ref_low is None
    assert b.ref_high == pytest.approx(25.0)


def test_llm_ref_low_ref_high_used_when_primary_line_has_no_bounds():
    """When primary reference string yields no limits, trust explicit ref_low/ref_high from JSON."""
    p = LLMParser()
    text = _parse_json_response(
        {
            "biomarkers": [
                {
                    "id": "x",
                    "name": "X",
                    "value": 5.0,
                    "unit": "U/L",
                    "reference": "See laboratory manual",
                    "raw_reference_text": "",
                    "confidence": 0.8,
                    "ref_low": 2.0,
                    "ref_high": 10.0,
                }
            ]
        }
    )
    r = p._parse_gemini_response(text)
    b = r.biomarkers[0]
    assert b.ref_low == pytest.approx(2.0)
    assert b.ref_high == pytest.approx(10.0)


def test_combined_scan_last_resort_when_no_primary_and_no_llm_bounds():
    """If primary is empty and LLM omits ref_low/ref_high, combined text may still yield bounds."""
    p = LLMParser()
    text = _parse_json_response(
        {
            "biomarkers": [
                {
                    "id": "y",
                    "name": "Y",
                    "value": 100.0,
                    "unit": "mg/dL",
                    "reference": "",
                    "raw_reference_text": "Adult: 70-100",
                    "confidence": 0.85,
                }
            ]
        }
    )
    r = p._parse_gemini_response(text)
    b = r.biomarkers[0]
    assert b.ref_low == pytest.approx(70.0)
    assert b.ref_high == pytest.approx(100.0)


def test_multiple_context_range_options_clear_top_level_bounds():
    """When two or more contextual bands are present, ref_low/ref_high must not be guessed."""
    p = LLMParser()
    text = _parse_json_response(
        {
            "biomarkers": [
                {
                    "id": "prolactin",
                    "name": "Prolactin",
                    "value": 12.0,
                    "unit": "mIU/L",
                    "reference": "See table",
                    "raw_reference_text": "Males: 2–18\nFemales: 2–29",
                    "confidence": 0.9,
                    "context_range_options": [
                        {
                            "context_label": "Male",
                            "min": 2.0,
                            "max": 18.0,
                            "unit": "mIU/L",
                            "source_snippet": "Males: 2–18",
                        },
                        {
                            "context_label": "Female",
                            "min": 2.0,
                            "max": 29.0,
                            "unit": "mIU/L",
                            "source_snippet": "Females: 2–29",
                        },
                    ],
                }
            ]
        }
    )
    r = p._parse_gemini_response(text)
    b = r.biomarkers[0]
    assert b.ref_low is None
    assert b.ref_high is None
    assert b.status == "Unknown"
    assert len(b.context_range_options) == 2
    assert b.context_range_options[0].context_label == "Male"


def test_single_context_range_option_populates_bounds():
    """One contextual option uses its bounds when present."""
    p = LLMParser()
    text = _parse_json_response(
        {
            "biomarkers": [
                {
                    "id": "x",
                    "name": "X",
                    "value": 10.0,
                    "unit": "U/L",
                    "reference": "Adult",
                    "raw_reference_text": "",
                    "confidence": 0.85,
                    "ref_low": None,
                    "ref_high": None,
                    "context_range_options": [
                        {
                            "context_label": "Adult",
                            "min": 5.0,
                            "max": 40.0,
                            "unit": "U/L",
                            "source_snippet": "5–40",
                        }
                    ],
                }
            ]
        }
    )
    r = p._parse_gemini_response(text)
    b = r.biomarkers[0]
    assert b.ref_low == pytest.approx(5.0)
    assert b.ref_high == pytest.approx(40.0)
    assert len(b.context_range_options) == 1
