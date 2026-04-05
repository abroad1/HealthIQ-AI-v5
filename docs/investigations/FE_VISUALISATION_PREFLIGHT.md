# FE-VISUALISATION Preflight — Results Surface Restructure and Delivery Shape

**work_id:** FE-VISUALISATION-PREFLIGHT  
**branch:** n/a (read-only investigation)  
**date:** 2026-04-05  
**status:** COMPLETE

---

## 1. Executive Summary

### What FE-VISUALISATION really is

FE-VISUALISATION is not a "4-widget implementation sprint." The four policy-named components (`InsightPanel`, `ClusterCard`, `BiomarkerChart`, `PipelineStatus`) are all TODO stubs that are **not imported or used anywhere in the live results path**. The results page instead uses a set of differently-named, differently-architected components arranged as a flat 5-tab engineering dashboard.

The real work is a **frontend information-architecture restructure**. The engine already produces the data the policy calls for. The problem is that the frontend does not honour the agreed surface hierarchy — the primary concern (the hero data) is buried in tab 5, visible only to users who click "Clinician Report," while standard users land on an "Overview" tab showing an overall health score and generic risk-assessment bars.

### What can ship immediately

Using data already present in `clinician_report_v1`:

- InsightPanel as hero wired to `page1.primary_concern`, `primary_concern_mode`, and `key_findings`
- Ranked-ambiguity disclosure using `primary_concern_mode` (already typed and rendered in `ClinicianReportRenderer`)
- Translated confidence/data-quality layer wired to `data_quality.confidence_caveat`, `panel_completeness`, and `data_quality_passed`
- ClusterSummary repositioned as the secondary biological-system surface (component is functional)
- BiomarkerDials repositioned as the tertiary supporting surface (component is functional, but has debug artifacts that must be cleaned)
- Improved type coverage for `Cluster` (currently `any[]` in the store)

### What must be deferred

