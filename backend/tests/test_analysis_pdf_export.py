"""Smoke test for Sprint 4 PDF summary builder (no Intelligence Core)."""

from core.dto.builders import build_analysis_result_dto
from tests.fixtures.sample_analysis import SAMPLE_ANALYSIS

from app.analysis_pdf_export import build_summary_pdf_bytes


def test_build_summary_pdf_bytes_starts_with_pdf_header():
    raw = dict(SAMPLE_ANALYSIS)
    raw["meta"] = raw.get("meta") or {}
    dto = build_analysis_result_dto(raw)
    out = build_summary_pdf_bytes(dto, user_display="test@example.com")
    assert out[:4] == b"%PDF"
    assert len(out) > 500
    # Disclaimer is drawn in the PDF (may be compressed; do not assert raw substrings).
