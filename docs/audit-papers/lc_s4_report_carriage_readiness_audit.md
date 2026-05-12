# LC-S4 Report Carriage Readiness Audit

**Audit ID:** LC-S4-LAUNCH-CORE-REPORT-CARRIAGE — pre-sprint readiness gate  
**Date:** 2026-05-12  
**Auditor:** Claude Code — audit / investigation mode (no implementation files modified)  
**Evidence standard:** Every factual claim cites file path and line number. Nothing is asserted from memory or conversational summary. Prior findings are re-verified against current code.

---

## 1. Executive Summary

Sprint 3 (LC-S3) successfully implemented the `ReportV1 → NarrativePayloadV1 → NarrativeReportV1` pipeline for the five governed sections. WP3 rationalised the questionnaire to a SSOT-tiered 38-question form. Both are confirmed complete and merged. The governed Layer B truth now exists and is deterministically assembled.

**The core Sprint 4 problem is not backend production — it is frontend carriage fidelity.**

Of the five `NarrativeReportV1` fields produced by LC-S3, only two reach the user in any meaningful position: `lead_narrative` and `next_steps_narrative` are both inside a collapsed disclosure section ("What this means"), visible only after user interaction. `retail_summary` is used as a hero-body fallback only, invisible on panels where an IDL record exists (which is the launch-core AB and VR case). `clinician_synthesis` is in the advanced / clinician tab. Most critically: **`body_overview` is populated by the backend but not rendered anywhere on the results page** — the `ResultsBodyOverview` component exists and accepts the compiled value, but is never imported in `results/page.tsx`.

Three additional standing obligations from the gate record remain unimplemented: `insights[]` retirement, mock-mode honesty wording, and questionnaire-visible personalisation payoff. All three are Sprint 4 scope.

**Sprint 4 readiness verdict: CONDITIONAL — scope and implementation sequence must be clear before authoring. No engine or schema work is required. Sprint 4 is frontend-only carriage work against governed fields that already exist in the API response.**

---

## 2. Sprint 4 Readiness Verdict

| Condition | Status |
|---|---|
| LC-S3 payload pipeline implemented and merged | ✓ CONFIRMED — `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md` |
| WP3 questionnaire rationalisation complete | ✓ CONFIRMED — `docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md` |
| `NarrativeReportV1` fields produced by backend | ✓ CONFIRMED — see §4 |
| `NarrativeReportV1` fields fully carried by frontend | ✗ FAIL — `body_overview` not rendered; `retail_summary` invisible on IDL panels; see §4 |
| `insights[]` retirement started | ✗ NOT STARTED — `backend/core/models/results.py:155` still defaults `manifest_id: "legacy_v1"` |
| Mock-mode honesty wording implemented | ✗ NOT IMPLEMENTED — no disclosure label exists in the report |
| Questionnaire/statin personalisation visible | ✗ PARTIAL — statin annotation reaches consequence_sentence as technical jargon only |
| IDL `clinical_only` consumer gate enforced | ✓ CONFIRMED CLOSED — `InterpretationPatternsSection.tsx:16` |
| Frontend types aligned to governed fields | ✓ CONFIRMED — `types/analysis.ts` carries all required types |
| Sprint 4 is frontend-only (no engine/SSOT/KB work needed) | ✓ CONFIRMED |

**Overall verdict: READY TO AUTHOR SPRINT 4.** All backend preconditions are met. Sprint 4 scope is bounded frontend carriage work. Sprint 4 must not touch the analytical engine, SSOT, Knowledge Bus, or narrative compiler implementation.

---

## 3. Current Report Surface Map

All evidence from `frontend/app/(app)/results/page.tsx`.

### 3.1 Always-visible sections (primary consumer path)

| Section | Component | Backend field(s) read | Audience |
|---|---|---|---|
| Page header | Inline JSX | `currentAnalysis.completed_at`, `.biomarkers.length` | Consumer |
| Primary hero | `ResultsPrimaryHero` (`ResultsHeroBlocks.tsx`) | `heroSummary` ← `buildPrimaryHeroSummary(narrativeReport?.retail_summary, clinicianReport, firstIdl)` | Consumer |
| Driving signals | `ResultsDrivingSignals` | `topDriverMarkers` ← `wave1_aligned_drivers` or cluster-derived | Consumer |
| Wave 1 domain cards | `Wave1DomainCards` | `currentAnalysis.consumer_domain_scores` | Consumer |
| System health | `BalancedSystemsSummary` | `currentAnalysis.balanced_systems_v1` | Consumer |
| Data quality | `PipelineStatus` | `clinicianReport.data_quality`, `clinicianReport.sections.confirmatory_tests` | Consumer |

### 3.2 "What this means" disclosure section (collapsed by default)

| Sub-section | Component | Backend field(s) read | Audience |
|---|---|---|---|
| Investigation spine | `ResultsInvestigationSpine` | `firstIdlRetailLabel` ← IDL first record | Consumer |
| IDL patterns | `InterpretationPatternsSection` | `interpretation_display_layer_v1.records` (phenotype_allowed only) | Consumer |
| System understanding | `SystemUnderstandingSection` | `balanced_systems_v1`, `clusters` | Consumer |
| Why this lead won | `WhyThisLeadWonSection` | `clinician_report_v1` page1 fields | Consumer / technical |
| Lead and secondary narrative | `NarrativeLeadAndSupportingSections` | `narrative_report_v1.lead_narrative`, `.secondary_narratives`, `.secondary_systems` | Consumer |
| Longitudinal + next steps | `NarrativeLongitudinalAndNextSteps` | `narrative_report_v1.longitudinal_narrative`, `.next_steps_narrative` | Consumer |
| Root cause WHY | `PrimaryFindingAndWhy` | `clinician_report_v1.sections.root_cause` | Consumer / technical |

### 3.3 "Actions" disclosure section (collapsed by default)

| Sub-section | Component | Backend field(s) read | Audience |
|---|---|---|---|
| Action cards | `ResultsActionCardsBlock` | `clusters`, `recommendations`, `insights` (fallback) | Consumer |

