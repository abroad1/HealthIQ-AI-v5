"""
Unit tests for lab origin detection (Sprint 2).

Deterministic only. Lab marker strings kept short and realistic.
"""

import pytest
from core.lab.detector import detect_lab_origin
from core.models.lab_origin import LabOrigin, lab_origin_unknown


# Lab marker strings used in tests (short, realistic)
MEDICHECKS_HEADER = "MediChecks\nYour blood test results\n---"
RANDOX_HEADER = "Randox Health\nLaboratory Report"
LML_HEADER = "London Medical Laboratory\nBiomarker Results"
UNKNOWN_HEADER = "Some Generic Lab\nResults"

# NHS hardened markers (structured only; no bare "NHS")
NHS_FOUNDATION_TRUST = "NHS Foundation Trust – Pathology Services"
NHS_DEPT_PATHOLOGY = "Department of Pathology – NHS Trust"
NHS_CLINICAL_BIOCHEM = "Clinical Biochemistry – NHS Foundation Trust"


class TestDetectLabOrigin:
    """Tests for detect_lab_origin."""

    def test_medichecks_header(self):
        """Header containing 'MediChecks' returns medichecks."""
        lo = detect_lab_origin(text=MEDICHECKS_HEADER, filename=None)
        assert lo.lab_provider_id == "medichecks"
        assert lo.lab_provider_name == "MediChecks"
        assert lo.detection_method == "header_regex"
        assert lo.detection_confidence == 0.9
        assert "MediChecks" in (lo.raw_evidence or "")

    def test_randox_header(self):
        """Header containing 'Randox' returns randox."""
        lo = detect_lab_origin(text=RANDOX_HEADER, filename=None)
        assert lo.lab_provider_id == "randox"
        assert lo.lab_provider_name == "Randox"
        assert lo.detection_method == "header_regex"
        assert lo.detection_confidence == 0.9

    def test_nhs_foundation_trust_pathology_services(self):
        """Header with 'NHS Foundation Trust – Pathology Services' detects nhs_generic."""
        lo = detect_lab_origin(text=NHS_FOUNDATION_TRUST, filename=None)
        assert lo.lab_provider_id == "nhs_generic"
        assert lo.detection_method == "header_regex"
        assert lo.detection_confidence == 0.9

    def test_nhs_department_of_pathology_trust(self):
        """Header with 'Department of Pathology – NHS Trust' detects nhs_generic."""
        lo = detect_lab_origin(text=NHS_DEPT_PATHOLOGY, filename=None)
        assert lo.lab_provider_id == "nhs_generic"
        assert lo.detection_method == "header_regex"

    def test_nhs_clinical_biochemistry_foundation_trust(self):
        """Header with 'Clinical Biochemistry – NHS Foundation Trust' detects nhs_generic."""
        lo = detect_lab_origin(text=NHS_CLINICAL_BIOCHEM, filename=None)
        assert lo.lab_provider_id == "nhs_generic"
        assert lo.detection_method == "header_regex"

    def test_nhs_false_positive_blood_test_results(self):
        """'NHS Blood Test Results' must NOT detect (bare NHS context)."""
        lo = detect_lab_origin(text="NHS Blood Test Results", filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_confidence == 0.0

    def test_nhs_false_positive_app_export(self):
        """'NHS App Export' must NOT detect."""
        lo = detect_lab_origin(text="NHS App Export", filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_confidence == 0.0

    def test_nhs_false_positive_my_nhs_login(self):
        """'My NHS Login Summary' must NOT detect."""
        lo = detect_lab_origin(text="My NHS Login Summary", filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_confidence == 0.0

    def test_nhs_false_positive_national_health_survey(self):
        """'National Health Survey' must NOT detect."""
        lo = detect_lab_origin(text="National Health Survey", filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_confidence == 0.0

    def test_london_medical_laboratory_header(self):
        """Header containing 'London Medical Laboratory' returns london_medical_laboratory."""
        lo = detect_lab_origin(text=LML_HEADER, filename=None)
        assert lo.lab_provider_id == "london_medical_laboratory"
        assert lo.lab_provider_name == "London Medical Laboratory"
        assert lo.detection_method == "header_regex"

    def test_unknown_when_no_match(self):
        """No known marker returns unknown."""
        lo = detect_lab_origin(text=UNKNOWN_HEADER, filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_method == "unknown"
        assert lo.detection_confidence == 0.0

    def test_unknown_when_empty(self):
        """Empty text and no filename returns unknown."""
        lo = detect_lab_origin(text=None, filename=None)
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_method == "unknown"

    def test_filename_medichecks(self):
        """Filename containing 'medicheck' returns medichecks via filename detection."""
        lo = detect_lab_origin(text=None, filename="medichecks_blood_test_2024.pdf")
        assert lo.lab_provider_id == "medichecks"
        assert lo.detection_method == "filename"
        assert lo.detection_confidence == 0.4

    def test_filename_randox(self):
        """Filename containing 'randox' returns randox via filename detection."""
        lo = detect_lab_origin(text=None, filename="randox_discovery_results.pdf")
        assert lo.lab_provider_id == "randox"
        assert lo.detection_method == "filename"
        assert lo.detection_confidence == 0.4

    def test_filename_nhs_bare_rejected(self):
        """Filename with bare 'nhs' must NOT detect (false-positive hardening)."""
        lo = detect_lab_origin(text=None, filename="nhs_lab_report.txt")
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_confidence == 0.0

    def test_filename_nhs_pathology_detects(self):
        """Filename with 'NHS Pathology' or 'Pathology Services' detects nhs_generic."""
        lo = detect_lab_origin(text=None, filename="NHS Pathology Report 2024.pdf")
        assert lo.lab_provider_id == "nhs_generic"
        assert lo.detection_method == "filename"

    def test_text_takes_precedence_over_filename(self):
        """When both text and filename match, header match wins (higher confidence)."""
        lo = detect_lab_origin(
            text=MEDICHECKS_HEADER,
            filename="randox_report.pdf",
        )
        assert lo.lab_provider_id == "medichecks"
        assert lo.detection_method == "header_regex"
        assert lo.detection_confidence == 0.9

    def test_medichecks_case_insensitive(self):
        """MediChecks match is case-insensitive."""
        lo = detect_lab_origin(text="medichecks report", filename=None)
        assert lo.lab_provider_id == "medichecks"


class TestLabOriginModel:
    """Tests for LabOrigin model."""

    def test_to_dict(self):
        """LabOrigin serialises to dict for API."""
        lo = LabOrigin(
            lab_provider_id="medichecks",
            lab_provider_name="MediChecks",
            detection_method="header_regex",
            detection_confidence=0.9,
            raw_evidence="MediChecks",
        )
        d = lo.to_dict()
        assert d["lab_provider_id"] == "medichecks"
        assert d["lab_provider_name"] == "MediChecks"
        assert d["detection_method"] == "header_regex"
        assert d["detection_confidence"] == 0.9
        assert d["raw_evidence"] == "MediChecks"

    def test_lab_origin_unknown(self):
        """lab_origin_unknown factory returns unknown."""
        lo = lab_origin_unknown()
        assert lo.lab_provider_id == "unknown"
        assert lo.detection_method == "unknown"
        assert lo.detection_confidence == 0.0
