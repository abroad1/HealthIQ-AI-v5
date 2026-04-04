# KB-S57 — CBC expansion tranche blocker report (Outcome B)

**work_id:** KB-S57  
**Date:** 2026-04-01  
**Mode:** Read-only assessment — **no packages created** (per hardened sprint authority).

## Outcome

**Outcome B — bounded blocker.** Governed **investigation_spec_contract_version 3.0.0** Pass 3 artifacts (`knowledge_bus/research/investigation_specs/multi_llm_research/Batch_*_Pass_3.json`) contain **no** `inv_*` specs whose **primary** `primary_marker.biomarker_id` matches any of the nine in-scope CBC canonical IDs. Ingestion into current KB packages therefore **cannot proceed** without a **new 3-pass research batch** producing v3.0.0-compliant specs.

**Preflight note:** `knowledge_bus/research/KB-S54_COVERAGE_AND_ARCHIVE_POSITION.md` is **not present** in this repository; commercial baseline for this assessment uses **`knowledge_bus/research/KB-S55_COMMERCIAL_COVERAGE_GAP_RESOLUTION.md`** only.

## Canonical ID confirmation (SSOT)

The following IDs are present in `backend/ssot/biomarkers.yaml` and are the approved tranche targets. **No SSOT edits** were made.

| Canonical ID | SSOT alignment |
|----------------|----------------|
| `mch` | Confirmed |
| `mchc` | Confirmed |
| `rdw_cv` | Confirmed |
| `rdw_sd` | Confirmed |
| `monocyte_pct` | Confirmed |
| `monocytes_abs` | Confirmed |
| `mpv` | Confirmed |
| `pdw` | Confirmed |
| `neutrophil_pct` | Confirmed |

## Governed v3.0.0 source search (Batches 3–7 Pass 3)

Recursive search of `Batch_3_Pass_3.json` through `Batch_7_Pass_3.json` for **primary** markers matching the nine IDs above returned **no** matching `inv_*` investigation specs.

**Adjacency only (not a primary CBC tranche spec):** `Batch_6_Pass_3.json` references `rbc_count` as a **supporting** / hypothesis marker in an unrelated spec — **not** a primary `rbc` or CBC-index spec, and **`rbc_count` must not** be used as canonical `biomarker_id` per sprint rules. No governed v3.0.0 primary spec exists for **`rbc`**; optional inclusion is **not** supported by preflight evidence.

## Required inventory (per sprint prompt)

| biomarker_id | governed_v3_spec_exists | source_file | spec_id | signal_id | can_package_proceed |
|--------------|-------------------------|-------------|---------|-----------|---------------------|
| `mch` | **No** | — | — | — | **No** |
| `mchc` | **No** | — | — | — | **No** |
| `rdw_cv` | **No** | — | — | — | **No** |
| `rdw_sd` | **No** | — | — | — | **No** |
| `monocyte_pct` | **No** | — | — | — | **No** |
| `monocytes_abs` | **No** | — | — | — | **No** |
| `mpv` | **No** | — | — | — | **No** |
| `pdw` | **No** | — | — | — | **No** |
| `neutrophil_pct` | **No** | — | — | — | **No** |

**Optional target `rbc` (documentation only):** no governed v3.0.0 **primary** spec exists; **not** an actionable ingestion item in this sprint.

## New `pkg_kb*` estate

No `knowledge_bus/packages/pkg_kb*` packages exist today for these primary markers (confirmed by package-name search). No new packages were added under KB-S57.

## Pre-v3.0.0 context pointers (ineligible as ingestion sources)

The following **legacy collection JSON** files contain older-format specs that **do not** declare `investigation_spec_contract_version: 3.0.0` and **do not** include the required v3 root fields (e.g. `hypotheses`, `hypothesis_ranking`, `confirmatory_tests`, `evidence` block as required by v3). Per `investigation_spec_schema_v3.0.0.yaml`, **v2.x artifacts without contract version remain v2-governed** and are **not** eligible as source artifacts for KB package creation under the current KB package contracts.

**They are listed only as historical pointers for a future research batch — not for direct ingestion:**

| File path | spec_id | signal_id | primary_marker (canonical) |
|-----------|---------|-----------|----------------------------|
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_mch_low` | `signal_hypochromic_erythropoiesis` | `mch` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_mchc_low` | `signal_reduced_hemoglobin_concentration` | `mchc` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_monocyte_pct_high` | `signal_relative_monocytosis` | `monocyte_pct` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_monocytes_abs_high` | `signal_absolute_monocytosis` | `monocytes_abs` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_mpv_high` | `signal_increased_platelet_turnover` | `mpv` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_neutrophil_pct_high` | `signal_relative_neutrophilia` | `neutrophil_pct` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch31-40.json` | `inv_pdw_high` | `signal_platelet_size_variability` | `pdw` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch41-50.json` | `inv_rdw_cv_high` | `signal_anisocytosis_cv` | `rdw_cv` |
| `knowledge_bus/research/investigation_specs/investigation-spec-collection-batch41-50.json` | `inv_rdw_sd_high` | `signal_anisocytosis_sd` | `rdw_sd` |

Promoting these without a **governed 3-pass re-research** pass would require **schema / contract** work outside this sprint scope.

## Next required step

**A new 3-pass research batch** must produce **v3.0.0-compliant** `inv_*` specs in `multi_llm_research/Batch_*_Pass_3.json` (or successor governed path) covering **all nine** canonical CBC targets above **before** KB-S57-style ingestion can execute **Outcome A**.

No medical research content was drafted or invented in this report.
