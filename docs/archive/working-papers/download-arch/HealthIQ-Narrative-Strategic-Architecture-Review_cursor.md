# HealthIQ AI — Strategic Architecture Review  
## Narrative assets, UX surfacing, and target experience

**Scope:** Strategy only (no code changes). **Grounding:** Repository inspection as of this review (`HealthIQ-AI-v5`).

---

## 1. Executive summary

HealthIQ already maintains a **strong deterministic core** (scoring, clustering, signal evaluation, arbitration, burden vectors) and **two parallel explanation paths**: (1) **compiler-shaped retail/clinical surfaces** (`clinician_report_v1`, `balanced_systems_v1`) built from `meta.insight_graph.report_v1` and related meta; and (2) **short LLM narratives** (`insights[]`) produced only from **structured contracts** (`InsightGraphV1` + `ExplainabilityReportV1`), not raw labs.

The **primary UX gap** is not missing text in the knowledge base—it is **layering and prioritization**: the hero and trust surfaces are wired to the clinician report compiler, while **rich deterministic explainability** (arbitration traces, dominance/causal structure, full explainability report) and **signal-library prose** (mechanism, pathway, interpretation) are largely **internal or compiler-internal** rather than first-class user-visible story beats. The **Gemini path is correctly bounded** by contract-only inputs, but it is **relegated to “Advanced → Narrative”** and may be **off or empty** depending on `narrative_runtime` policy—so users often experience “world-class reasoning” as **structured clinical copy** without the **connective tissue** (why this system leads, how systems compete, what is reassuringly stable) at the depth the assets allow.

**Strategic recommendation:** Treat **Layer B outputs** (`report_v1`, explainability, balanced systems, retail explainers) as the **authoritative product narrative spine**; use **Layer C (Gemini)** only for **optional polish and category summaries** on top of the same objects; **promote** selected deterministic fields (signal `explanation.*`, explainability summaries) into **compiler-mediated** hero/Why/system-group copy—not raw YAML strings.

---

## 2. Problem statement

The product brief asks for an experience that feels like a **metabolic reasoning engine**—body-level interpretation, balance between strain and resilience, and honest uncertainty—not a **fragmented report**. The codebase already contains many **governed explanation-bearing artifacts**; the open question is whether **surfacing, contracts, and narrative policy** align so users receive that story **in one coherent arc** (hero → evidence → stability → depth).

---

## 3. Narrative / explanation asset inventory

