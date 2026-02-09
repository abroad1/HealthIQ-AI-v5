import pytest

from core.pipeline.orchestrator import AnalysisOrchestrator


class TestOrchestratorUnmappedQuarantine:
    def setup_method(self):
        self.orchestrator = AnalysisOrchestrator()

    def test_unmapped_biomarkers_quarantined_in_run(self):
        raw_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "unmapped_albumin_(venous)": 3.8,
            "unmapped_free_t4_(venous)": 1.1
        }
        user_data = {
            "user_id": "test_user",
            "age": 35,
            "gender": "male"
        }

        dto = self.orchestrator.run(raw_biomarkers, user_data, assume_canonical=True)

        assert dto is not None
        assert sorted(dto.unmapped_biomarkers) == [
            "unmapped_albumin_(venous)",
            "unmapped_free_t4_(venous)"
        ]

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

    def test_alias_resolution_quarantine_for_specimen_suffixes(self):
        raw_biomarkers = {
            "albumin_(venous)": {"value": 44.0, "unit": "g/L"},
            "calcium_(venous)": {"value": 2.2, "unit": "mmol/L"},
        }
        user_data = {
            "user_id": "test_user",
            "age": 35,
            "gender": "male"
        }

        dto = self.orchestrator.run(raw_biomarkers, user_data, assume_canonical=True)

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
            name != "albumin_(venous)" for name in biomarker_names
        )

        calcium_entries = [
            biomarker for biomarker in dto.biomarkers
            if getattr(biomarker, "biomarker_name", None) == "calcium"
            or (isinstance(biomarker, dict) and biomarker.get("biomarker_name") == "calcium")
        ]
        assert calcium_entries, "Expected calcium biomarker to be present in DTO"
        calcium_entry = calcium_entries[0]
        if isinstance(calcium_entry, dict):
            assert calcium_entry.get("value") == 2.2
            assert calcium_entry.get("unit") == "mmol/L"
        else:
            assert calcium_entry.value == 2.2
            assert calcium_entry.unit == "mmol/L"