### 3.4 "Advanced & clinician report" disclosure section (collapsed by default)

| Sub-section | Component | Backend field(s) read | Audience |
|---|---|---|---|
| Overall score | Inline card | `currentAnalysis.overall_score` | Technical |
| Risk summary | Inline card | `currentAnalysis.risk_assessment` | Technical |
| Overflow key findings | Inline ul | `clinicianReport.sections.page1.key_findings.slice(1)` | Technical |
| Narrative alert | `Alert` | `insights.length` (if > 0) | Misleading (legacy) |
| Clinical interpretation | `InsightPanel` (contextOnly) | `clinician_report_v1` | Clinician |
| Layer C features | `LayerCInsightSection` | `meta.insight_graph.layer_c_features` | Technical |
| System groups | `ClusterSummary` | `clusters` | Consumer |
| Biomarker dials | `BiomarkerDials` | `biomarkers` | Consumer |
| Narrative summaries | `InsightsPanel` | `insights` (legacy_v1 array) | Misleading (legacy) |
| Clinician report | `ClinicianReportRenderer` | `clinician_report_v1` + `narrative_report_v1.clinician_synthesis` | Clinician |

---

## 4. `NarrativeReportV1` Carriage Assessment

Backend produces `NarrativeReportV1` at `backend/core/analytics/narrative_report_compiler_v1.py:735–745`. The LC-S3 assembly path (`narrative_compiler_lc_s3_assembly_v1.py`) drives all five governed fields when `NarrativePayloadV1` is present.

### 4.1 `retail_summary`

- **Produced by:** `_retail_from_payload()` (`narrative_compiler_lc_s3_assembly_v1.py:87–105`)  
- **Backend status:** Populated ✓  
- **Frontend path:** `buildPrimaryHeroSummary(narrativeReport?.retail_summary, clinicianReport, firstIdl)` at `results/page.tsx:182`  
- **Rendering logic:** `resultsPageLayout.ts:229–242` — `retail_summary` is the second-priority source. If `firstIdl` is present, the hero body is built from IDL fields (`buildIdlLedHeroSummary`), not from `retail_summary`.  
- **Gap:** On the launch-core AB and VR panels, IDL records are always present (11 records per the verification ledger). This means `retail_summary` is **never rendered on those panels** — it is silently bypassed by the IDL-led hero path. The `NarrativeRetailSummaryCard` component (`DeterministicNarrativeSurface.tsx:28–56`) exists and is designed to display it, but is **never imported or used** in `results/page.tsx`.  
- **Sprint 4 action:** Wire `NarrativeRetailSummaryCard` into a visible position (recommended: inside "What this means" disclosure, above `NarrativeLeadAndSupportingSections`). This makes `retail_summary` visible regardless of IDL presence.

### 4.2 `lead_narrative`

- **Produced by:** LC-S3 assembly from `lead_yaml_block + rc_block + bridge_block` (`narrative_compiler_lc_s3_assembly_v1.py:280–283`)  
- **Backend status:** Populated ✓ — includes lifestyle bridges when active  
- **Frontend path:** `NarrativeLeadAndSupportingSections` → `narrative?.lead_narrative?.trim()` (`DeterministicNarrativeSurface.tsx:67`)  
- **Rendering location:** Inside "What this means" disclosure (`results/page.tsx:663`), collapsed by default  
- **Audience label:** "Primary focus" within the card (`DeterministicNarrativeSurface.tsx:87`)  
- **Gap:** Content is present and correctly routed, but the section is collapsed by default. A paying user does not see the lead narrative without interaction. The prominence is insufficient for a field that carries the core WHY reasoning.  
- **Sprint 4 action:** Consider whether "What this means" should default open, or whether `lead_narrative` deserves a dedicated always-visible position.

### 4.3 `body_overview`

- **Produced by:** LC-S3 assembly from `_body_overview_payload_sentence(payload) + body_overview_structural_with_ia` (`narrative_compiler_lc_s3_assembly_v1.py:285–290`)  
- **Backend status:** Populated ✓ — includes statin annotation appendix when intervention annotations are active (`narrative_report_compiler_v1.py:662–666`)  
- **Frontend component:** `ResultsBodyOverview` (`results/ResultsBodyOverview.tsx`) — designed to accept `compiledBodyOverview?: string | null` prop  
- **Frontend wiring:** `ResultsBodyOverview` is **NOT imported in `results/page.tsx`** — confirmed by searching the import block and body: no import statement, no JSX usage  
- **Status: CRITICAL GAP — body_overview is produced by the backend but invisible to users**  
- **Impact:** Statin medication context that flows into `body_overview` via `ia_appendix` is also invisible. The cross-system posture section, which is specifically designed to bridge the lead finding into wider context, does not render.  
- **Sprint 4 action (REQUIRED):** Import `ResultsBodyOverview` and render it in `results/page.tsx`. Position: inside "What this means" disclosure, before `NarrativeLeadAndSupportingSections`, or as an always-visible section below the domain cards.

### 4.4 `secondary_narratives`

- **Produced by:** `secondary_text` (secondary pathway blocks) in `narrative_report_compiler_v1.py:733`  
- **Backend status:** Populated when secondary signals exist ✓  
- **Frontend path:** `NarrativeLeadAndSupportingSections` → `narrative?.secondary_narratives?.trim()` (`DeterministicNarrativeSurface.tsx:68`)  
- **Rendering location:** Inside "What this means" disclosure, within the same card as `lead_narrative`  
- **Gap:** Same collapse issue as `lead_narrative` — not visible by default. Minor gap since secondary patterns are secondary by definition.

### 4.5 `longitudinal_narrative`