| Asset class | Where it lives | How it is produced | Deterministic vs LLM | Surfaced today? | Notes |
|-------------|----------------|-------------------|----------------------|-----------------|-------|
| **Signal library YAML** (`mechanism`, `biological_pathway`, `interpretation`, implications, `supporting_metrics` roles, thresholds) | `knowledge_bus/packages/**/signal_library.yaml` | Authored/ingested KB | Deterministic (authored) | **Partially** — drives evaluation; prose not generally shown verbatim in main hero | Example: `pkg_kb60_tc_hdl_ratio_high_atherogenic_discordance_pattern/signal_library.yaml` includes rich `explanation.mechanism` and structured `supporting_metrics` with `role` + `rationale`. |
| **`meta.insight_graph`** | Orchestrator pipeline → stored on analysis `meta` | `build_insight_graph_v1` and downstream engines (state, precedence, causal, calibration, burden) | Deterministic | **Indirectly** — FE sees **fragments** via DTO fields and compiled reports, not the full graph in a dedicated UI | `InsightGraphV1` embeds `report_v1`, signal results, burden vectors, arbitration, biomarker nodes, optional `layer_c_features` bundle (`core/contracts/insight_graph_v1.py`). |
| **`report_v1`** | `core/contracts/report_v1.py`; nested under `insight_graph.report_v1` | Report compiler / insight graph assembly | Deterministic | **Via** `clinician_report_v1` compilation | Top findings, chains, actions, `root_cause_v1`, intervention annotations, meta stamps. |
| **`root_cause_v1`** | Under `ReportV1` / clinician compilation inputs | Deterministic graph/report pipeline | Deterministic | **Yes** — clinician report + `RootCauseEvidenceSummary` | Referenced from compiled clinician report sections. |
| **`clinician_report_v1`** | `core/analytics/report_compiler_v1.py` → `core/contracts/clinician_report_v1.py` | **Compiled** from `report_v1` + biomarker rows (+ optional medical history) | Compiler-shaped (deterministic transform) | **Yes** — primary structured UX | Built in `core/dto/builders.py` via `compile_clinician_report_v1`. |
| **`meta.explainability_report` / ExplainabilityReportV1** | `core/analytics/explainability_builder.py`, `core/contracts/explainability_report_v1.py` | Built from `InsightGraphV1` (dominance, causal, burden, arbitration) | Deterministic | **No dedicated FE section** (internal + LLM input) | Docstring in `explainability_builder.py`: deterministic builder for production/tooling. |
| **`meta.burden_vector` / burden fields on graph** | `InsightGraphV1.raw_system_burden_vector`, `adjusted_system_burden_vector`, insight assembler checks | Deterministic engines | Mostly **internal**; DTO exposes some top-level keys | Partial — `builders.py` passes `burden_hash`, `primary_driver_system_id`, `system_capacity_scores`; not a user-facing “burden story” | `core/layer3/insight_assembler_v1.py` asserts DTO exposure expectations for burden. |
| **`insights[]`** | `core/insights/synthesis.py` | **Gemini** (or mock) using **only** serialized `InsightGraphV1` + `ExplainabilityReportV1` | LLM (governed inputs) | **Yes** — Advanced → Narrative tab; `InsightsPanel` | Production path **requires** `explainability_report` (`synthesis.py`); legacy path disabled outside fixture/test mode. |
| **System/group explainers** | Optional `system_educational_explainer` on clusters | Backend retail explainer contracts | Deterministic (governed content) | **Yes** — `ClusterSummary` when present | Typed in `frontend/app/types/analysis.ts` as `SystemEducationalExplainerV1`. |
| **Biomarker educational explainers** | `biomarker_educational_explainer` on biomarker rows | Backend B1A retail explainer | Deterministic | **Yes** — `BiomarkerDials` | Same types file: `BiomarkerEducationalExplainerV1`. |
| **Contribution context** | `contribution_context` on biomarkers | Deterministic factual statements | **Light** — passed into dials as `factual_statement` | Could be expanded |
| **Narrative runtime / policy** | `meta.narrative_runtime` (from synthesis summary) | `core/insights/narrative_runtime_policy.py` | Policy (not user content) | **Yes** — `extractNarrativeRuntimeMeta`, empty-state copy in `InsightsPanel` path | `frontend/app/lib/narrativeRuntimePresentation.ts` documents policy reasons. |
| **Layer C feature stubs** | `LayerCFeatureBundleV1` on `InsightGraphV1` | Placeholder structure in contract | N/A / future | **Not surfaced** as dedicated UI | Metabolic age, heart, inflammation, fatigue, detox fields exist as contract defaults (`insight_graph_v1.py`). |

**Cross-cutting observation:** The **richest consumer-safe prose** in the KB lives in **signal packages**; the **most structured “clinical story”** lives in **`clinician_report_v1`**; the **most complete “why the engine decided this”** lives in **`ExplainabilityReportV1`** but is **not** given a visible section on `/results`.

---

## 4. Current UX surfacing map

Source: `frontend/app/(app)/results/page.tsx` and referenced components.

