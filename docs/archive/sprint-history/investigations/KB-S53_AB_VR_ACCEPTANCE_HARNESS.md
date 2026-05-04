# KB-S53 — AB/VR acceptance harness (governed)

**work_id:** `KB-S53-ABVR-HARNESS` (strategic Wave 3 KB-S53 — AB/VR formalisation)  
**Machine authority:** `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml`  
**Import surface (tests):** `backend/tests/support/panel_acceptance.py`  
**Bounded runner:** `backend/scripts/run_ab_vr_acceptance_harness.py`  

---

## Naming disambiguation (mandatory)

| Label | Meaning |
|-------|---------|
| **Strategic KB-S53 (this harness)** | AB/VR panel formalisation + acceptance objects. |
| **`KB-S53_WAVE_C_CLASSIFICATION_AUDIT.md`** | **Different** work — Wave C ingestion classification. **Out of scope** for this harness; do not merge authority or scope. |

---

## What AB and VR are (authoritative fixtures)

| Profile (manifest `profile_id`) | Authoritative file | Role |
|----------------------------------|-------------------|------|
| `ab_acceptance` | `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` | **AB acceptance harness** — lab-shaped biomarkers with `reference_range`. |
| `vr_acceptance` | `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json` | **VR acceptance harness** — same harness class as AB. |

**Not** authoritative for acceptance:

- `ab_full_panel.json`, `vr_full_panel.json` — minimal / legacy-shaped siblings (see manifest `legacy_minimal`).
- `ab_full_panel_with_profiles.json` — lab reference **profile** variant for specific regression tests only (`ab_lab_reference_profile_variant`).

---

## Relationship to `golden_panel_160.json`

- **Default** `run_golden_panel` fixture and **`verify_three_layer_pipeline`** / **`golden_gate_local`** baseline path: `backend/tests/fixtures/golden_panel_160.json` (manifest profile `golden_panel_160`).
- **AB/VR** are **additional** acceptance harnesses (commercial floor), **not** a replacement for the gate anchor.
- Release semantics: the **control-plane gate is unchanged** by KB-S53; operators should run **`run_ab_vr_acceptance_harness.py`** when validating AB/VR explicitly (see script docstring).

---

## What AB/VR are intended to prove

- **Deterministic** full-panel runs with lab ranges produce **stable** structured outputs for regression (insight graph slices, `report_v1`, root-cause homocysteine context, interaction-chain smoke).
- **Clinician report v1** contract: valid compilation from runtime output; VR output **fully** matches expected JSON fixture; AB subset checks on header/disclaimer alignment.
- **Confirmatory-test suppression** behaviour on AB where applicable (root-cause tests).

## What AB/VR are **not** intended to prove

- Full **SSOT** or **signal-package** coverage for every domain (hepatic/thyroid WHY waves, Wave C ingestion, etc.).
- **Cluster/scoring coherence** (KB-S54).
- **Interaction-map completeness** — separate gap reports may apply.
- They are **floor harnesses**, not the full product ontology (adopted plan §7.6).

---

## Owning tests / harnesses (authoritative)

| Area | Module | Notes |
|------|--------|--------|
| Clinician report + DTO | `backend/tests/unit/test_clinician_report_runtime_alignment.py` | Uses manifest-backed paths for AB/VR. |
| Golden runner `report_v1` + interaction chains | `backend/tests/unit/test_golden_panel_runner.py` | Parametrized AB/VR acceptance filenames from manifest. |
| Root-cause homocysteine + suppression | `backend/tests/unit/test_root_cause_v1_homocysteine.py` | Parametrized acceptance paths; AB-only cases use AB acceptance path. |
| Lab reference profile variant | `backend/tests/unit/test_golden_panel_runner.py` (`test_ab_profile_fixture_pass_through_and_hba1c_band_label`) | Uses `ab_lab_reference_profile_fixture_path()`. |

Expected JSON fixtures (do not casually edit):

- `backend/tests/fixtures/reports/clinician_report_v1_ab.json`
- `backend/tests/fixtures/reports/clinician_report_v1_vr.json` — **full** golden snapshot for VR; **regenerated 2026-04-04** under `KB-S53-ABVR-HARNESS` to match current deterministic `compile_clinician_report_v1` output (VR **panel** JSON unchanged; acceptance snapshot only).

---

## Operator acceptance — VR clinician fixture regeneration (gate / audit basis)

**Recorded:** 2026-04-04  
**work_id:** `KB-S53-ABVR-HARNESS`  

**Decision:** Operator **explicitly accepts** the regenerated `backend/tests/fixtures/reports/clinician_report_v1_vr.json` as **stale fixture correction**, not a KB-S53 implementation defect.

**Basis (authoritative for merge/gate conversations):**

- VR clinician output matches **existing** deterministic ranking in `compile_report_v1` (`report_compiler_v1.py`): sort by state rank, then confidence, then **ascending `signal_id`** tie-break.
- On the VR acceptance panel, `signal_alp_low` and `signal_homocysteine_elevation_context` tie on state and confidence; **`signal_alp_low` sorts first lexicographically** — see `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`.
- KB-S53 **did not** change pipeline / ranking code.
- **No** ranking-policy sprint opened under this acceptance; clinical reordering of ties, if desired, is **out of scope** here.

**Related artefacts:** `docs/investigations/KB-S53_VR_FIXTURE_OPERATOR_REVIEW.md` (review pack), `VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md` (technical trace).

---

## How to run AB/VR acceptance

From repo root:

```powershell
python backend/scripts/run_ab_vr_acceptance_harness.py
```

Requires standard gate / baseline still run separately (`golden_gate_local` / `run_baseline_tests` / `verify_three_layer_pipeline` as today).

---

## Cold-operator checklist

1. **What is AB?** — Acceptance profile `ab_acceptance` → `ab_full_panel_with_ranges.json` (manifest).  
2. **What is VR?** — Acceptance profile `vr_acceptance` → `vr_full_panel_with_ranges.json`.  
3. **Which file is authoritative?** — See `panel_acceptance_profiles_v1.yaml` (`authoritative_for_acceptance: true`).  
4. **Which tests own them?** — Table above + runner script node list.  
5. **How does this relate to `golden_panel_160`?** — Default gate/runner anchor remains `golden_panel_160`; AB/VR are **additional** harnesses.