- **Produced by:** Backend always emits `""` — `narrative_report_compiler_v1.py:740`: `longitudinal_narrative=longitudinal_narrative` where `longitudinal_narrative` is never assigned a non-empty value in the LC-S3 path  
- **Backend status:** Always empty string — by design for current deterministic-mock mode  
- **Frontend path:** `NarrativeLongitudinalAndNextSteps` → conditional render when non-empty — correctly guards against empty  
- **Status:** No gap — empty field correctly produces no render  
- **Sprint 4 action:** None required. Note for Sprint 5+: if longitudinal data is added, the render path is already wired.

### 4.6 `secondary_systems`

- **Produced by:** Backend hardcodes `secondary_systems=""` at `narrative_report_compiler_v1.py:741`  
- **Backend status:** Always empty — by design  
- **Frontend path:** `NarrativeLeadAndSupportingSections` → conditional render  
- **Status:** No gap — correctly renders nothing  
- **Sprint 4 action:** None required.

### 4.7 `next_steps_narrative`

- **Produced by:** `_next_steps_from_payload()` (`narrative_compiler_lc_s3_assembly_v1.py:168–197`)  
- **Backend status:** Populated ✓ — bounded next-step bullets plus confirmatory test lines  
- **Frontend path:** `NarrativeLongitudinalAndNextSteps` → `narrative?.next_steps_narrative?.trim()` (`DeterministicNarrativeSurface.tsx:118`)  
- **Rendering location:** Inside "What this means" disclosure, collapsed by default  
- **Gap:** Collapsed by default. Otherwise correctly routed.  
- **Sprint 4 action:** Linked to whether "What this means" should default open.

### 4.8 `clinician_synthesis`

- **Produced by:** `_clinician_header(payload) + clinician_base_without_consumer_lead` (`narrative_compiler_lc_s3_assembly_v1.py:295–298`)  
- **Backend status:** Populated ✓  
- **Frontend path:** Passed as `deterministicClinicianSynthesis={narrativeReport?.clinician_synthesis}` to `ClinicianReportRenderer` at `results/page.tsx:826`. Rendered inside a violet-tinted card (`ClinicianReportRenderer.tsx:137–147`).  
- **Rendering location:** Inside "Advanced & clinician report" disclosure — collapsed by default  
- **Audience label:** "Clinician synthesis (deterministic compiler)" with description "Compiled synthesis from governed narrative assets — not a live model output."  
- **Gap:** Placement is correct and audience-appropriate. The label clearly marks it as clinician-facing content. No gap for Sprint 4.  
- **Note:** Content uses `**markdown bold**` formatting (`_clinician_header` uses backtick and double-asterisk syntax) that is passed as a raw string to `whitespace-pre-line` rendering — markdown is not parsed. This produces visible asterisk/backtick characters in the rendered output. Sprint 4 should either strip these or use a markdown renderer.

### 4.9 Summary Table

| Field | Backend produces | Frontend renders | Rendered position | Sprint 4 gap |
|---|---|---|---|---|
| `retail_summary` | ✓ populated | Only as hero fallback when no IDL | Hero (bypassed on IDL panels) | Wire `NarrativeRetailSummaryCard` |
| `lead_narrative` | ✓ populated | Yes | "What this means" (collapsed) | Consider prominence |
| `body_overview` | ✓ populated | **NOT RENDERED** | Nowhere | **CRITICAL: import `ResultsBodyOverview`** |
| `secondary_narratives` | ✓ when signals exist | Yes | "What this means" (collapsed) | Consider prominence |
| `longitudinal_narrative` | Always `""` | Guards empty — no render | N/A | None |
| `secondary_systems` | Always `""` | Guards empty — no render | N/A | None |
| `next_steps_narrative` | ✓ populated | Yes | "What this means" (collapsed) | Consider prominence |
| `clinician_synthesis` | ✓ populated | Yes | Advanced section (collapsed) | Strip markdown tokens |

---

## 5. `insights[]` Retirement Assessment

### 5.1 Backend status

`InsightResult.manifest_id` field defaults to `"legacy_v1"` at `backend/core/models/results.py:155`. This has not changed since the Pre-Sprint 1 gap audit. The orchestrator emits 6 generic `legacy_v1` insight payloads on every completed run with empty `biomarkers`, empty `drivers`, empty `evidence`, and `confidence: 0.72` (panel-invariant, profile-invariant).

### 5.2 Frontend consumption paths

| Path | File | Line | What it does |
|---|---|---|---|
| Page-level read | `results/page.tsx` | 141 | `const insights = currentAnalysis?.insights ?? [];` |
| Action card fallback | `results/page.tsx` | 209 | `insights: currentAnalysis?.insights` passed to `buildActionCardModels` |
| Advanced section alert | `results/page.tsx` | 779–787 | Shows Alert when `insights.length > 0` — "N short narrative summaries available" |
| InsightsPanel | `results/page.tsx` | 819 | `<InsightsPanel insights={insights} ...>` in advanced section |
| Actions hub | `actions/page.tsx` | 60–63 | `insights: data.insights` passed to `buildActionCardModels` with `maxItems: 8` |
| ClusterStore | `state/clusterStore.ts` | 466–468 | `updateClustersFromAnalysis` sets `clusterInsights: analysisResults.insights` |
| Action card fallback in layout | `lib/resultsPageLayout.ts` | 418–435 | Iterates `insights` for `ins.recommendations` when cluster/panel recs are thin |

### 5.3 Consumer-path leak assessment

**Results page (advanced section):** The `InsightsPanel` and the preceding `Alert` are inside the "Advanced & clinician report" disclosure, which is collapsed by default. The consumer does not see legacy_v1 insights unless they expand this section. **Risk: medium** — the alert says "N short narrative summaries available in the 'Narrative' list below," which is actively misleading since the content is generic placeholder material, not genuine narrative summaries.

**Actions hub:** `actions/page.tsx` fetches the latest completed analysis and calls `buildActionCardModels(..., { insights: data.insights })`. The `buildActionCardModels` function falls through to `insights[].recommendations` as a fallback source when cluster/panel recommendations are thin (`resultsPageLayout.ts:418`). If cluster recommendations are sparse, legacy_v1 insight recommendations appear as action cards in the Actions hub — a consumer-visible path with no collapse gate. **Risk: high** — this is a primary consumer path.