| Section | User sees | Source fields | Component(s) | Richer data elsewhere? |
|---------|-----------|---------------|--------------|------------------------|
| **Page framing** | “Interpretation first…” | Static + `completed_at`, marker count | Page layout | — |
| **Hero interpretation** | Primary concern, limited page1 copy, ambiguity modes | `clinician_report_v1.sections.page1` | `InsightPanel` | Full `key_findings` list intentionally **not** in hero (comment: defer to Advanced). |
| **Trust strip / quality** | Data quality, confirmatory tests, “missing chapter” line | `clinician_report_v1.data_quality`, `sections.confirmatory_tests`, heuristics vs primary driver | `PipelineStatus` | Explainability report has **additional** traceability not shown. |
| **Lead hypothesis / Why** | Evidence for/against, hypotheses | Clinician report root-cause / evidence structures | `RootCauseEvidenceSummary` | `explainability_report` arbitration/dominance detail not surfaced. |
| **Stable / reassuring systems** | Balanced systems presentation | `balanced_systems_v1` from `compile_balanced_systems_v1` in DTO builder | `BalancedSystemsSummary` | Burden/capacity nuance mostly not shown as narrative. |
| **System groups** | Cluster cards, severity, biomarker lists, optional system explainer | `clusters[]` | `ClusterSummary` | Full `insight_graph.cluster_summary` not exposed as JSON view. |
| **Biomarker evidence** | Dials, refs, interpretation, educational explainer, contribution | `biomarkers[]` | `BiomarkerDials` | Raw values already user-facing; **signal YAML** mechanism text not shown per marker. |
| **Advanced analysis** | Collapsed by default | — | Card + tabs | Progressive disclosure **hides** narrative and full clinician view initially. |
| **Advanced → Overview** | Overall score, risk object, overflow key findings | `overall_score`, `risk_assessment`, clinician page1 | Tabs content | — |
| **Advanced → Narrative** | Short summaries + runtime empty states | `insights[]`, `meta.narrative_runtime` | `InsightsPanel`, `narrativeRuntimePresentation` | Full `InsightGraph` not shown (by design). |
| **Advanced → Clinician report** | Full structured report | `clinician_report_v1`, `balanced_systems_v1` | `ClinicianReportRenderer` | Deepest structured view. |
| **Export** | Full JSON including `meta` | Whole `currentAnalysis` | Button handler | Users **can** inspect `meta.insight_graph` if they export—**not** a guided UX. |

**Weakness diagnosis (typical):** **Surfacing / product-definition** — the **data model supports** a reasoning story; the **default viewport** emphasizes **compiler output + clusters + dials**, while **explainability** and **signal-library prose** are **not mapped** to primary sections.

---

## 5. Gap analysis

| Category | Finding |
|----------|---------|
| **Surfacing gap** | `ExplainabilityReportV1` and **signal `explanation.*`** are **underused** in the primary results flow; users must **export JSON** or **infer** reasoning from clinician wording. |
| **Contract gap** | Layer C **feature bundle** exists in `InsightGraphV1` but is **not** tied to visible product surfaces—risk of **perpetual stub** unless product owns these pillars. |
| **Compiler/report gap** | Clinician report is **strong** but **cannot** alone convey full **precedence / tie-break** story without pulling explainability fields into **compiler** (or a sibling “Why this order” block). |
| **Runtime narrative gap** | `insights[]` may be **empty** when policy disables LLM or validation fails; UX **handles** this (`narrativeRuntimePresentation`) but **does not replace** the missing story with **deterministic** copy from explainability. |
| **Asset-governance gap** | Signal YAML is **rich**; direct surfacing risks **inconsistent tone/length**—needs **templating or compiler excerpts**. |
| **Product-definition gap** | “World-class reasoning engine” requires a **visible graph of influence** (even simplified)—**not yet** a first-class module despite data in `insight_graph`. |

---

## 6. Target user experience definition

After a successful analysis, the user should **walk away with**:

1. **A single clear lead story** — what the engine believes is most important, **and** whether that choice was **obvious or a close call** (modes already exist in `InsightPanel` via `primary_concern_mode`).
2. **Evidence literacy** — what supports the lead, what argues against it, and **what test or missing marker** would change the picture (clinician report + trust strip begin this).
3. **Balance** — **which systems look strained vs stable**, without false reassurance: stability should cite **which markers/patterns** support “doing well,” aligned with `balanced_systems_v1` and cluster explainers.
4. **Connection** — **how markers relate** (ratio patterns, clusters, signal roles)—currently fragmented across clusters and dials; target is **one mental model** (“this pattern ↔ these drivers ↔ this uncertainty”).
5. **Depth on demand** — advanced sections stay **technical/clinical**, not mixed into the hero; export remains for **power users**.

**Emotional targets:** **Reassurance** from transparent handling of ties and missing data; **importance** from a decisive but honest lead; **surprise** from well-placed mechanism snippets; **education** from biomarker/system explainers; **action** from interventions where present in `report_v1` / clinician actions.

---

## 7. Proposed layered explanation architecture

### Layer A — Analytical truth  
**Authority:** Scoring, cluster engine, signal registry evaluation, state/precedence/causal engines, burden computation.  
**Output shape:** `InsightGraphV1` + evaluated signals + vectors.  
**User-facing:** Never raw; always through Layer B or controlled summaries.

