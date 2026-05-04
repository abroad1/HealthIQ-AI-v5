# N-6 — Functional interpretation and confidence assets (implementation note)

## Governed asset location

**`knowledge_bus/functional_interpretation_v1/functional_interpretation_v1.yaml`**

### Preflight rationale

| Existing asset | What it already does | Why it is insufficient for N-6 |
|----------------|----------------------|--------------------------------|
| `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` | Pathway biology and transport architecture | Does not encode **functional reads**, **confidence framing**, **clarification**, or **monitoring** moves |
| Root-cause hypothesis YAML | Evidence / mechanism packaging | Not reusable **interpretive framing** separate from hypothesis identity |
| `idl_records_v1.yaml` | Display labels, short “why it matters” | Too shallow for benchmark-grade interpretive language |
| `confirmatory_tests_v1.yaml` | Test catalog | Points to *what* to order, not *how* to narrate confidence and monitoring |

A **new pack** keeps **authority separation**: pathway explanation ≠ higher-order interpretive framing ≠ display copy.

## Pack structure (compiler-oriented)

Per benchmark domain, v1 provides:

- `functional_reading` — e.g. pathway efficiency vs simple deficiency framing; LDL in full transport context  
- `why_beyond_itself` — vascular / marrow or cumulative exposure framing  
- `confidence_grade_label` — short token (e.g. `moderate_by_default`) for downstream mapping  
- `confidence_supports_reading` / `confidence_limits` — explicit supports vs limits (implements sprint §3 “what supports / what limits”)  
- `clarification_paths` — list of strings for selective compiler use  
- `monitoring_improvement_signals` / `monitoring_persistence_signals` — trajectory language without alarmism  

`related_pathway_explainer_id` links to N-5 pathway rows **by reference only** (no duplication of pathway prose).

## Domains in v1

1. `one_carbon_methylation_functional_v1`  
2. `lipid_transport_functional_v1`

## Validation

- `backend/tests/unit/test_functional_interpretation_v1.py`  
- Wired into `backend/scripts/run_baseline_tests.py` (golden gate baseline).

## What this unblocks

- **N-8 / narrative compiler** implementation can load interpretive slices by `domain_id` without conflating them with pathway explainers or IDL strings.

## Limits

- No runtime wiring in this sprint; consumption is **file-based** until the compiler loads the pack.  
- `confidence_grade_label` is a **governed hint**, not a scored output from the analytics core.