### 5.4 Recommended Sprint 4 route

Pre-Sprint 1 §3.6 decided: retire as intelligence layer, replace with projection from `top_findings`, `consumer_domain_scores`, `root_cause_v1`, `interpretation_display_layer_v1`, `narrative_report_v1`. The full replacement projection is Sprint 4 scope.

Minimum safe Sprint 4 steps (in dependency order):

1. **Remove `insights` from `buildActionCardModels` calls** in `actions/page.tsx:63` and `results/page.tsx:209`. The fallback to insight recommendations must stop. This is safe because cluster/panel recommendations already provide the primary action source.
2. **Gate `InsightsPanel` and the associated `Alert` behind `HEALTHIQ_LEGACY_INSIGHTS` flag** (or remove the advanced section render of both) so legacy_v1 content is not visible even to advanced users.
3. **Add feature flag check** before `clusterStore.updateClustersFromAnalysis` stores insights — or skip the `clusterInsights` write when all entries are `manifest_id: "legacy_v1"`.

Full deletion (backend `InsightResult` and `AnalysisDTO.insights`) is post-Sprint 4 once the replacement projection is tested safe.

### 5.5 Tests needed

- Test that `buildActionCardModels` does not include recommendations from insights with `manifest_id: "legacy_v1"`
- Test that the `Alert` in the advanced section does not appear when all insights are legacy_v1
- Test that the Actions hub action list does not include legacy_v1 insight recommendations

---

## 6. Mock-Mode Honesty Assessment

### 6.1 Current implementation

- **Approved wording** (Pre-Sprint 1 §3.7): "Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view."  
- **Approval date:** 2026-05-09. Approved as written, no modifications.  
- **Implementation status:** NOT IMPLEMENTED anywhere.

### 6.2 What exists

`extractNarrativeRuntimeMeta()` at `lib/narrativeRuntimePresentation.ts:8` extracts `meta.narrative_runtime` from the analysis result. The returned object carries `runtime_mode`, `synthesizer_allow_llm_resolved`, and `policy_reason`. This data is already available in the frontend via `narrativeRuntime` at `results/page.tsx:150–152`.

`narrativeEmptyPresentation()` at `lib/narrativeRuntimePresentation.ts:45` uses this data to produce honest empty-state copy for `InsightsPanel` when insights are absent. The `policy_reason: 'HEALTHIQ_NARRATIVE_LLM_not_set_default_off'` case produces "Narrative summaries are not enabled in this environment (narrative layer switch)."

**This is the wrong surface.** The empty-state copy appears only inside `InsightsPanel` (in the advanced section) when `insights.length === 0`. It is not a report-level disclosure and is never seen on the launch-core path where insights are present (even as legacy_v1 placeholders).

No disclosure label exists in the report header, footer, hero section, domain cards, or anywhere in the primary consumer flow.

### 6.3 Runtime mode determination

`meta.narrative_runtime.runtime_mode` is available via `currentAnalysis.meta.narrative_runtime`. On every current run, this is `"deterministic_mock"` (confirmed in the verification ledger and the gap map §4.4). `synthesizer_allow_llm_resolved === false` is the flag that governs LLM activation.

The condition for showing the honesty label is:  
`narrativeRuntime?.runtime_mode === "deterministic_mock"` OR `narrativeRuntime?.synthesizer_allow_llm_resolved === false`.

### 6.4 Recommended implementation

**Placement:** Non-intrusive label in the results page header area, visible without scrolling, below the page title and before the hero card.  
**Condition:** When `narrativeRuntime?.synthesizer_allow_llm_resolved === false` (covers deterministic_mock and all non-LLM modes).  
**Wording:** The approved Option B text — do not modify.  
**Component:** A minimal info banner using the existing `Alert`/`AlertDescription` UI primitives. No new component required.

**This is a small, self-contained Sprint 4 task.** It touches only `results/page.tsx` (add one conditional Alert before `ResultsPrimaryHero`) and reads data already extracted at line 150.

---

## 7. Questionnaire / Personalisation Payoff Assessment

### 7.1 Statin annotation

**Backend path:** `format_intervention_annotation_consumer_cv_suffix_v1()` (`intervention_annotation_formatter_v1.py:58–65`) produces a suffix that is appended to the cardiovascular domain card's `consequence_sentence` at `domain_score_assembler.py:424–425`:

```python
_cons_cv = (_cons + " " + _suffix).strip() if _suffix else _cons
```

The suffix text format is: `"Medication context: Layer B intervention annotation — lipid-lowering statin (user-reported; framing only; does not alter signal states, bands, or rankings): effect_type [biomarker_ids] direction=..."`.

**Frontend rendering:** `Wave1DomainCards.tsx:119` renders `d.consequence_sentence` inside the expanded card view ("What this may mean" subsection), visible only after clicking "More detail". The always-visible card body shows `d.headline_sentence` and `d.contributor_sentence` — the statin suffix is in neither.

**Gap 1:** Statin annotation is in `consequence_sentence` only — not visible in the collapsed card state.  
**Gap 2:** The annotation text is technical API-style language ("Layer B intervention annotation — lipid-lowering statin (user-reported; framing only; does not alter signal states, bands, or rankings): modifier_type [ldl_cholesterol_c] direction=lower"). This is not consumer-friendly copy. Pre-Sprint 1 §3.10 Check 3 requires "at least one user-visible field" to differ in a statin-on vs statin-off comparison — the field does differ, but the language is not suitable for a paying user.

**Statin annotation in body_overview:** The `ia_appendix` from `format_intervention_annotation_narrative_appendix_v1()` is appended to `body_overview_with_ia` in the narrative compiler (`narrative_report_compiler_v1.py:662–666`). Since `body_overview` is not rendered (§4.3), this annotation path is also invisible.