### Layer B — Structured explanation contract  
**Authority:** `ReportV1`, `ExplainabilityReportV1`, retail explainer contracts, compilers (`report_compiler_v1`, `balanced_systems_presentation_v1`, `explainability_builder`).  
**Role:** Turn analytical truth into **auditable, versioned objects** suitable for UI and optional LLM.  
**User-facing:** Primary (**clinician_report_v1**, balanced systems, trust, root-cause summaries).

### Layer C — Narrative shaping  
**Authority:** `InsightSynthesizer` + prompts (`core/insights/prompts.py`) — LLM receives **JSON** for `InsightGraphV1` and explainability only (`synthesis.py`).  
**Role:** Short categorical narratives; **must not** invent biomarker values or contradict structured conclusions.  
**User-facing:** Secondary — Advanced → Narrative.

### Layer D — UX surfacing (target sections)

| Section | Purpose | Source authority | Depth / tone | Belongs | Does not belong |
|---------|---------|------------------|--------------|---------|-----------------|
| Hero | Orient and motivate | Compiler clinician page1 + modes | Plain, decisive | Lead, ambiguity, co-primaries | Long lists, raw JSON |
| Trust | Honesty about data limits | Data quality + confirmatory | Neutral | Missing panels, confirm tests | Internal hashes (except optional “details”) |
| Why / evidence | Justify the lead | Root cause + evidence blocks; **future:** explainability excerpts | Clinical but readable | For/against, next tests | Full arbitration trace dumps |
| Stability | Balanced narrative | `balanced_systems_v1` + low-burden systems | Reassuring but conditional | What’s strong and why | Declaring “healthy” without evidence |
| System groups | Pattern language | Clusters + optional system explainers | Educational | Names, members, severity | Signal YAML pasted wholesale |
| Biomarkers | Marker-level truth | Scores, refs, B1A explainers | Factual | Values, ranges, education | Speculative diagnosis |
| Reasoning depth (new target) | “How the engine combined signals” | Explainability + signal roles (mediated) | Structured, stepwise | Dominance, ties, key roles | Raw graph JSON |
| Advanced narrative | Optional polish | `insights[]` | Conversational shortform | Category summaries | Replacing Layer B |
| Advanced clinician | Full report | `clinician_report_v1` | Clinical detail | Interventions, hypotheses | User-intimidating wall of text without TOC |

---

## 8. Deterministic vs Gemini boundary

| Should be… | Examples in repo |
|------------|------------------|
| **Fully deterministic** | Signal evaluation, burden, arbitration outputs, `ExplainabilityReportV1` construction, `report_v1`, retail explainers, DTO compilation. |
| **Compiler-generated from deterministic assets** | `clinician_report_v1`, `balanced_systems_v1`, hero page1 copy. |
| **Gemini-polished (optional)** | `insights[]` — only after **InsightGraph + explainability** are populated (`synthesis.py` enforcement). |
| **Never delegated to Gemini** | Raw lab values, reference ranges, arbitration hashes as **ground truth**, safety-critical escalation rules, **anything** that would bypass `InsightGraphV1` as sole LLM input (violates stated design in `InsightGraphV1` docstring and `synthesis.py`). |

**Assessment:** Gemini is **aimed at the right inputs** (structured contracts only). It is **not** “the answer to everything”—it is **supplementary**. Risk: when LLM is **off** or **empty**, the product **does not** currently **backfill** with deterministic explainability narrative, so the **reasoning layer feels thin** even though `explainability_report` exists.

---

## 9. Balanced narrative strategy

**Current support:** `balanced_systems_v1` is **first-class in the API DTO** and rendered in `BalancedSystemsSummary` **above** deep cluster detail—this is the right **architectural commitment** to “not only bad news.”

**Recommendations:**

- **Elevate** balanced-system copy to **explicitly reference** which **signals or clusters** justify “stable” language (compiler-mediated), reusing **`meta.insight_graph`** stable/low-burden facts—not generic praise.
- **Cross-link** strained vs stable: e.g., “Cardiometabolic strain coexists with preserved **X**” when `cluster_summary` + burden support it.
- **Avoid false reassurance** by tying positives to **observed markers** and **data_quality** flags; reuse trust strip when panel incomplete.

