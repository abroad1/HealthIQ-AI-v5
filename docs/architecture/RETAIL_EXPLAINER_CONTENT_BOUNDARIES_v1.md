# Retail explainer content boundaries (v1)

**Work:** FE-VISUALISATION-B1A  
**Purpose:** Prevent mixing of unrelated content classes in product and API contracts.

## Content classes (governed)

| Class | Model / JSON key | Meaning |
|--------|------------------|--------|
| **Engine interpretation** | `BiomarkerScore.interpretation` → `interpretation` | Deterministic scoring/lab-mechanics messaging (e.g. “Scored using lab reference range”). **Personalised to the run** only in the sense of reflecting that run’s bounds; **not** retail physiology education. |
| **Biomarker educational explainer** | `BiomarkerEducationalExplainerV1` → `biomarker_educational_explainer` | **Reusable**, **non-personalised** plain-language education for a biomarker id. Sourced from `backend/ssot/retail_explainer_v1/registry.yaml` (population grows in B1B+). Must not state patient-specific conclusions. |
| **System educational explainer** | `SystemEducationalExplainerV1` → `system_educational_explainer` | **Reusable** education keyed to cluster **schema system** (e.g. `metabolic`). Same registry file, `systems:` section. Must read as **general education**, not proof of individual illness. |
| **Contribution context** | `ContributionContextV1` → `contribution_context` | **Bounded factual** linkage: currently **cluster membership** only (`relationship_kind: cluster_membership`). **No** mechanism/causality/symptom inference. |
| **Personalised clinical interpretation** | `clinician_report_v1` | Policy-ranked primary concern, key findings, hypotheses, confidence — **separate contract**. |
| **Symptom relevance** | *deferred* | **Must not** appear in B1A fields. Reserved UI slot only until a future governed sprint. |

## Storage / ownership

- **Primary SSOT file:** `backend/ssot/retail_explainer_v1/registry.yaml`
- **Validation / loading:** `core/ssot/retail_explainer_registry_v1.py`
- **Contracts:** `core/contracts/retail_explainer_v1.py`
- **Runtime attachment:** `core/analytics/retail_explainer_assembly_v1.py` (after cluster DTOs are built)

## FE consumption (later)

- FE-VISUALISATION-B2 **renders** these keys; it **must not** merge them into `interpretation` or `clinician_report_v1` blocks.
- Educational strings are **not** symptom associations and **not** individual medical advice.

## Persistence note

- In-memory / `client_result_shape_v1` JSON may include these fields when produced by the live orchestrator path.
- Relational **per-biomarker row** hydration in `PersistenceService.get_analysis_result` may **omit** optional explainer columns until a storage sprint extends the schema; B1B should align DB blobs or columns with this contract.