**Sprint 4 actions:**  
1. Wire `body_overview` render (§4.3) — this makes the statin narrative appendix visible.  
2. Improve `format_intervention_annotation_consumer_cv_suffix_v1()` output to consumer-readable language — e.g., "Statin medication noted — this may explain lower LDL values on this panel." This is a small formatter change, low risk.

### 7.2 Alcohol / lifestyle bridge

**Backend path:** `_bridge_lines()` at `narrative_report_compiler_v1.py:508–535` reads `meta.lifestyle_interpretation_bridges_v1` for keys including `alcohol_methylation_macrocytosis`. When active, the bridge text is appended to `lead_text` or `secondary_text`, and flows into `bridge_block` in the LC-S3 assembly → `lead_narrative`.

**Frontend rendering:** `lead_narrative` is rendered in `NarrativeLeadAndSupportingSections` inside "What this means" (collapsed by default). The bridge is present in the content when active, but the section must be opened.

**Gap:** The lifestyle bridge is not visible in the primary consumer flow. Pre-Sprint 1 §3.10 Check 2 requires the alcohol-methylation bridge to appear in `lead_narrative` in user-readable language. The bridge does appear there — but only inside a collapsed section. The check is satisfied at data-contract level, not at UX prominence level.

**Sprint 4 action:** If "What this means" defaults to open, this becomes visible without extra action. Alternatively, a one-line personalisation note in the hero area ("Alcohol intake pattern has been considered in this interpretation") would satisfy the prominence requirement.

### 7.3 Other lifestyle context (smoking, sleep, body size, BP)

These lifestyle inputs flow through the `LifestyleModifierEngine` and produce overlay effects on signal confidence and band — they are not surfaced as explicit text in any consumer-facing section. No user-readable sentence says "your BMI of X influenced this interpretation." The gap map §3.7 and Pre-Sprint 1 §3.5 confirm this as a known unmet gap.

**Sprint 4 action:** The minimum satisfying bar is one visible personalisation line in the consumer path. The alcohol bridge in `lead_narrative` may satisfy this if the "What this means" section defaults open. No new engine work is required — the bridges exist in the payload.

### 7.4 Assessment

| Context input | Flows to backend field | Frontend render | Consumer-visible |
|---|---|---|---|
| Statin | `consequence_sentence` (CV card, expanded) + `body_overview` | Expanded domain card only; `body_overview` not rendered | NO (unless card expanded) |
| Alcohol/methylation bridge | `lead_narrative` | "What this means" (collapsed) | NO (unless section opened) |
| Smoking, sleep, BMI, BP | Signal confidence overlays only | No text surface | NO |

**Zero personalisation context is visible in the primary consumer flow without user interaction.** This fails Pre-Sprint 1 §3.5 and §3.10 Checks 1 and 2.

---

## 8. Consumer / Clinician Boundary Assessment

### 8.1 IDL `clinical_only` gate

**Status: CONFIRMED CLOSED.**

`selectVisibleIdlRecords()` at `InterpretationPatternsSection.tsx:16`:
```typescript
.filter((r) => r.enabled_for_frontend === true && r.frontend_allowed_term !== 'clinical_only')
```
No `clinical_only` IDL record can reach a consumer surface regardless of `enabled_for_frontend` value. Confirmed closed in the WP2 second-pass audit; code unchanged.

### 8.2 `clinician_synthesis` placement

Rendered only inside the "Advanced & clinician report" disclosure (`results/page.tsx:822–826`). The card label reads "Clinician synthesis (deterministic compiler)" with description "Compiled synthesis from governed narrative assets — not a live model output." This is an appropriate audience label. The section is collapsed by default.

**Gap:** The content of `clinician_synthesis` uses markdown-style formatting (backtick code spans, `**bold**`) produced by the LC-S3 assembly module. These are rendered via `whitespace-pre-line` in `ClinicianReportRenderer.tsx:145`, not a markdown parser. Asterisks and backticks appear as literal characters in the rendered output. Sprint 4 should strip these tokens or introduce a markdown renderer for this card only.

### 8.3 `InsightPanel` (contextOnly)

`InsightPanel` with `contextOnly` prop at `results/page.tsx:791–795` renders inside the advanced section. This is appropriate placement. The `contextOnly` prop limits what is displayed to non-sensitive content.

### 8.4 `ClinicianReportRenderer`

Full clinician report (page1, root_cause, confirmatory tests, data quality) renders inside the advanced section only. The section is collapsed by default. Appropriate placement.

### 8.5 Consumer-facing claim strength

The Wave1DomainCards use governed language ("not a diagnosis", "Not a simple all-clear" where band is "stable"). The domain card `disclaimer_top` is present in `clinicianReport.header`. Consumer-facing sentence templates (contributor, consequence, next_step) do not contain prohibited claim patterns based on the claim boundary definitions in `NarrativeClaimBoundaryV1`.

**No audience-boundary violations found.** The clinician boundary is well-maintained.

---

## 9. Cross-Section Coherence Assessment

### 9.1 Hero → IDL → clinician lead coherence

Hero title source: `pickPhenotypeLabel()` at `resultsPageLayout.ts:64` — priority order: IDL `retail_display_label` → root cause hypothesis title → cluster name → clinician `primary_concern`.

On AB/VR panels: IDL `retail_display_label` is always first priority. `deriveSecondaryRankedSignalLine()` at `resultsPageLayout.ts:120` surfaces the clinician `primary_concern` as a secondary line if it differs semantically from the IDL title, avoiding a silent contradiction in the hero.

This is correct design: the hero is IDL-led and surfaces the clinician lead as secondary context when they differ. **No contradiction at the hero level.**

### 9.2 Domain cards → hero coherence

The Wave1 cardiovascular card `band_label` and `headline_sentence` are produced by governed sentence templates in `domain_score_assembler.py`. The `headline_cv_coherent()` function is called with the band to select the appropriate copy. No guaranteed cross-check against IDL severity exists in code, but the IDL `severity_state` and the domain card `band_label` are derived from different analytical paths and may disagree on nuance.