- Biomarker plain-language biological explainers (unknown if `BiomarkerResult.interpretation` is populated by the backend; no guaranteed content)
- Educational body-system explainer layer (no backend support; new content domain)
- Symptom-relevance slot (policy explicitly defers this)
- Translated cluster names (requires verification that the engine's `cluster.name` field contains biological names, not engineering labels)

### Final recommendation

**SPLIT_INTO_RESTRUCTURE_AND_CONTENT_ENRICHMENT**

- **FE-VISUALISATION-A** — Results surface restructure using existing backend data (bounded, deliverable now)
- **FE-VISUALISATION-B** — Enriched explanatory content (deferred; requires backend or content work)

---

## 2. Policy-to-Repo Translation

Source: `docs/architecture/HealthIQ_FE_VISUALISATION_Surface_Policy_Final.md`

### 2.1 Requirements implementable immediately (data exists)

| Policy requirement | Data source | Status |
|---|---|---|
| InsightPanel: surface lead concern when evidence is clear | `clinician_report_v1.sections.page1.primary_concern` | Ready |
| InsightPanel: surface co-primary / ranked-ambiguous concerns | `page1.primary_concern_mode`, `co_primary_signal_ids` | Ready — already typed and rendered in `ClinicianReportRenderer` |
| InsightPanel: confidence / uncertainty in plain language | `page1.confidence_and_missing_data` | Ready |
| InsightPanel: next-step logic | `page1.top_hypothesis_line` | Ready |
| InsightPanel: body-system context | `page1.key_findings`, `page1.chains` | Ready |
| ClusterCard: interpreted state, severity, contributing markers | `cluster.severity`, `cluster.confidence`, `cluster.biomarkers` | Ready (component exists) |
| ClusterCard: short explanation | `cluster.description` | Ready if backend populates `name`/`description` |
| BiomarkerChart: value, unit, range position, interpreted state | `BiomarkerResult.value`, `unit`, `status`, `reference_range` | Ready (BiomarkerDials exists) |
| PipelineStatus / confidence layer: plain-language quality limits | `data_quality.confidence_caveat`, `panel_completeness_present/expected`, `data_quality_passed` | Ready — data exists, component is a stub |
| PipelineStatus: what additional tests would improve confidence | `sections.confirmatory_tests` | Ready |
| Advanced/clinician: ranked ambiguity + supporting/conflicting evidence | `root_cause.hypotheses[].evidence_for/against` | Ready — rendered in `ClinicianReportRenderer` |
| Advanced/clinician: confirmatory tests with rationale | `sections.confirmatory_tests[].rationale` | Ready |
| Surface priority order: InsightPanel hero → ClusterCard → BiomarkerChart → Confidence layer | Page restructure | Architecture work only |

### 2.2 Requirements not yet supported

| Policy requirement | Gap | Deferred to |
|---|---|---|
| BiomarkerChart: brief plain biological explainer per marker | `BiomarkerResult.interpretation` exists in type but backend population is unconfirmed; no guaranteed content | FE-VISUALISATION-B |
| BiomarkerChart: "whether this marker contributes to a broader body-system pattern" | No cross-reference from biomarker to cluster/system exists in the API output | FE-VISUALISATION-B |
| ClusterCard: translated biological system name (not engineering label) | `cluster.name` field exists, but whether it contains a translated biological name or an engine label is unverified | Verify before FE-VISUALISATION-A |
| Educational body-system explainer layer | No engine support; new content domain | Explicitly deferred |
| Symptom-relevance slot | Policy explicitly defers this; no activation | Explicitly deferred |

---

## 3. Current Surface Audit

### 3.1 Results page structure

File: `frontend/app/results/page.tsx`

The results page is a **5-tab flat layout**:

| Tab | Label | Content |
|---|---|---|
| 1 (default) | Overview | Overall health score (numeric, 0–100), risk_assessment bar chart, "Quick Insights" grid (small cards per insight) |
| 2 | Biomarkers | `BiomarkerDials` — dial-per-biomarker grid |
| 3 | Health Clusters | `ClusterSummary` — expandable cluster list |
| 4 | AI Insights | `InsightsPanel` — category-filtered insight browser |
| 5 | Clinician Report | `ClinicianReportRenderer` — structured clinician output |

### 3.2 Hierarchy problems

1. **Primary concern is in tab 5.** Standard users land on tab 1 (health score). The most important interpretation output — `primary_concern`, `primary_concern_mode`, `key_findings`, `top_hypothesis_line` — is in `ClinicianReportRenderer` under tab 5. A standard user who does not click "Clinician Report" never sees it.

2. **Hero component does not exist.** Nothing on the page functions as a lead interpretation surface. Tab 1 leads with a numeric health score and risk-category bars, which is exactly the "chart-first commodity blood app" the policy prohibits.

3. **All five tabs have equal weight.** There is no disclosure tier. Standard content, advanced content, and engineering detail are co-equal tabs.

4. **`InsightsPanel` is an engineering browser, not a hero component.** It shows total insights count, "critical" badge count, average confidence percentage, category selector dropdowns, and collapsible category groups. It does not surface a lead concern. It is closer to a debug inspector than a consumer interpretation surface.

5. **PipelineStatus is a TODO stub and has no replacement.** There is no translated confidence/data-quality layer anywhere on the results page.

6. **Debug artifacts present in `BiomarkerDials`.** Line 321 of `BiomarkerDials.tsx` applies `border-2 border-red-500` and `bg-yellow-50` to every biomarker card. These are debug borders that must not reach production.

### 3.3 Components in active use vs. policy-named stubs

| Component | File | State | Used on results page |
|---|---|---|---|
| `InsightsPanel` | `app/components/insights/InsightsPanel.tsx` | Implemented (engineering browser) | Yes — tab 4 |
| `InsightCard` | `app/components/insights/InsightCard.tsx` | Implemented | Yes — inside InsightsPanel |
| `ClusterSummary` | `app/components/clusters/ClusterSummary.tsx` | Implemented | Yes — tab 3 |
| `BiomarkerDials` | `app/components/biomarkers/BiomarkerDials.tsx` | Implemented (has debug artifacts) | Yes — tab 2 |
| `ClinicianReportRenderer` | `app/components/results/ClinicianReportRenderer.tsx` | Most mature component | Yes — tab 5 |
| **`InsightPanel`** | `app/components/insights/InsightPanel.tsx` | **TODO stub** | **Not used** |
| **`ClusterCard`** | `app/components/clusters/ClusterCard.tsx` | **TODO stub** | **Not used** |
| **`BiomarkerChart`** | `app/components/biomarkers/BiomarkerChart.tsx` | **TODO stub** | **Not used** |
| **`PipelineStatus`** | `app/components/pipeline/PipelineStatus.tsx` | **TODO stub** | **Not used** |

The four policy-named stub components are not imported anywhere in the active results path.

### 3.4 Analysis detail page

File: `frontend/app/(app)/analysis/[id]/page.tsx`

This is also a stub — 8 lines of placeholder. If persisted analyses are to be viewable at `/analysis/[id]`, that page needs to be built.

---

## 4. Data Readiness Audit

### 4.1 `clinician_report_v1` — fully ready

This is the richest engine output and is already fully typed in `frontend/app/types/analysis.ts` (`ClinicianReportV1`).

| Field | Available | Notes |
|---|---|---|
| `sections.page1.primary_concern` | Yes | String; the lead concern |
| `sections.page1.primary_concern_mode` | Yes | `distinct_lead` \| `near_tie_ambiguity` \| `technical_tiebreak_lead` |
| `sections.page1.co_primary_signal_ids` | Yes | String array; co-ranked signal IDs |
| `sections.page1.key_findings` | Yes | String array; max 5 bullets |
| `sections.page1.chains` | Yes | String array; max 2 |
| `sections.page1.top_hypothesis_line` | Yes | One-line hypothesis |
| `sections.page1.confidence_and_missing_data` | Yes | Plain-language confidence statement |
| `sections.page1.ranking_policy_version` | Yes | Policy stamp |
| `data_quality.confidence_caveat` | Yes | Plain-language caveat for confidence layer |
| `data_quality.panel_completeness_present` / `expected` | Yes | Numerics for completeness display |
| `data_quality.data_quality_passed` | Yes | Boolean |
| `data_quality.lab_range_quality_by_primary_metric` | Yes | String array |
| `sections.root_cause.hypotheses[].evidence_for` / `evidence_against` | Yes | Advanced surface: supporting/conflicting evidence |
| `sections.root_cause.hypotheses[].ranking_rationale` | Yes | Advanced surface: why one interpretation ranked above another |
| `sections.confirmatory_tests` | Yes | Array of `{test_id, display_name, rationale}` |

### 4.2 `BiomarkerResult` — mostly ready

| Field | Available | Notes |
|---|---|---|
| `biomarker_name` | Yes | |
| `value`, `unit` | Yes | |
| `status` | Yes | `optimal \| normal \| elevated \| low \| critical` |
| `score` | Yes | 0–1 normalised |
| `reference_range.min/max/unit/source` | Yes | |
| `interpretation` | **Unconfirmed** | Field exists in both `analysis.ts` and `analysisStore.ts` but backend population unknown. Must verify against a live API response before relying on it for FE-VISUALISATION-A. |

### 4.3 `clusters[]` — partial; type coverage gap

| Field | Available | Notes |
|---|---|---|
| `cluster_id` / `id` | Yes | Results page accesses both with fallback |
| `name` | **Unconfirmed as translated** | Field accessed by results page; whether it contains a biological system name or an engineering label is unverified. Must inspect a live API response. |
| `severity` | Yes (API) | Not in the `Cluster` interface in `analysis.ts` — type mismatch |
| `confidence` | Yes (API) | Not in the `Cluster` interface in `analysis.ts` — type mismatch |
| `description` | Yes (API) | Not in `Cluster` interface — type mismatch |
| `recommendations` | Yes (API) | Not in `Cluster` interface — type mismatch |
| `biomarkers` | Yes (API) | `analysis.ts` uses `biomarkers_involved`; API may use `biomarkers` |
| `category` | Yes | |

**Note:** `AnalysisResult.clusters` is typed as `any[]` in `analysisStore.ts`. The `Cluster` interface in `analysis.ts` is sparse and does not match the fields the results page actually reads. Type coverage for clusters must be fixed as part of FE-VISUALISATION-A.

### 4.4 `insights[]` — present but limited

The `insights[]` array has `category`, `severity`, `confidence`, `recommendations`, `biomarkers_involved`. It has no lead-concern concept, no `primary_concern_mode`, and no ranked ambiguity. It is a flat array of equal-weight items, not a priority surface. For the hero surface, `clinician_report_v1.page1` is the correct data source, not `insights[]`.

### 4.5 `overall_score` and `risk_assessment`

Present in `AnalysisResult`. Used on the current Overview tab. These should be demoted to secondary status per the policy (polished charts ≠ meaningful interpretation).

---

## 5. Missing-Content Audit

### 5.1 Biomarker plain-language biological explainers

**Gap:** The policy requires BiomarkerChart to show "a brief explainer of what the marker is responsible for in plain biological language." The `BiomarkerResult.interpretation` field exists in the type definition, but backend population is unconfirmed. No SSOT-derived plain-language content is visible in the frontend types.

**Impact on FE-VISUALISATION-A:** Does not block the restructure. BiomarkerDials can be repositioned correctly without this content. The explainer field can be conditionally rendered if `interpretation` is populated.

**Deferred to:** FE-VISUALISATION-B. If `interpretation` is confirmed empty in live payloads, content authoring or backend enrichment is required before the field is useful.

### 5.2 "Whether this marker contributes to a broader body-system pattern"

**Gap:** The policy requires each biomarker to indicate whether it materially contributes to a body-system pattern (i.e., links to a cluster). No cross-reference between `BiomarkerResult` and `clusters[]` exists in the `AnalysisResult` schema — individual biomarkers do not carry a cluster reference, and clusters carry a `biomarkers[]` list but it is not mapped back.

**Impact on FE-VISUALISATION-A:** Does not block the restructure. This linking would be a frontend derivation (cluster.biomarkers contains the biomarker name → render badge on the biomarker card). Feasible in FE-VISUALISATION-A if cluster names are verified as translated.

**Deferred to:** Partial. The data to derive the link exists; it just requires frontend logic to join `cluster.biomarkers` → `BiomarkerResult.biomarker_name`.

### 5.3 Translated cluster names

**Gap:** The policy requires ClusterCard to show a "translated body-system or pattern name" and explicitly prohibits raw cluster IDs or untranslated engineering objects. The `cluster.name` field exists in the API response but whether it is human-readable ("Metabolic Stress Pattern") or an engine label ("cluster_metabolic_002") is unverified.

**Impact on FE-VISUALISATION-A:** **Must be verified before the sprint is authored.** If cluster names are already translated, this is a non-issue. If they are engine labels, the sprint cannot deliver a compliant ClusterCard.

**Action needed:** Inspect a live API response or the backend cluster schema to confirm `cluster.name` format.

### 5.4 Educational body-system explainer layer

**Gap:** No backend support. This is a new content domain. Would require either static authored content keyed by body system, or a new backend enrichment path.

**Deferred to:** Separate content/enrichment sprint. **Does not block FE-VISUALISATION-A.**

### 5.5 Symptom-relevance slot

**Policy position:** Explicitly deferred. Reserve space in the layout, do not activate.

**Action in FE-VISUALISATION-A:** Include a clearly non-activated reserved slot div in the layout if the sprint authors the full results surface. No content needed.

---

## 6. Recommendation

### SPLIT_INTO_RESTRUCTURE_AND_CONTENT_ENRICHMENT

The split is clean and the boundary is clear.

---

### FE-VISUALISATION-A — Results Surface Restructure (deliverable now)

**Scope:** Restructure the results surface to honour the adopted surface policy using data that already exists in `clinician_report_v1` and current component output.

**Deliverables:**

1. **Results page layout restructure** — replace 5-tab flat layout with a priority-ordered vertical surface:
   - InsightPanel (hero, full width, top of page)
   - ClusterCard/ClusterSummary (secondary, below InsightPanel)
   - BiomarkerDials/BiomarkerChart (tertiary, below clusters)
   - Confidence/data-quality layer (below biomarkers or adjacent)
   - Clinician-depth section (collapsed or gated, preserves existing `ClinicianReportRenderer` output)

2. **InsightPanel implementation** — wire to `clinician_report_v1.sections.page1`:
   - Surface `primary_concern` as the lead statement
   - Render `primary_concern_mode` context (using existing `ClinicianReportRenderer` ambiguity block logic, ported to standard-user language)
   - Surface `key_findings` and `top_hypothesis_line`
   - Surface `confidence_and_missing_data`

3. **PipelineStatus / confidence layer implementation** — wire to `clinician_report_v1.data_quality`:
   - Plain-language completeness: `{present}/{expected} markers analysed`
   - `confidence_caveat` as the primary quality statement
   - `data_quality_passed` as a trust signal
   - Confirmatory tests as "what would improve confidence"

4. **ClusterSummary positioning** — reposition as biological system surface, verify `cluster.name` is translated.

5. **BiomarkerDials cleanup** — remove debug borders/backgrounds (line 321: `border-2 border-red-500 p-2 min-h-[200px] bg-yellow-50`).

6. **`Cluster` type fix** — update `analysis.ts` `Cluster` interface and `analysisStore.ts` `clusters: any[]` to reflect actual API fields (`name`, `severity`, `confidence`, `description`, `recommendations`, `biomarkers`).

7. **Conditional `BiomarkerResult.interpretation` rendering** — if the field is confirmed populated by the backend, surface it on the biomarker card. If not, omit without error.

8. **Reserved symptom-relevance slot** — empty non-visible placeholder per policy §5.5.

**Pre-sprint action required:** Confirm `cluster.name` values from a live API response before the sprint is authored.

---

### FE-VISUALISATION-B — Enriched Explanatory Content (deferred)

**Scope:** Add content-layer depth after backend/content enrichment is available.

**Deliverables (when data exists):**

- Biomarker plain-language biological explainers (when `interpretation` is confirmed populated or SSOT-derived content is available)
- Educational body-system explainer layer (when content domain is authored)
- Cross-linking biomarkers to their contributing body-system clusters (can be derived once cluster names are confirmed translated)
- Translated cluster names (if FE-VISUALISATION-A reveals engine labels rather than biological names)

---

## 7. Likely Touched Surfaces for FE-VISUALISATION-A

| File | Change needed |
|---|---|
| `frontend/app/results/page.tsx` | Full layout restructure — primary change |
| `frontend/app/components/insights/InsightPanel.tsx` | Implement (currently stub) — hero component, wired to `page1` |
| `frontend/app/components/pipeline/PipelineStatus.tsx` | Implement (currently stub) — confidence translation layer |
| `frontend/app/components/clusters/ClusterSummary.tsx` | Reposition; minor rendering adjustments if needed |
| `frontend/app/components/biomarkers/BiomarkerDials.tsx` | Remove debug artifacts (line 321) |
| `frontend/app/types/analysis.ts` | Fix `Cluster` interface to match actual API fields |
| `frontend/app/state/analysisStore.ts` | Fix `clusters: any[]` to typed `Cluster[]` |
| `frontend/app/components/clusters/ClusterCard.tsx` | May replace or supplement `ClusterSummary` for card-level rendering |
| `frontend/app/components/biomarkers/BiomarkerChart.tsx` | May replace or supplement `BiomarkerDials` |
| `frontend/app/(app)/analysis/[id]/page.tsx` | Requires a decision: build as alias to results surface, or defer |

**Not needed for FE-VISUALISATION-A:**
- `frontend/app/components/results/ClinicianReportRenderer.tsx` — preserve as-is; referenced by advanced/clinician surface
- `frontend/app/components/insights/InsightsPanel.tsx` — may be demoted to advanced mode or replaced

---

## 8. Boundary — Out of Scope for FE-VISUALISATION-A

The following must remain outside the sprint boundary:

| Item | Reason |
|---|---|
| Backend engine changes | No engine output changes required; all needed data already exists |
| SSOT content additions | No new SSOT content required for Phase A |
| Biomarker plain-language explainer authoring | Content does not exist; deferring to FE-VISUALISATION-B |
| Educational body-system explainer layer | New content domain; deferring |
| Symptom-relevance implementation | Policy explicitly defers this |
| Advanced/clinician mode redesign | `ClinicianReportRenderer` is preserved; no new clinician work in Phase A |
| New backend API endpoints | Not required; existing `AnalysisResult` payload is sufficient |
| FE-PAGES scale work (history browsing, multi-report) | Out of scope; persistence sprint is separate |
| Auth or session changes | Out of scope |