**Assets:** `balanced_systems_v1`, cluster `system_educational_explainer`, optional future **signal explanation** lines for **non-activated** or **optimal** states where the KB supports them.

---

## 10. Signal-library explanation strategy

**Suitability:** Fields like **`explanation.mechanism`** and structured **`supporting_metrics` (`role`, `rationale`)** are **high value** for differentiation but **not** ideal as raw YAML in the UI (length, tone, duplication across signals).

**Recommended use:**

| Field | Best destination |
|-------|------------------|
| `mechanism` / `interpretation` | **Compiler-fed** “Why this signal matters” snippets in **system group** or **hypothesis detail**, not hero (unless top-1 signal). |
| `biological_pathway` | Deeper **education** drawer or biomarker detail—not the default hero. |
| `supporting_metrics` roles | **Internal graph visualization** + **clinician evidence** crosswalks. |
| `implications` | **Action/intervention** alignment with `report_v1` actions (compiler merge). |

**Transformations:** Length limits, **retail vs clinician** tone split, **dedupe** when multiple signals share prose, **version stamps** from signal registry already on `InsightGraphV1`.

---

## 11. Strategic recommendation

1. **Own Layer B as the product spine** — invest in **compiler outputs** and **explainability excerpts** before expanding LLM scope.
2. **Introduce one new user-facing module** — “**How we reached this conclusion**” (non-technical but faithful), fed from **`ExplainabilityReportV1`** + top signal `explanation` lines—**not** raw meta.
3. **Keep Gemini** as **Advanced narrative only**, with **explicit empty-state** that **points to** deterministic reasoning when insights are missing (already partially implemented; extend with **content** not just messaging).
4. **Signal library** becomes **first-class for compilers**, not for direct string paste in React.
5. **Layer C features** in the contract—**either** commit to product pillars (metabolic age, etc.) with UX **or** remove from user-facing roadmap to avoid **stub fatigue**.

---

## 12. Sequenced roadmap / priority next steps

1. **Inventory → UX spec (product):** Define the **exact** copy blocks for a **Reasoning / Why order** section; map each block to **explainability fields** (arbitration, dominance, ties) and **clinician** sections—no new engines until mapped.
2. **Compiler enhancement (backend/product):** Extend **clinician or sibling compiler** to ingest **short deterministic excerpts** from `ExplainabilityReportV1` and **top signals’** `explanation` (with caps)—surface via **new subsection** between hero and clusters (or expand `RootCauseEvidenceSummary` responsibly).
3. **Balanced systems reinforcement:** Add **evidence hooks** (which clusters/signals support “stable”) using existing `meta`—copy-only change in compiler first.
4. **Narrative policy:** When `insights[]` is empty but explainability exists, **emit a deterministic fallback summary** (bullet list) in **`synthesis_summary` or meta**—optional, but closes the “silent reasoning” gap without LLM.
5. **Signal library:** Build **compiler templates** (“signal card”) for **system groups**—pilot on **lipid** packages where YAML is richest.
6. **Layer C features:** Product decision on **`LayerCFeatureBundleV1`** — either **ship** one pillar end-to-end or **hide** from roadmap until ready.

---

### Key file references (for traceability)

- `backend/core/contracts/insight_graph_v1.py` — `InsightGraphV1`, `report_v1`, burden vectors, optional `layer_c_features`.
- `backend/core/contracts/report_v1.py` — `ReportV1`, top findings/chains/actions, `root_cause_v1`.
- `backend/core/analytics/explainability_builder.py` — deterministic `ExplainabilityReportV1`.
- `backend/core/insights/synthesis.py` — production synthesis requires `insight_graph` + `explainability_report`; `narrative_runtime` in summary.
- `backend/core/dto/builders.py` — `compile_clinician_report_v1`, `compile_balanced_systems_v1`, DTO shape.
- `frontend/app/(app)/results/page.tsx` — section order and Advanced tabs.
- `frontend/app/components/insights/InsightPanel.tsx` — hero interpretation contract.
- `frontend/app/lib/narrativeRuntimePresentation.ts` — narrative policy UX.
- `knowledge_bus/packages/**/signal_library.yaml` — signal `explanation` and roles (example package cited above).

---

*End of document.*