**Known open gap (from gap map §3.1):** No regression test enforces that hero severity tone, IDL severity, and domain card band are mutually consistent on the same panel. `test_wave1_contradiction_status.py` is an explicit placeholder.

### 9.3 Clinician `primary_concern` → `retail_summary` coherence

Pre-Sprint 1 §3.10 Check 6 requires: `clinician_report_v1.sections.page1.primary_concern` and `narrative_report_v1.retail_summary` reference the same lead pattern.

The LC-S3 `retail_summary` is built from `_retail_from_payload()` which uses the top-ranked finding from `NarrativePayloadV1.top_findings`. The clinician `primary_concern` is built by `compile_clinician_report_v1()` from the same `report_v1` source. They should agree on lead signal. However: `retail_summary` is invisible on IDL panels (§4.1), so this coherence is untestable from the consumer surface.

**No active cross-section coherence test exists for this.** The fingerprint file `docs/audit-papers/launch-core-proving/latest_fingerprints.json` was stamped at `git_short_sha: 48efd2e` (pre-LC-S3). A Sprint 4 proving run should regenerate it.

### 9.4 Next-steps → clinician lead coherence

`_next_steps_from_payload()` derives confirmatory test lines from `root_cause_v1.findings[lead].hypotheses[].confirmatory_tests` — the same source as the clinician report confirmatory_tests section. Coherence is structural.

### 9.5 Coherence verdict

| Cross-section check | Status |
|---|---|
| Hero IDL title ↔ clinician primary_concern | Bridged by `deriveSecondaryRankedSignalLine` |
| Hero severity ↔ IDL severity ↔ domain band | Not guarded — placeholder test |
| `retail_summary` ↔ `primary_concern` same lead | Structurally aligned; not regression-protected |
| Next steps ↔ clinician confirmatory tests | Structurally coherent |
| Domain card `band_label` ↔ `headline_sentence` polarity | Governed sentence templates reduce risk; not regression-protected |

---

## 10. Placeholder / Demo-Like Content Inventory

| Item | Location | Classification | Sprint 4 action |
|---|---|---|---|
| `insights[]` with `manifest_id: "legacy_v1"` — 6 generic, panel-invariant entries | `backend/core/models/results.py:155` + all frontend consumers | **Remove from consumer path** | Yes — see §5.4 |
| `InsightsPanel` in advanced section rendering legacy_v1 array | `results/page.tsx:819` | **Gate or remove** | Yes |
| `Alert` in advanced section ("N short narrative summaries available") | `results/page.tsx:779–787` | **Misleading — gate or remove** | Yes |
| `ResultsBodyOverview` component — built, not wired | `results/ResultsBodyOverview.tsx` / `results/page.tsx` | **Wire in Sprint 4** | Yes (critical) |
| `NarrativeRetailSummaryCard` — built, not wired | `DeterministicNarrativeSurface.tsx:28–56` | **Wire in Sprint 4** | Yes |
| `longitudinal_narrative` — always empty string from backend | `narrative_report_compiler_v1.py:740` | Acceptable gap — correct guard in UI | No action |
| `secondary_systems` — always empty string from backend | `narrative_report_compiler_v1.py:741` | Acceptable gap — correct guard in UI | No action |
| Statin annotation in `consequence_sentence` — technical jargon | `intervention_annotation_formatter_v1.py:44–47` | **Rewrite to consumer language** | Yes |
| Markdown tokens (`**`, backtick) in `clinician_synthesis` output | `narrative_compiler_lc_s3_assembly_v1.py:200–228` | **Strip or render as markdown** | Yes |
| Overall score card (normalised display score) | `results/page.tsx:706–726` | Acceptable technical detail — in advanced section | No action |
| Risk summary card | `results/page.tsx:729–766` | Acceptable technical detail — in advanced section | No action |

---

## 11. Frontend Type / API Readiness

### 11.1 Governed field types

| Field | TypeScript type | Location | Status |
|---|---|---|---|
| `narrative_report_v1` | `NarrativeReportV1 \| null` | `types/analysis.ts:334` | ✓ Fully typed, all 8 fields |
| `consumer_domain_scores` | `ConsumerDomainScoreV1[] \| null` | `types/analysis.ts:336` | ✓ Fully typed |
| `interpretation_display_layer_v1` | `InterpretationDisplayLayerBundleV1 \| null` | `types/analysis.ts:332` | ✓ Fully typed |
| `clinician_report_v1` | `ClinicianReportV1 \| null` | `types/analysis.ts:324` | ✓ Fully typed |
| `insights` | `Insight[]` | `types/analysis.ts:314` | Typed but field represents legacy_v1 content |
| `meta` | `Record<string, any>` | `types/analysis.ts:322` | Loose — `narrative_runtime` accessed via `any` traversal |
| `intervention_annotations_v1` | Not in `AnalysisResult` interface | — | Not exposed; by design (carried via narrative/domain fields) |

### 11.2 `meta` loose typing

`currentAnalysis?.meta` is typed as `Record<string, any>`. The `narrative_runtime` object is extracted via `extractNarrativeRuntimeMeta()` which returns `NarrativeRuntimeMetaV1 | undefined`. This pattern is correct — the function adds type-safety at the extraction boundary.

`wave1_aligned_drivers` is accessed via a cast at `results/page.tsx:196`:
```typescript
const insightGraph = currentAnalysis.meta?.insight_graph as { layer_c_features?: LayerCFeatureBundleV1 } | undefined;
```
This is an `any`-level cast. It is acceptable for the current sprint as `layer_c_features` is a debug-only surface.

### 11.3 Sprint 4 type additions needed

| Addition | Why needed |
|---|---|
| No new governed field types required | All five `NarrativeReportV1` fields are already typed |
| `ResultsBodyOverview` props are already typed in the component | No new type work for `body_overview` carriage |
| Mock-mode disclosure: reads from `NarrativeRuntimeMetaV1` (already typed) | No new types needed |
| `ResultsBodyOverview.compiledBodyOverview` prop (`string \| null`) | Already typed in component interface |

