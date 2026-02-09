import pytest

from core.pipeline.orchestrator import AnalysisOrchestrator
from core.canonical.normalize import normalize_biomarkers_with_metadata


class TestOrchestratorUnmappedQuarantine:
    def setup_method(self):
        self.orchestrator = AnalysisOrchestrator()

    def test_unmapped_biomarkers_quarantined_in_run(self):
        raw_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "albumin_(venous)": 44.0,
            "calcium_(venous)": {
                "value": 2.2,
                "unit": "mmol/L",
                "reference_range": {"min": 2.1, "max": 2.6, "unit": "mmol/L", "source": "lab"}
            }
        }
        user_data = {
            "user_id": "test_user",
            "age": 35,
            "gender": "male"
        }

        normalized = normalize_biomarkers_with_metadata(raw_biomarkers)
        dto = self.orchestrator.run(normalized, user_data, assume_canonical=True)

        assert dto is not None
        assert "unmapped_albumin_(venous)" in dto.unmapped_biomarkers

        biomarker_names = []
        for biomarker in dto.biomarkers:
            if hasattr(biomarker, "biomarker_name"):
                biomarker_names.append(biomarker.biomarker_name)
            elif hasattr(biomarker, "name"):
                biomarker_names.append(biomarker.name)
            elif isinstance(biomarker, dict):
                biomarker_names.append(biomarker.get("biomarker_name") or biomarker.get("name"))

        assert all(
            name and not name.startswith("unmapped_")
            for name in biomarker_names
        )

        calcium_entries = [
            b for b in dto.biomarkers
            if getattr(b, "biomarker_name", None) == "calcium"
        ]
        assert calcium_entries, "Expected calcium to remain in DTO biomarkers"
        assert calcium_entries[0].unit == "mmol/L"

