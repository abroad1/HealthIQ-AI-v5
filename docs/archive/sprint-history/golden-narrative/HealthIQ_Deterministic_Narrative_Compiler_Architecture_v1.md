# HealthIQ AI — Deterministic Narrative Compiler Architecture v1

## 1. Purpose
This document defines the recommended architecture for HealthIQ's deterministic narrative compiler stack.

It exists because the repo already has strong deterministic signal, hypothesis, ranking, and display primitives, but does not yet have a dedicated narrative assembly architecture capable of producing the benchmark-style outputs defined by:

- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`
- `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

This is an architecture authority document for later implementation sprints. It is not an implementation patch.

## 2. Source authorities used
### Planning authorities
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`
- `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

### Runtime/compiler files inspected
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/analytics/interpretation_display_layer_publish_v1.py`
- `backend/core/analytics/balanced_systems_presentation_v1.py`
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/analytics/state_transition_engine.py`
- `backend/core/analytics/insight_graph_builder.py`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/dto/builders.py`

### Contract files inspected
- `backend/core/contracts/report_v1.py`
- `backend/core/contracts/clinician_report_v1.py`
- `backend/core/contracts/insight_graph_v1.py`

### Current runtime evidence
- `backend/artifacts/golden_runs/20260405T085509Z/narrative.txt`

## 3. Deterministic narrative support stack
The deterministic narrative support stack should be treated as four separate layers with explicit authority boundaries.

### 3.1 Data and contract layer
This layer contains deterministic structured inputs and stamps, including:
- biomarker rows and lab ranges
- questionnaire/lifestyle context
- `InsightGraphV1`
- `ReportV1`
- `ClinicianReportV1`
- state transitions
- system states
- arbitration outputs
- IDL inputs and outputs
- actions / confirmatory tests / root-cause evidence

This layer is the source of computational truth. It should not contain freeform narrative prose.

### 3.2 Governed narrative asset layer
This layer should contain the narrative-bearing governed assets that later compilers consume, including:
- pathway explainers
- functional interpretation labels
- confidence / uncertainty templates
- monitoring / resolution criteria
- body-overview posture assets
- lifestyle-to-pathway joins
- governed interpretation entities

This layer is the source of narrative content authority. It should not perform ranking or runtime assembly itself.

### 3.3 Compiler and assembly layer
This layer should:
- consume the data/contract layer
- consume the governed narrative asset layer
- perform deterministic joins and section assembly
- emit narrative contracts

This is the master missing layer.

### 3.4 Output and display layer
This layer should:
- expose compiled narrative contracts in API/runtime outputs
- keep frontend rendering thin
- avoid reconstructing narrative at display time

This layer should surface compiled narrative sections, not re-infer them.

## 4. Compiler boundary decision
### Recommended decision
The deterministic narrative compiler should be a **separate compiler module/layer**, not an extension of `report_compiler_v1.py`.

### Recommended module placement
Recommended new module:

`backend/core/analytics/narrative_report_compiler_v1.py`

### Why it should not extend `report_compiler_v1.py`
`report_compiler_v1.py` is already doing a specific job:
- ranking top findings
- ranking top chains
- shaping `ReportV1`
- deriving compact `ClinicianReportV1` output

This is visible in:
- `backend/core/analytics/insight_graph_builder.py`, where `compile_report_v1(...)` is called during graph construction
- `backend/core/dto/builders.py`, where `compile_clinician_report_v1(...)` is applied later for API shaping

Repo-grounded reasons **not** to overload `report_compiler_v1.py` further:

1. **Wrong stage timing**
   - `compile_report_v1(...)` is invoked inside `build_insight_graph_v1(...)` before orchestrator-level enrichments such as state transitions, system states, precedence/arbitration, and IDL publication are fully surfaced.
   - Benchmark-grade narrative needs those later-layer outputs.

2. **Current responsibility is structured summary, not narrative assembly**
   - `ReportV1` is a compact structured ranking/action contract.
   - `ClinicianReportV1` is a bounded clinician discussion-aid contract.
   - Both are intentionally concise and not designed as full narrative outputs.

3. **Extending it would create brittle coupling**
   - Narrative compilation needs cluster/system posture, lifestyle joins, longitudinal deltas, governed explainer assets, and section-specific prose composition.
   - Injecting all of that into `report_compiler_v1.py` would blur the line between ranking logic and narrative assembly.

4. **Narrative should consume the final enriched picture**
   - The new compiler should operate after the graph has been enriched with:
     - state transitions
     - system states
     - arbitration result / primary driver
     - IDL bundle
     - balanced systems outputs

### Recommended invocation point
The new compiler should be invoked **after orchestrator-level enrichments are complete**, not inside `build_insight_graph_v1(...)`.

Architecturally, that means:
- `ReportV1` remains compiled inside or adjacent to graph construction
- `NarrativeReportV1` is compiled later from the enriched final runtime picture

This supports cleaner layering and future scale.

## 5. Output contract strategy
### Recommended primary contract
Create a new contract:

`backend/core/contracts/narrative_report_v1.py`

Primary root model:

`NarrativeReportV1`

### Why a new contract is preferable
A new contract is preferable to extending `ReportV1` or `ClinicianReportV1` because:

1. **`ReportV1` is a ranking/action contract**
   - It is authoritative for top findings, chains, and actions.
   - It should stay compact and analytics-oriented.

2. **`ClinicianReportV1` is a compact discussion-aid contract**
   - It is authoritative for a short clinician-facing page-1/root-cause structure.
   - It should not become the entire narrative authority for patient summary, body overview, longitudinal narrative, and pathway sections.

3. **Narrative needs section-level authority**
   - Benchmark support requires multiple narrative sections with different inputs, scopes, and audiences.
   - A dedicated narrative contract keeps those outputs governed without overloading legacy contracts.

### Recommended relationship to existing contracts
- `ReportV1`
  - remains authoritative for ranked findings, chains, actions, and root-cause references
- `ClinicianReportV1`
  - remains authoritative for compact clinician summary blocks and confirmatory-test presentation
- `InterpretationDisplayLayerBundleV1`
  - remains authoritative for governed pattern-display records and short `why_it_matters`
- `LayerCFeatureBundleV1`
  - remains authoritative for bounded deterministic feature cards
- `NarrativeReportV1`
  - becomes authoritative for compiled narrative sections

### Recommended contract shape
Recommended top-level sections inside `NarrativeReportV1`:

- `retail_summary`
- `body_overview`
- `lead_narrative`
- `secondary_narratives`
- `longitudinal_narrative`
- `secondary_systems`
- `next_steps_narrative`
- `clinician_synthesis`
- `meta`

### Compiled versus display-time assembly
The following should be emitted as **compiled authoritative assets**, not assembled ad hoc in the frontend:

- `retail_summary`
- `body_overview`
- `lead_narrative`
- `secondary_narratives`
- `longitudinal_narrative`
- `secondary_systems`
- `next_steps_narrative`
- `clinician_synthesis`

Display time should only handle:
- layout
- truncation / expansion
- section ordering that does not change semantic meaning
- audience-specific presentation of already-compiled sections

Display time should **not** decide:
- which pathway leads
- how body-level reassurance is phrased
- how longitudinal direction is described
- how next steps are narratively prioritised
- how multiple sections are fused into a new story

### Authority by output type
- Retail patient summary:
  - authoritative contract: `NarrativeReportV1.retail_summary`
- Body overview:
  - authoritative contract: `NarrativeReportV1.body_overview`
- Pathway-level narrative blocks:
  - authoritative contract: `NarrativeReportV1.lead_narrative` and `secondary_narratives`
- Longitudinal section:
  - authoritative contract: `NarrativeReportV1.longitudinal_narrative`
- Next-steps narrative:
  - authoritative contract: `NarrativeReportV1.next_steps_narrative`
- Rich clinician synthesis:
  - authoritative contract: `NarrativeReportV1.clinician_synthesis`

### DTO/API recommendation
Expose `narrative_report_v1` as a top-level analysis result field in the same spirit as:
- `clinician_report_v1`
- `balanced_systems_v1`
- `interpretation_display_layer_v1`

Do not require the frontend to assemble these sections from lower-level fragments.

## 6. Section-to-compiler model
### 6.1 Retail patient summary
- Intended compiled output type:
  - short, lay-readable summary section
- Likely inputs:
  - ranked lead finding
  - secondary finding
  - direction-of-travel output
  - highest-value next step
- Likely owning asset classes:
  - retail summary templates
  - governed interpretation entities
  - longitudinal summary rules

### 6.2 Body overview / panel posture
- Intended compiled output type:
  - cross-system posture section
- Likely inputs:
  - system states
  - balanced systems output
  - primary driver
  - cluster/system burden outputs
- Likely owning asset classes:
  - body-overview posture assets
  - exclusionary framing templates

### 6.3 Lead pathway narrative
- Intended compiled output type:
  - multi-block lead pattern narrative
- Likely inputs:
  - top finding
  - root-cause evidence
  - pathway explainer assets
  - functional interpretation labels
  - confidence/missing-data assets
  - lifestyle joins
- Likely owning asset classes:
  - pathway explainers
  - functional-label assets
  - confidence templates
  - interpretation entities

### 6.4 Secondary pattern narrative
- Intended compiled output type:
  - secondary narrative section(s)
- Likely inputs:
  - runner-up / ranked findings
  - lipid transport evidence
  - pathway explainer assets
  - hierarchy explanation outputs
- Likely owning asset classes:
  - secondary-pattern templates
  - governed interpretation entities
  - pathway explainers

### 6.5 Longitudinal section
- Intended compiled output type:
  - direction-of-travel section
- Likely inputs:
  - `state_transitions`
  - prior/current raw values when available
  - lifestyle-change context
  - persistence / improvement criteria
- Likely owning asset classes:
  - longitudinal rules
  - monitoring criteria
  - numeric-delta support

### 6.6 Secondary systems worth noting
- Intended compiled output type:
  - "worth noting" narrative section
- Likely inputs:
  - lower-ranked findings
  - system states
  - bounded reassurance / non-lead signals
- Likely owning asset classes:
  - secondary-context templates
  - system-importance rules

### 6.7 Next-steps narrative
- Intended compiled output type:
  - prioritised follow-up section
- Likely inputs:
  - confirmatory tests
  - interventions
  - monitoring actions
  - lifestyle joins
  - pathway resolution criteria
- Likely owning asset classes:
  - next-step templates
  - action-priority rules
  - monitoring criteria assets

### 6.8 Clinician synthesis
- Intended compiled output type:
  - dense closing synthesis
- Likely inputs:
  - body overview output
  - lead and secondary narratives
  - longitudinal summary
  - next-step priority
- Likely owning asset classes:
  - clinician synthesis templates
  - hierarchy explanation assets

## 7. Architectural prerequisites
The following are hard prerequisites for later implementation sprints.

1. **Longitudinal raw-value decision**
   - `snapshot_linker.py` currently preserves only safe status/score metadata from fallback biomarker rows.
   - Benchmark-style numeric delta narration cannot be supported until the contract question is explicitly settled.

2. **Governed interpretation entities before richer narrative prose**
   - Methylation-first, protective-lipid, and cross-system vascular entities should be settled before too much narrative logic is built around them.

3. **Lifestyle-to-pathway joins before contextual narrative**
   - Alcohol -> methylation / macrocytosis and similar joins must exist before those contextual statements can be compiled deterministically.

4. **Pathway explainer asset layer before pathway narrative build**
   - Existing IDL and biomarker explainers are not deep enough for benchmark-grade pathway sections.

5. **Narrative contract decision before frontend use**
   - The frontend should not start consuming ad hoc narrative fragments from `ReportV1`, `ClinicianReportV1`, and IDL in combination.
   - The dedicated narrative contract should be defined first.

## 8. Sprint dependency implications
### `N-2` implications
This sprint should settle:
- compiler boundary
- contract strategy
- section ownership
- prerequisite dependencies

### `N-3` implications
`N-3` must make the explicit longitudinal contract decision:
- raw prior/current values are preserved safely
- or benchmark-style delta narration is declared unavailable

### `N-4` implications
`N-4` should focus on deterministic lifestyle-to-pathway joins, because those are inputs to later narrative assembly rather than a late optional enhancement.

### `N-5` implications
`N-5` should author governed pathway-grade explainer assets and related narrative-bearing governed content.

### `N-6` implications
`N-6` should build functional labels, confidence/uncertainty assets, monitoring criteria, and next-step narrative ingredients.

### `N-7` implications
`N-7` should define the missing governed interpretation entities that the narrative compiler will rely on.

### `N-8` implications
`N-8` should implement:
- `NarrativeReportV1`
- `narrative_report_compiler_v1.py`
- orchestrator/DTO integration

It should not first discover the architecture from scratch.

## 9. Risks and failure modes
### Risk 1 — overloading `report_compiler_v1.py`
If the narrative compiler is added directly into `report_compiler_v1.py`, that module risks becoming a brittle mix of:
- ranking logic
- root-cause shaping
- clinician compact summary
- retail/patient narrative
- longitudinal narrative
- body-wide reassurance

That would make future extension harder and authority boundaries less clear.

### Risk 2 — contract ambiguity
If no dedicated `NarrativeReportV1` is created, the frontend may end up stitching together:
- `ReportV1`
- `ClinicianReportV1`
- IDL
- `balanced_systems_v1`
- Layer C features

This would recreate the very fragmented narrative layer the planning work is trying to eliminate.

### Risk 3 — building narrative before prerequisites exist
If implementation starts before:
- raw-value longitudinal decisions
- interpretation entities
- pathway explainer assets
- lifestyle joins

then the resulting compiler will either overclaim or become packed with temporary logic.

### Risk 4 — display-time assembly drift
If major narrative sections are assembled in the frontend instead of compiled backend-side, deterministic authority and auditability will weaken.

### Risk 5 — architecture chosen for convenience rather than scale
A convenience-first patch into existing compilers may work for AB but fail to scale to future narrative domains.

## 10. Recommended next implementation sprint
`N-3` should now proceed as the next implementation-facing sprint, with a narrower and more explicit mandate:

1. settle the longitudinal raw-value contract decision
2. define safe numeric-delta support if approved
3. prepare deterministic longitudinal inputs for the future narrative compiler

That work should be treated as a prerequisite for benchmark-grade longitudinal narrative, not as a cosmetic enhancement.

## Recommended architecture summary
- **Compiler boundary decision:** separate compiler module
- **Recommended module:** `backend/core/analytics/narrative_report_compiler_v1.py`
- **Recommended primary output contract:** `backend/core/contracts/narrative_report_v1.py`
- **Recommended ownership model:** narrative sections are compiled backend-side and surfaced as authoritative outputs, not assembled at display time
- **Key prerequisite before full build:** `N-3` longitudinal contract decision