**No frontend type additions are required for Sprint 4.** All governed fields are correctly typed in `types/analysis.ts`. Sprint 4 is wiring work, not type definition work.

---

## 12. Recommended LC-S4 Implementation Scope

Listed in implementation priority order.

### 12.1 CRITICAL: Wire `body_overview`

**File:** `frontend/app/(app)/results/page.tsx`  
**Action:** Import `ResultsBodyOverview` from `@/components/results/ResultsBodyOverview`. Add to JSX with `compiledBodyOverview={narrativeReport?.body_overview}`, `clinicianReport={clinicianReport}`, `clusters={clusters}`.  
**Recommended position:** Inside "What this means" disclosure, as first child — before `ResultsInvestigationSpine`.  
**Why critical:** `body_overview` is the cross-system posture section and the only frontend surface that carries the statin medication appendix text. It is produced and invisible.

### 12.2 REQUIRED: Implement mock-mode honesty disclosure

**File:** `frontend/app/(app)/results/page.tsx`  
**Action:** Add a conditional `Alert`/`AlertDescription` block between the page header and `ResultsPrimaryHero` (or in the report footer). Condition: `narrativeRuntime?.synthesizer_allow_llm_resolved === false`.  
**Wording:** Exactly as approved: "Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view."  
**Dependencies:** `narrativeRuntime` is already extracted at line 150; `Alert`, `AlertDescription` are already imported.

### 12.3 REQUIRED: Wire `NarrativeRetailSummaryCard`

**File:** `frontend/app/(app)/results/page.tsx`  
**Action:** Import `NarrativeRetailSummaryCard` from `@/components/results/DeterministicNarrativeSurface`. Add inside "What this means" disclosure, after `ResultsBodyOverview`, before `NarrativeLeadAndSupportingSections`.  
**Why:** On IDL panels (launch-core AB/VR), `retail_summary` is the top-level governed narrative lay summary and currently invisible.

### 12.4 REQUIRED: Retire `insights[]` from consumer path

**Files:** `frontend/app/(app)/actions/page.tsx:63`, `frontend/app/(app)/results/page.tsx:209`, `frontend/app/(app)/results/page.tsx:779–819`  
**Actions:**  
a. Remove `insights: data.insights` from `buildActionCardModels` in `actions/page.tsx`.  
b. Remove `insights: currentAnalysis?.insights` from `buildActionCardModels` in `results/page.tsx`.  
c. Gate the `Alert` (line 779) and `InsightsPanel` (line 819) in the advanced section behind `HEALTHIQ_LEGACY_INSIGHTS` env flag or remove them.  
**Why:** Legacy_v1 recommendations can reach the consumer-visible Actions hub and the advanced section presents misleading "N narrative summaries available" copy.

### 12.5 STANDARD: Improve statin consumer copy

**File:** `backend/core/analytics/intervention_annotation_formatter_v1.py:58–65`  
**Action:** Rewrite `format_intervention_annotation_consumer_cv_suffix_v1()` to produce consumer-readable language. Example: "Statin medication noted — expected to lower LDL and may affect this reading."  
**Note:** This is a content change in a formatter module, not an analytical engine change. Low risk.

### 12.6 STANDARD: Strip markdown tokens from `clinician_synthesis`

**File:** `frontend/app/components/results/ClinicianReportRenderer.tsx`  
**Action:** Strip or process `**`, `*`, and backtick tokens from `deterministicClinicianSynthesis` before rendering, or introduce a markdown renderer for the clinician synthesis card.

### 12.7 STANDARD: Consider defaulting "What this means" to open

**File:** `frontend/app/components/results/ResultsDisclosureSection.tsx`  
**Action:** Change `defaultOpen={false}` to `defaultOpen={true}` for the "What this means" disclosure. This makes `lead_narrative`, `next_steps_narrative`, and the body_overview visible without interaction — directly satisfying Pre-Sprint 1 §3.10 Checks 2 and 6.  
**Risk:** Increases initial page visual weight. Acceptable given the section carries the primary governed explanation.

---

## 13. Recommended Tests and Sentinel Candidates

### 13.1 Sprint 4 test recommendations

| Test | Type | Rationale |
|---|---|---|
| `insights[]` with `legacy_v1` manifest do not appear in Actions hub action list | Jest — `resultsPageLayout.ts` unit | CHECK 4 partial — actions path |
| Alert in advanced section does not render when all insights are `legacy_v1` | Jest — `ResultsPage` integration | CHECK 4 partial — results path |
| Mock-mode disclosure appears when `synthesizer_allow_llm_resolved === false` | Jest — `ResultsPage` integration | CHECK from §3.7 approved wording |
| Mock-mode disclosure does not appear when `synthesizer_allow_llm_resolved === true` | Jest — `ResultsPage` integration | Guard against false positive |
| `ResultsBodyOverview` renders when `body_overview` is non-empty | Jest — `ResultsBodyOverview` unit | Body overview carriage |
| `NarrativeRetailSummaryCard` renders when `retail_summary` is non-empty | Jest — component unit | retail_summary carriage |
| `clinician_synthesis` does not render outside "Advanced & clinician report" section | Jest — `ResultsPage` integration | Consumer/clinician boundary |
| IDL `clinical_only` gate remains protected (existing test) | Jest — `InterpretationPatternsSection.test.tsx:84–109` | Already passing — confirm not regressed |
| Statin annotation text in cardiovascular consequence_sentence is consumer-readable | Jest — `intervention_annotation_formatter_v1` unit | Statin language quality |
| Hero phenotype label and `clinician_report_v1.primary_concern` reference the same lead pattern | Backend pytest — proving harness | CHECK 6 partial |
| No band ↔ headline contradiction in cardiovascular domain card (stable band → non-contradictory headline) | Backend pytest / Jest — domain score fixture | CHECK 5 |

### 13.2 Sentinel promotion candidates

The following tests should be promoted to Sentinel (added to `sentinel/packs/` or equivalent) after Sprint 4:

| Test | Sentinel value | Priority |
|---|---|---|
| `insights[]` not visible on consumer Actions path | Prevents regression if someone re-enables legacy insights | High |
| IDL `clinical_only` gate (already tested) | This is a safety boundary; regression must be instantly detected | High — promote if not already in Sentinel |
| Mock-mode honesty wording appears when LLM inactive | Trust claim; must not silently break | Medium |
| Hero/clinician primary_concern same lead on AB fixture | Coherence regression guard (graduates the placeholder) | Medium |

---

## 14. Risk Classification

**Sprint 4 change_type: BEHAVIOUR + CONTENT mix — classify as MIXED → governed using BEHAVIOUR controls (SOP §4).**

Most Sprint 4 changes are frontend-only UI wiring (STANDARD risk). Two exceptions:

| Change | Risk | Reason |
|---|---|---|
| Wire `ResultsBodyOverview` | STANDARD | Frontend carriage only; no analytical engine change |
| `NarrativeRetailSummaryCard` wiring | STANDARD | Frontend only |
| Mock-mode disclosure | STANDARD | Frontend only; reads already-extracted data |
| `insights[]` retirement from consumer path | STANDARD | Frontend wiring change + optional backend model change |
| `format_intervention_annotation_consumer_cv_suffix_v1` rewrite | STANDARD | Formatter module only; does not alter signal states or rankings |
| Defaults-open for "What this means" | LOW | CSS/UX state only |
| Markdown stripping in `clinician_synthesis` | LOW | Rendering post-process only |

No Sprint 4 change touches the Intelligence Core, SSOT, Knowledge Bus, or governing compilers. Sprint 4 is a STANDARD risk sprint per SOP.

---

## 15. Non-Goals

Sprint 4 must not:

- Modify `narrative_report_compiler_v1.py` section assembly logic (that is LC-S3 scope, complete)
- Modify `NarrativePayloadV1` schema or builder
- Add new WHY assets or Knowledge Bus content
- Change `questionnaire.json` or `questionnaire_mapper.py`
- Modify `domain_score_assembler.py` signal logic (statin formatter change is the only acceptable exception, bounded to the formatter module)
- Enable live Gemini or change narrative runtime policy
- Restructure `AnalysisDTO` (Path A deferral is ADR-recorded)
- Implement Sentinel Phase 2
- Broaden the launch-core biology slice
- Run the proving harness (that is Sprint 5)

---

## 16. Open Questions / Blockers

| Question | Owner | Blocking? |
|---|---|---|
| Should "What this means" default open? The governed narrative (lead_narrative, next_steps) is hidden by default. Defaulting it open would satisfy CHECK 2 and 6 without additional work. | Anthony | Recommendation — not a blocker |
| `longitudinal_narrative` is always empty. Should Sprint 4 author a simple "first run" fallback sentence, or leave it empty? | Anthony | No — defer to Sprint 5 |
| Should `body_overview` be always-visible (before domain cards) or inside "What this means"? Positioning affects how strongly Sprint 4 satisfies Check 1 (lifestyle visible payoff). | Anthony | Recommendation — not a blocker |
| The `synthesis.py` GPT ratification gap (standing protocol finding from the WP2 second-pass audit) remains unrecorded. GPT should formally acknowledge this merge before Sprint 4 closes. | GPT | Standing governance gap — not Sprint 4 blocker |
| Proving harness fingerprints (`latest_fingerprints.json`) were stamped at `48efd2e` (pre-LC-S3). Sprint 4 should regenerate them post-implementation to confirm LC-S3 output is stable. | Cursor | Post-Sprint 4 implementation task |

---

## 17. Files Inspected

### Authority documents (full read)
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness_second_pass.md`
- `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md`
- `docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md`
- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
- `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`

### Frontend files (full read unless noted)
- `frontend/app/(app)/results/page.tsx` — full read (843 lines)
- `frontend/app/(app)/actions/page.tsx` — full read
- `frontend/app/components/results/DeterministicNarrativeSurface.tsx` — full read
- `frontend/app/components/results/ResultsHeroBlocks.tsx` — full read
- `frontend/app/components/results/Wave1DomainCards.tsx` — full read
- `frontend/app/components/results/ClinicianReportRenderer.tsx` — full read
- `frontend/app/components/results/InterpretationPatternsSection.tsx` — full read
- `frontend/app/components/results/ResultsBodyOverview.tsx` — full read
- `frontend/app/components/results/BalancedSystemsSummary.tsx` — partial read
- `frontend/app/components/insights/InsightsPanel.tsx` — full read
- `frontend/app/lib/narrativeRuntimePresentation.ts` — full read
- `frontend/app/lib/resultsPageLayout.ts` — partial read (lines 1–60, 60–180, 180–240, 370–435)
- `frontend/app/types/analysis.ts` — full read
- `frontend/app/state/clusterStore.ts` — partial read (lines 450–490)

### Backend files (partial reads)
- `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py` — full read (300 lines)
- `backend/core/analytics/narrative_report_compiler_v1.py` — partial read (lines 508–535, 530–610, 730–746) + grep
- `backend/core/analytics/intervention_annotation_formatter_v1.py` — full read
- `backend/core/analytics/domain_score_assembler.py` — partial read (lines 420–510) + grep
- `backend/core/contracts/narrative_report_v1.py` — full read
- `backend/core/models/results.py` — partial read (lines 140–163)
- `backend/core/pipeline/orchestrator.py` — partial read (lines 2255–2291) + grep

### Test files (partial)
- `frontend/tests/components/insights/InsightsPanel.narrative-framing.test.tsx` — full read
- `frontend/tests/components/InterpretationPatternsSection.test.tsx` — referenced (previously audited in WP2 pass)

---

## Non-Document Files Modified

**NONE.** This audit read code and documentation files only. No implementation files, backend files, frontend files, SSOT files, Knowledge Bus files, Automation Bus artefacts, or Sentinel files were modified.
