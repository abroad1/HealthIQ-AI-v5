# Headline and Concern-Set Current-State Investigation

**Date:** 2026-08-02
**Type:** Read-only repository investigation. No code, tests, configuration, prompts, content, registers or data were changed.
**Trace case:** `analysis_id: b07848c6-c22d-4565-a7c0-f4e2ea620614` (live governed database, `backend/.env` project Postgres, `aws-0-eu-west-1.pooler.supabase.com:5432/postgres`)

Legend used throughout: `DOCUMENTED FACT` (stated in a governance/policy artefact) · `REPOSITORY-VERIFIED CURRENT STATE` (read directly from code, or derived by read-only re-execution against real persisted data this session) · `PRODUCT/POLICY GAP` (a decision the repository shows is still open) · `IMPLEMENTATION CONSTRAINT` (a structural reason a change would require contract/frontend work) · `PROVISIONAL INFERENCE` (reasoned conclusion, flagged as such).

---

## A. Finding eligibility — every stage and its decision type

| Stage | Source (file:function) | Input | Output | Governing policy | Decision type |
|---|---|---|---|---|---|
| Signal activation | `backend/core/analytics/signal_evaluator.py`, `SignalRegistry._load` / `SignalEvaluator.evaluate_all` | canonical biomarkers + lab ranges + loaded package `signal_library.yaml` files | `SignalResult` rows (`signal_state`, `confidence`, `activation_key`) | Knowledge Bus package definitions; `package_runtime_activation_register_v1.yaml` gates which packages load at all | Architectural (deterministic lab-range/override evaluation), not medical judgement at this stage |
| Package reachability gate | `backend/core/knowledge/package_runtime_eligibility_v1.py`, `package_activation_register_v1.py` | package manifest / eligibility classification | reachable / excluded | ARCH-CONV-E runtime activation boundary (this session's ARCH-CONV-I/PKGB-1 audits) | Architectural |
| Duplicate-authority resolution | `root_cause_compiler_v1.py::_dedupe_signal_rows`, `core/knowledge/duplicate_authority_resolution_v1.py` | rows sharing `(signal_id, activation_key)` | one winning row per identity | named duplicate-authority resolution rule; equal-authority ties fail closed | Architectural |
| WHY authority resolution (compiled/legacy/skip/fail-closed) | `backend/core/knowledge/why_authority_v1.py::resolve_frame_why_authority` | `signal_id`, `activation_key`, `compiled_why_authority_register_v1.yaml` | mode: `compiled` / `legacy` / `skip` / `fail_closed` | ratified per-wave Gate 1/Gate 2 decisions (ARCH-CONV-A/B/C/F/G/H/I, ARCH-CONV-PKGB-1) — this session's own audit trail | **Medical** (which content may be emitted) enacted through architectural machinery |
| Root-cause finding compilation | `backend/core/analytics/root_cause_compiler_v1.py::compile_root_cause_v1` | signal rows, WHY authority mode | `RootCauseFindingV1[]` (may be fewer than `top_findings`) | same as above, plus `_compile_why_engine_fallback_finding` (L-04) for uncovered leads | Medical (content) / Architectural (fallback quarantine, `is_governed_hypothesis`) |
| Report-level ranking and inclusion | `backend/core/analytics/report_compiler_v1.py::compile_report_v1` | all signal rows | `ReportV1.top_findings` — **unrestricted, ordered, includes every signal row, no truncation** | `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1` (`docs/intelligence/...`), `TOP_FINDINGS_RANKING_POLICY_VERSION` constant | Presentational (ordering), Architectural (mechanics) |
| Clinician page-1 selection | `report_compiler_v1.py::compile_clinician_report_v1` | `top_findings`, `root_cause_v1.findings` | singular `primary_concern` string; `root_causes` list (all authorised root-cause findings, not truncated); `co_primary_signal_ids`/`runner_up_*` (ambiguity-detection fields) | same policy doc | Presentational |
| Retail/frontend selection | `frontend/app/lib/primaryFindingShaping.ts` (`pickPhenotypeLabel`, `buildPrimaryHeroSummary`, `resolveHeroPrimaryStory`, `getFirstIdlRecord`) | clinician report + IDL bundle | singular `heroTitle`/hero body | LC-S6, ARCH-CONV-CORRECT-1 inline comments (no standalone policy doc found) | Presentational |
| Output-authority provenance labelling | `backend/core/analytics/output_authority_provenance_builder_v1.py` | `top_findings`, `root_cause` | additive `governed`/`quarantined` element lists — does **not** filter or reorder anything upstream (independently confirmed this session, ARCH-CONV-PKGC-2 audit) | ARCH-COMPLETION-2 | Architectural, provenance-only |

**REPOSITORY-VERIFIED CURRENT STATE:** `ReportV1.top_findings` is not truncated anywhere in the backend. `compile_report_v1` (`report_compiler_v1.py:805-834`) sorts **all** `signal_results` and emits one `ReportTopFindingV1` per row with `priority_rank` 1..N. The "single headline" is not a backend list-length restriction — it is a downstream **selection** of `top_findings[0]` for a **singular field**.

---

## B. Ranking model — the exact comparator

**REPOSITORY-VERIFIED CURRENT STATE**, `backend/core/analytics/report_compiler_v1.py:115-133`:

```python
_STATE_RANK = {"at_risk": 4, "suboptimal": 3, "optimal": 2, "unknown": 1}

def _top_finding_sort_tuple(row):
    return (
        -_STATE_RANK.get(state, 1),          # 1. categorical signal_state
        -conf,                                # 2. confidence (float)
        -supp_n,                              # 3. COUNT of supporting_markers (not weighted, not magnitude)
        reasons_key,                          # 4. sorted confidence_reasons tuple (stabiliser)
        primary_metric,                       # 5. lexicographic (stabiliser)
        signal_id,                            # 6. lexicographic (final stabiliser)
    )
```

`ordered_findings = sorted(signal_results, key=_top_finding_sort_tuple)` (line 805) is the **entire** ranking mechanism for `top_findings`.

| Requested ranking input | Used? | Where |
|---|---|---|
| Signal state | **Yes** — primary key | `_STATE_RANK`, categorical only (`at_risk`/`suboptimal`/`optimal`/`unknown`); no numeric severity gradient within a state |
| Confidence | **Yes** — secondary key | raw float from the signal row |
| Supporting-marker completeness | **Yes** — tertiary key, as a **count**, not weighted against magnitude or clinical relevance of which markers | `_supporting_marker_count` |
| Severity / magnitude relative to reference range | **No** — not present anywhere in the tuple | — |
| Absolute threshold distance (e.g. how far above ULN) | **No** | — |
| Persistence / historical trend | **No** — no prior-analysis comparison in this tuple | — |
| Urgency / red flags | **No** — no such field exists on `SignalResult` or in this tuple | — |
| Contradiction / exclusion logic | Indirect only, via `confidence_reasons` string tuple used purely as a tie-break, not a ranking weight | `reasons_key` |
| Domain weighting | **No** | — |
| Actionability | **No** | — |
| Causal vs contextual WHY role | **No** — ranking happens in `report_compiler_v1` **before** `compile_root_cause_v1` is even called (line 879 runs after `top_findings` is built); WHY role cannot influence `top_findings` order | — |
| Deterministic tie-breakers | **Yes** — `reasons_key`, `primary_metric`, `signal_id` (lexicographic) | last three tuple elements |

**UAT trace — exact ordering shown by tuple** (see §J for full derivation): the top four ranked findings for `analysis_id b07848c6...` all tie on `state="suboptimal"`; three (all `signal_mcv_high` frames) also tie on `confidence=0.9` and `supporting_marker_count=3`; the winner among those three, and the reason `signal_transferrin_low` (also `suboptimal`/`0.9`/3-marker) ranks below all three MCV frames rather than above them, is the **lexicographic tie-break on `primary_metric`**: `"mcv" < "transferrin"` as strings.

---

## C. Confidence versus priority — are these distinct concepts in code?

**REPOSITORY-VERIFIED CURRENT STATE:** the implementation **collapses** interpretive confidence, clinical significance, severity, urgency, and actionability into a single ranking scalar built from exactly three governed fields (state, confidence, supporting-marker count). These are presentationally distinct concepts in the codebase's naming (`signal_state` vs `confidence` vs `supporting_markers` are separate DTO fields) but there is no independent "clinical significance" or "severity magnitude" field anywhere in `SignalResult`, `ReportTopFindingV1`, or the sort tuple. Severity, urgency and actionability are not modelled at all in this ranking path.

**Direct answer to "can supporting-marker completeness outweigh magnitude/seriousness":** **Yes, demonstrated, not hypothetical.** In the UAT trace, ALT = 250 U/L against a lab reference max of 49 U/L (>5× the upper limit) ranks **5th and 7th**, below three MCV findings (99.5 fL against a max of 96 fL — a proportionally far smaller deviation) that won on tied state + confidence + a marginally higher supporting-marker count than the ALT findings, with a 0.75/0.7 confidence for the two ALT frames versus 0.9 for MCV. Magnitude relative to reference range plays no role in either the win or the loss — it is not read anywhere in `_top_finding_sort_tuple`.

**DOCUMENTED FACT**, `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` §7 (already anticipates this exact gap): "Implementation must **not** treat lexicographic signal identifiers ... as a clinical reason for primacy," and confidence/supporting-marker inputs are described as things that **should** matter for ranking, but the same document explicitly states in §0.2 that the **current** behaviour ("severity, then confidence, then deterministic tie-break") is "reference, not normative" and is **not** a statement of clinical prioritisation philosophy.

---

## D. Single-headline constraint — root cause

**REPOSITORY-VERIFIED CURRENT STATE — this is a combination, not one single cause:**

1. **Backend contract shape:** `Page1SummaryBlockV1.primary_concern` (`core/contracts/clinician_report_v1.py`, consumed at `report_compiler_v1.py:756`) is a **singular string field**, not a list. `ClinicianSectionsV1.root_cause` (singular, legacy) is separately still present alongside `root_causes` (plural, the full authorised list) — `report_compiler_v1.py:769-770,731`: `legacy_root = root_causes_snapped[0] if len(root_causes_snapped) == 1 else None`. This is a genuine singleton contract field for the headline string.
2. **Report compiler policy:** `primary = top_findings[0] if top_findings else {}` (`report_compiler_v1.py:583`) — explicit index-zero selection for everything the clinician page-1 headline is built from.
3. **Partial ambiguity-awareness already exists but does not remove the singleton:** `_resolve_page1_concern_mode`, `_near_tie_cluster_in_top3`, `_technical_tie_bucket_signal_ids`, `_build_runner_up_page1_fields` (`report_compiler_v1.py:166-260`) implement a **KB-S54B** partial response to the ratified policy — they detect near-ties **across distinct `signal_id`s** and populate `co_primary_signal_ids`/`runner_up_signal_id`/`runner_up_topic_line`/`runner_up_why_not_lead_line`. **This does not detect the UAT case**, because the near-tie cluster is built from `signal_id`, and all three top MCV findings share **one** `signal_id` (`signal_mcv_high`) — `_near_tie_cluster_in_top3` collapses them to a set of size 1 and returns `[]` (§B/§J). Multi-frame-within-one-signal ties are invisible to the existing ambiguity detector.
4. **Frontend component assumptions:** `getFirstIdlRecord` (`frontend/app/lib/resultsPageLayout.ts:536-541`) returns a single `InterpretationDisplayRecordV1 | null`. `pickPhenotypeLabel`, `resolveHeroPrimaryStory`, `buildPrimaryHeroSummary` (`frontend/app/lib/primaryFindingShaping.ts:74-90,152-168,262-292`) all resolve to one `heroTitle`/hero body string via an explicit precedence chain (IDL → narrative retail → clinician page1), with no code path that renders more than one lead concern as a co-equal headline.
5. **Narrative template:** `_why_template`/`_state_consumer_phrase` (`report_compiler_v1.py:79-98`) generate copy phrased around a single named pattern ("X also stood out on this panel"), and `_page1_policy_key_finding_line` explicitly writes "the headline highlights **one** first so discussion has a clear starting point" when ambiguity **is** detected — i.e. even the ambiguity-aware copy still commits to one headline.
6. **Product policy:** the ratified `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1` **already commits** (§4.2) to surfacing ranked ambiguity rather than collapsing to an arbitrary winner "where multiple interpretations are materially plausible and similarly supported" — this is a `DOCUMENTED FACT` of ratified intent, but §9 of the same document explicitly defers all runtime/contract/frontend implementation to "later phases" that were never subsequently authored as an Automation Bus work package (no such work package found anywhere in `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`).

**Hard-coded singleton assumptions found, itemised:**
- `top_findings[0]` index-zero selection (`report_compiler_v1.py:583`)
- `Page1SummaryBlockV1.primary_concern: str` singular field
- `ClinicianSectionsV1.root_cause: Optional[RootCauseFindingV1]` legacy singular field (retained alongside the plural `root_causes`)
- `getFirstIdlRecord` returns `| None`, never a list
- `firstIdl` parameter threaded singular through `resolvePrimaryFindingSeverity`, `pickPhenotypeLabel`, `resolveHeroPrimaryStory`, `buildIdlLedHeroSummary`
- `key_findings = key_findings[:5]` (`report_compiler_v1.py:672`) — **list truncation**, the one place multiple items are deliberately capped
- `co_primary_signal_ids` capped `[:4]` (lines 223, 228) — also list truncation, but only populated in the two ambiguity modes, and never for the UAT case (§ above)

---

## E. Additional findings — what happens below the lead

**REPOSITORY-VERIFIED CURRENT STATE, quantified for the UAT analysis (13 signal rows evaluated, 8 fired at `at_risk`/`suboptimal`):**

- **All 8 fired findings are present in `ReportV1.top_findings`** — confirmed, no backend truncation (§A, §J).
- **Root-cause content is not 1:1 with `top_findings`.** 10 `RootCauseFindingV1` entries exist for this panel, but they are not the same 8 rows: `signal_hepatic_alt_context` (rank 5 in `top_findings`) produces **zero** root-cause content (WHY-skip, ARCH-CONV-I retirement, §J), while `signal_systemic_inflammation`, `signal_lipid_transport_dysfunction`, and `signal_oxygen_transport_capacity` produce root-cause findings **without** appearing in the fired `top_findings` list at all (they are legacy family-level WHY targets that can fire root-cause content from markers other than their own primary-metric threshold activation — confirmed by `authority_scope: family_level` on these rows).
- **Clinician `root_causes` list carries all 10, unfiltered and untruncated** (`compile_clinician_report_v1` — confirmed by direct re-derivation, §J) — this is a genuine, already-present "all findings visible" surface, just not the one rendered as the hero.
- **Display limit:** the only hard list caps are `key_findings[:5]` and `co_primary_signal_ids[:4]` in the clinician DTO; there is no cap on `top_findings` or `root_causes`.
- **Multiple frames from one signal ARE shown separately** in `top_findings` (three distinct `signal_mcv_high` activation keys, ranked 1/2/3 independently) — confirmed by the UAT trace.
- **Contextual findings can crowd out distinct clinical concerns** — demonstrated directly: `signal_systemic_inflammation` (confidence 0.3, CRP-driven) still produces 3 hypotheses and is included in `root_causes`, occupying list space and clinician attention alongside genuinely severe findings, with no confidence floor gating inclusion.
- **No independent "worthy of observation" threshold exists** separate from rank — inclusion in `top_findings`/`root_causes` is purely "did the signal fire," with no minimum-confidence or minimum-severity cut a user-facing surface applies on top of rank.

---

## F. IDL interaction

**REPOSITORY-VERIFIED CURRENT STATE:** IDL enablement and ordering are governed entirely independently of signal ranking.

- **Enablement:** `publish_interpretation_display_layer_v1` (`backend/core/analytics/interpretation_display_layer_publish_v1.py:143-213`) computes `severity_state` per phenotype record from whether its **required** signals fired (`_derive_severity_state`, lines 90-106: `not_observed` → `watch` → `attention` → `strong_signal`), then `enabled = static_enabled and sev != "not_observed"` (line 171).
- **Priority/order:** static, hardcoded `display_order_priority` field from the governed registry YAML, sorted ascending (`interpretation_display_layer_publish_v1.py:163`; frontend re-sorts the same way in `selectVisibleIdlRecordsLocal`, `resultsPageLayout.ts:527-534`). **This static order is completely independent of §B's signal-ranking tuple.**
- **First-record selection:** `getFirstIdlRecord` (`resultsPageLayout.ts:536-541`) takes the first enabled record after that static sort — a single, hardcoded winner.
- **Combination with signal findings:** `buildPrimaryHeroSummary` (`primaryFindingShaping.ts:262-292`) gives the IDL-derived body **precedence** over clinician page1/narrative content whenever any IDL record is enabled at all — "Hero summary precedence: 1) If a visible IDL record exists → IDL-only body ... 2) Else → narrative_report_v1.retail_summary ... else clinician page1" (inline doc comment, lines 258-261).

**UAT trace, quantified — this is a directly demonstrated misordering, not a hypothetical:**

| IDL record | `display_order_priority` | `severity_state` | `enabled_for_frontend` |
|---|---|---|---|
| `ph_metabolic_early_ir_v1` | 1 | `not_observed` | false |
| `ph_hba1c_metabolic_stress_v1` | 2 | `not_observed` | false |
| `ph_vascular_hcy_inflammation_v1` ("Vascular Inflammation Risk") | 3 | **`watch`** | **true** |
| `ph_hepatic_alt_inflammatory_v1` ("Liver Stress Pattern") | 4 | **`attention`** (higher than `watch` on the IDL's own severity scale) | true |
| `ph_renal_stress_v1` | 5 | `not_observed` | false |

`getFirstIdlRecord` selects `ph_vascular_hcy_inflammation_v1` ("Vascular Inflammation Risk") purely because `3 < 4`, **despite** `ph_hepatic_alt_inflammatory_v1` ("Liver Stress Pattern" — the IDL's own liver/ALT-domain record) being enabled with a **strictly higher severity state on the IDL's own internal scale**. This is not merely misaligned with the backend signal ranking (which separately puts ALT at rank 5/7, §J) — it is a demonstrated instance of the IDL's static priority number overriding its **own** severity classification.

**Answer to "is IDL priority clinically coordinated with signal ranking, or independent":** **Independent.** Two fully separate ordering systems exist in this codebase with no cross-referencing code path between them.

---

## G. Current contracts and dependencies

| Surface | File | Assumes |
|---|---|---|
| `ReportTopFindingV1` / `ReportV1.top_findings` | `core/contracts/report_v1.py` | Unrestricted ordered set (no assumption of singularity) |
| `RootCauseFindingV1` / `RootCauseV1.findings` | `core/contracts/root_cause_v1.py` | Unrestricted ordered set |
| `Page1SummaryBlockV1.primary_concern` | `core/contracts/clinician_report_v1.py` | **One primary concern**, string field |
| `ClinicianSectionsV1.root_cause` (legacy) vs `.root_causes` (plural) | same | Both exist simultaneously — a genuine "one primary plus multiple secondary" **partial** contract shape already, but the singular field is still what page-1 narrative logic keys off (`primary_root` selection, lines 603-616) |
| `co_primary_signal_ids`, `runner_up_signal_id` | same | One primary plus **at most** a small (≤4) secondary/co-primary set — the closest existing thing to a concern-set contract, but restricted to the near-tie/technical-tiebreak modes only |
| `InterpretationDisplayLayerBundleV1.records` | `core/contracts/interpretation_display_layer_v1.py` | Unrestricted ordered set at the contract level; frontend collapses to first-enabled |
| `output_authority_provenance_v1` | `core/contracts/output_authority_provenance_v1.py` | Unrestricted `governed`/`quarantined` lists — no primacy assumption at all |
| Frontend `ClinicianReportV1`/`analysis.ts` types | `frontend/app/types/analysis.ts` | Mirrors backend: `root_causes?: ClinicianRootCauseFindingV1[]` (plural, present) alongside singular `primary_concern`/`heroTitle` derivation |
| Frontend hero components | `primaryFindingShaping.ts`, `resultsPageLayout.ts`, `WhyThisLeadWonSection.tsx`, `ResultsBodyOverview.tsx` | **One primary concern** — no component renders a list of co-equal lead concerns today |
| Narrative generator | `core/analytics/report_compiler_v1.py::_why_template`, consumer prose modules | One primary concern, copy phrased in the singular |
| Tests / golden panels | `backend/tests/regression/*`, `backend/tests/fixtures/panels/**` | Golden-panel acceptance harnesses (AB/VR) assert against the singular `primary_concern`/hero fields in numerous places (e.g. `docs/audit-papers/verification-2026-05-04/clinician_report_summary.json`); no test in this repository was found asserting a multi-concern "co-headline" contract |
| Architecture policy | `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | **Ratified intent** for "one primary plus multiple secondary, or ranked ambiguity when warranted" — the only artefact in the repository that already assumes something beyond a pure single-winner model |
| Medical research artefacts | knowledge_bus signal-family research specs, compiled hypotheses | No artefact found this session encoding cross-signal-family severity/urgency/priority — each signal's research spec is self-contained; there is no governed cross-signal priority taxonomy |
| Provenance / result-versioning | `output_authority_provenance_builder_v1.py`, `result_versioning_policy_v1.py` | No primacy assumption — confirmed additive-only (this session's ARCH-CONV-PKGC-2 audit) |

---

## H. Feasibility of a concern-set model — implementation structure only

> Target: "A clinically prioritised set of findings worthy of discussion, ordered by importance, with one optional orienting lead but no requirement to suppress other significant findings."

**IMPLEMENTATION CONSTRAINT common to all four shapes below:** none of them can be delivered without **some** contract change to `ClinicianReportV1`/`Page1SummaryBlockV1`, because `primary_concern` is a bare string with no structured sibling list today beyond the already-present-but-narrow `co_primary_signal_ids`/`root_causes`. The backend `top_findings`/`root_causes` lists themselves require **no** structural change — they are already unrestricted ordered sets (§A, §G). The change is concentrated in the **presentation contract and frontend**, not the ranking/eligibility backend.

### 1. Single lead plus visible secondary concerns
- **Backend:** minimal — extend `Page1SummaryBlockV1` with a small ordered `secondary_concerns: List[ConcernSummaryV1]` (reusing `top_findings[1:N]` already computed); no change to `compile_report_v1`'s core ranking.
- **Contract:** additive field, backward-compatible if new field is optional.
- **Frontend:** add a "secondary findings" card list component; hero logic unchanged.
- **Narrative:** extend `_why_template`-style generation to per-item short copy (already exists in embryonic form via `key_findings`).
- **Migration/versioning:** additive DTO field, no breaking change; existing AB/VR golden fixtures need new expected-field assertions, not rewrites.
- **Testing burden:** low-medium — new field, new component tests.
- **Compatibility risk:** low.
- **Additive?** **Yes** — this shape can be introduced without breaking any existing contract consumer, since `primary_concern` remains present and unchanged.

### 2. Two or three co-primary concerns
- **Backend:** requires generalising `_resolve_page1_concern_mode`'s existing near-tie/technical-tiebreak detection (§D item 3) to also catch multi-frame-within-one-`signal_id` ties (the exact UAT case) — a real logic change, not just a new field.
- **Contract:** `primary_concern: str` becomes semantically inadequate for "2-3 co-equal leads" — likely needs a new `leads: List[ConcernSummaryV1]` replacing or supplementing the singular field.
- **Frontend:** hero component must be redesigned to render N co-equal cards instead of one dominant title — a real UI change, not additive styling.
- **Narrative:** `_page1_policy_key_finding_line`'s "the headline highlights one first" copy contradicts this shape and would need rewriting.
- **Migration/versioning:** likely a **breaking** or dual-field transitional contract change (`extra="forbid"` schemas are called out explicitly in the policy doc §9 as implying versioned change).
- **Testing burden:** medium-high.
- **Compatibility risk:** medium — existing consumers reading `primary_concern` as the sole lead would see reduced information unless the field is preserved as a computed "first of leads."
- **Additive?** Possible if `primary_concern` is preserved as a derived/first-of-`leads` field, but the underlying detection logic change is not purely additive.

### 3. Tiered concern set (prompt review / discuss-investigate / monitor / contextual only)
- **Backend:** requires a genuinely new classification dimension not present anywhere today — none of state, confidence, or supporting-marker-count map cleanly to "prompt review" vs "monitor" without new governed policy input (§C: no severity/urgency/actionability field exists to tier on).
- **Contract:** new tier enum + per-item structure; largest contract change of the four options.
- **Frontend:** new tiered-list UI, distinct from the current flat hero+key-findings shape.
- **Narrative:** new tier-aware copy templates.
- **Migration/versioning:** almost certainly a new major DTO version; not naturally additive to `v1`.
- **Testing burden:** high — new tiering logic needs its own governed correctness tests, likely requiring medical/clinical input on tier boundaries.
- **Compatibility risk:** high without a long transition period.
- **Additive?** Not cleanly — the missing tiering **inputs** (§C, §I) are the real blocker, not just presentation.

### 4. No fixed lead ("These findings deserve attention" with ordered cards)
- **Backend:** simplest of the four in one sense — no "pick one" logic needed at all; `top_findings` already provides the ordered set.
- **Contract:** removes the `primary_concern` singular-string requirement entirely — the largest **behavioural** change of the four (drops a field every existing consumer currently reads), even though the underlying data need not change shape.
- **Frontend:** full hero-section redesign — the single biggest UI change of the four options.
- **Narrative:** all singular-lead copy (`_why_template`, `_page1_policy_key_finding_line`, `resolveHeroPrimaryStory`) needs rewriting or removal.
- **Migration/versioning:** breaking for any consumer keyed on `primary_concern`/`heroTitle` existing and being non-empty.
- **Testing burden:** highest — every existing golden-panel fixture asserting hero/primary-concern text needs rebuilding.
- **Compatibility risk:** highest.
- **Additive?** **No** — this is the only one of the four that is not additive by nature, since it removes rather than supplements the current singular surface.

---

## I. Existing evidence and policy gaps

| Topic | Status | Evidence |
|---|---|---|
| Primary concern definition | **Policy already ratified** | `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md`, Status: `ADOPTED` |
| Ranked ambiguity | **Policy already ratified (principle)**; **implementation partial** | same doc §6; `_resolve_page1_concern_mode` et al. implement a narrow slice (cross-`signal_id` near-ties only) |
| Concern sets (multi-headline) | **Unresolved product decision** | Policy doc §9 explicitly defers "extend contracts if multiple foreground concerns... required" to a future phase never authored as a work package |
| Severity ranking (magnitude-aware) | **Missing implementation, not even partially attempted** | No file found anywhere in `backend/core/` computing severity as a function of distance-from-range; confirmed absent from the ranking tuple (§B) |
| Urgency | **Missing medical-policy evidence entirely** | No field, no doc, no research artefact found encoding urgency as a distinct concept |
| Actionability | **Missing medical-policy evidence entirely** | Same — `ReportInterventionV1.safety_class` (`clinician_referral`/`monitoring`) exists as an **intervention**-side concept but is never fed back into finding **ranking** |
| Multi-finding presentation | **Legacy behaviour, implementation convention only** | `key_findings[:5]` is an ad hoc cap with no governing policy document found specifying "5" as a considered number |
| Headline selection | **Legacy behaviour + partial ratified-policy follow-through** | §D |
| Patient-facing prioritisation (retail/IDL) | **Legacy behaviour, implementation convention only, independent of signal policy** | §F — no policy doc found governing IDL `display_order_priority`'s relationship (or lack of one) to signal-level severity |

---

## J. UAT trace — `analysis_id: b07848c6-c22d-4565-a7c0-f4e2ea620614`

**REPOSITORY-VERIFIED CURRENT STATE.** Persisted `analyses.raw_biomarkers`/`questionnaire_data` were read from the live governed database (read-only `SELECT`s only) and passed through the same canonical normalisation (`core/canonical/normalize.py`), `SignalEvaluator`, `compile_report_v1`, and `compile_clinician_report_v1` functions production uses, entirely in-memory, to deterministically reconstruct the exact ranked output. No database write occurred. This re-derivation is a **PROVISIONAL INFERENCE only in the sense that it re-runs current code against persisted raw inputs rather than reading a persisted `report_v1` snapshot** (the DB's `processing_metadata.client_result_shape_v1` does not itself store `top_findings`/`root_cause_v1`/`primary_concern` — it stores `clusters`, `interpretation_display_layer_v1`, `narrative_report_v1`, `consumer_domain_scores` instead); all raw input values (ALT=250, MCV=99.5, transferrin=2) were independently confirmed against the persisted `raw_biomarkers` column and match the user's stated observations exactly.

| Rank | Signal ID | Activation key | State | Confidence | Supporting markers (n) | WHY role / root-cause presence | Domain | IDL association | Backend (`top_findings`) | Clinician (`root_causes`) | Frontend visible | Reason for reduced prominence / omission |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `signal_mcv_high` | `...::inv_mcv_high_macrocytosis` | suboptimal | 0.90 | 3 | `morphology_context` (compiled) | haematology | none directly | Yes | Yes | Yes — becomes `primary_concern` | — (the winner) |
| 2 | `signal_mcv_high` | `...::inv_mcv_high_megaloblastic_macrocytosis` | suboptimal | 0.90 | 3 | skip (no root-cause row) | haematology | none | Yes | No | Present in `top_findings` only; not in clinician `root_causes` | WHY authority for this specific frame did not resolve to compiled/legacy content |
| 3 | `signal_mcv_high` | `...::inv_mcv_high_nonmegaloblastic_macrocytosis` | suboptimal | 0.90 | 3 | `causal` (compiled) | haematology | none | Yes | Yes | Yes, in `root_causes` list | Not the hero; visible only in the (currently unrendered-as-list) `root_causes` array |
| 4 | `signal_transferrin_low` | `...::inv_transferrin_low_inflammatory_negative_acute_phase_suppression` | suboptimal | 0.90 | 3 | `causal` (legacy family-level) | iron/inflammation | none | Yes | Yes | In `root_causes`; not hero | Lost tie-break to MCV purely on `primary_metric` string comparison ("mcv" < "transferrin") — **not** a clinical reason |
| 5 | `signal_hepatic_alt_context` | `...::inv_alt_context` | suboptimal | 0.75 | 4 | **skip — LEGACY_RETIRED (ARCH-CONV-I)** | hepatic | "Liver Stress Pattern" IDL record enabled but not selected as hero (§F) | Yes | **No — zero root-cause content** | Ranked in backend list; **no explanatory content anywhere downstream** | Confidence/tie-break loss vs MCV, **and** WHY-authority silently retired for this exact frame — the most clinically striking finding on the panel (ALT 250 vs ULN 49) has no root-cause narrative at all |
| 6 | `signal_transferrin_low` | `...::inv_transferrin_low_visceral_protein_depletion_or_synthetic_failure` | suboptimal | 0.75 | 4 | `causal` (legacy family-level) | protein/renal | none | Yes | Yes | In `root_causes` | Lower confidence than rank 1-4 |
| 7 | `signal_alt_high` | `...::inv_alt_high_r_value_hepatocellular_biochemical_pattern` | suboptimal | 0.70 | 6 | `morphology_context` (compiled, ARCH-CONV-I) | hepatic | as above | Yes | Yes | In `root_causes` | The **only** ALT root-cause content that reaches the clinician report belongs to this lower-ranked (#7) frame, not the more-prominent #5 frame |
| 8 | `signal_systemic_inflammation` | `...::inv_inflammation` | suboptimal | 0.30 | 2 | `causal` (legacy family-level, 3 hypotheses) | inflammation | none | Yes | Yes | In `root_causes` | Lowest confidence of all fired findings, still fully included with no floor |

**Additional root-cause-only findings** (produced by legacy family-level WHY targets whose primary metric did not independently cross an activation threshold on this panel, so they do not appear in the `top_findings` table above at all): `signal_lipid_transport_dysfunction` (×2 activation keys), `signal_oxygen_transport_capacity` (×1). All three are present in `clinician.sections.root_causes`.

**IDL bundle for this analysis** (11 phenotype records total, 2 enabled):

| IDL record | Priority | Severity (IDL's own scale) | Enabled | Selected as `firstIdl` |
|---|---|---|---|---|
| `ph_vascular_hcy_inflammation_v1` ("Vascular Inflammation Risk") | 3 | `watch` | true | **Yes** |
| `ph_hepatic_alt_inflammatory_v1` ("Liver Stress Pattern") | 4 | `attention` (higher) | true | No |

`primary_driver_system_id` persisted for this analysis: `cardiovascular_4_biomarkers` — a **third**, separately-computed selection (system-capacity-score driver, `ARCH-CONV-CORRECT-1`), aligned with neither the ranked signal lead (MCV/haematology) nor the selected IDL record (vascular/hcy) nor the most severe raw abnormality (ALT/hepatic). All three cardiovascular-panel biomarkers driving this were persisted as `severity: "normal"` in `clusters` — i.e. the "primary driver system" shown elsewhere in the UI is not flagged abnormal at all on this panel.

**Backend `meta.ranking_signal_id_fallback_invoked`:** `False` for this analysis — the technical-tiebreak-lead ambiguity mode was **not** triggered (it only fires when the *lexicographic signal_id* fallback specifically is invoked across the whole `top_findings` set, a narrower condition than the `primary_metric`-level tie-break that actually decided MCV vs transferrin here). `concern_mode` resolved to `"distinct_lead"` — **no ambiguity was flagged to the user at all**, despite three tied top findings and a fourth near-tied finding immediately behind them.

**Original user-observed behaviour, verified:**
1. "ALT 250 U/L activated the hepatocellular ALT frame and ranked fifth." — **Confirmed exactly** (rank 5, `signal_hepatic_alt_context`).
2. "MCV 99.5 fL produced three MCV findings with confidence 0.9 and became the primary concern." — **Confirmed exactly.**
3. "Low transferrin ranked above ALT." — **Confirmed** (rank 4 vs rank 5/7).
4. "'Vascular Inflammation Risk' appeared as broader context from IDL." — **Confirmed**, and further shown to rank below a higher-severity enabled IDL record on the IDL's **own** scale (§F).
5. "The hero presented one lead finding rather than all findings worthy of discussion." — **Confirmed**, and quantified: 8 fired findings, 10 root-cause findings, exactly 1 rendered as the singular hero.

---

## Conclusions

**1. Exact root cause of the current single-headline behaviour:**
A combination (§D), not one cause: (a) `Page1SummaryBlockV1.primary_concern` is a bare singular string contract field; (b) `top_findings[0]` index-zero selection feeds it; (c) the existing partial ambiguity-detection logic (`_resolve_page1_concern_mode`) only catches ties **across distinct `signal_id`s**, not the far more common case of ties **within** one multi-frame signal_id (exactly the UAT case); (d) frontend hero components are built around a single `heroTitle`/`firstIdl` throughout; (e) narrative copy is phrased in the singular even in the ambiguity-aware branch. The backend ranking/eligibility layer itself (`top_findings`, `root_causes`) is **already** an unrestricted ordered set — the singleton constraint is concentrated in the **presentation contract and downstream consumers**, not in signal eligibility or ranking machinery.

**2. Are clinically relevant findings hidden, de-emphasised, or still accessible?**
**Mixed, and this is a materially important distinction:**
- Findings that reach `top_findings` and have resolved root-cause content (e.g. rank 3, 4, 6, 7, 8 in the UAT trace) are **de-emphasised, not hidden** — present in `report_v1.top_findings` and `clinician_report_v1.sections.root_causes`, just not rendered as the hero by any frontend component found this session.
- **One finding class is genuinely silent, not merely de-emphasised**: `signal_hepatic_alt_context` (rank 5, the ALT frame the user specifically flagged) produces **zero** root-cause content because its sole WHY-authority row is `LEGACY_RETIRED` (ARCH-CONV-I). This is a **separate defect class** from ranking/presentation — it is a WHY-authority coverage gap, not a headline-selection problem, and it means the most visible ALT ranking position on this panel carries no explanation anywhere in the pipeline.
- IDL's non-selected-but-enabled records (e.g. "Liver Stress Pattern" in the UAT trace) are accessible in the `interpretation_display_layer_v1.records` array but not surfaced as the hero.

**3. Can the current architecture support a concern set additively?**
**Partially.** The backend ranking/eligibility layer requires **no** structural change — `top_findings` and `root_causes` are already unrestricted ordered lists. The presentation contract (`Page1SummaryBlockV1`, frontend hero components) requires **additive, non-breaking** contract extension for product shapes 1 and (with care) 2 in §H; shapes 3 and 4 are **not** cleanly additive and would require breaking or major-version contract changes plus new governed inputs (severity/urgency/actionability) that do not exist anywhere in the repository today.

**4. Minimum repository changes required (structure only, not policy):**
- Extend `Page1SummaryBlockV1` with an ordered secondary/co-lead list reusing already-ranked `top_findings[1:N]` (no backend ranking change needed for shape 1).
- Generalise `_near_tie_cluster_in_top3`/`_resolve_page1_concern_mode` to detect ties **within** a shared `signal_id` across multiple frames, not only across distinct `signal_id`s (closes the exact gap the UAT trace exposes).
- Decide and, if approved, remediate the `signal_hepatic_alt_context` WHY-silence separately — this is not a ranking/contract question at all, it is a WHY-authority coverage decision already flagged in this session's own carry-forward register work (Package A/B residuals).
- Any tiering/severity/urgency shape (H.3) requires new governed input fields before any frontend work is meaningful.

**5. Decisions requiring Head of Medical Research input:**
- What severity/urgency/actionability actually means clinically for HealthIQ's signal families (currently undefined anywhere in the repository — §C, §I).
- Whether ALT at 5× ULN should be structurally guaranteed a minimum prominence regardless of confidence/supporting-marker tie-breaks (a genuine clinical-safety question, not an engineering one).
- Tier boundary definitions if product shape 3 (§H) is pursued.

**6. Decisions requiring Anthony's product ratification:**
- Which of the four product shapes in §H to pursue, if any, and in what order.
- Whether to close the `signal_hepatic_alt_context` WHY-silence as its own bounded work package ahead of any headline/concern-set work (it is independently valuable and does not depend on a concern-set decision).
- Whether IDL's static `display_order_priority` should be reconciled with signal ranking, or intentionally kept as an independent editorial ordering (a legitimate product choice either way, but currently undocumented as a choice).

**7. Questions for further independent research (non-implementation):**
- Full enumeration of every golden-panel/AB/VR fixture that asserts against `primary_concern`/hero text, to scope the exact test-migration cost of any breaking shape (H.3/H.4).
- Whether `docs/archive/sprint-history/investigations/KB-S54B_PRIMARY_CONCERN_RANKED_AMBIGUITY_PREFLIGHT.md` and `VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md` (referenced by the ratified policy but not read in full this session) contain additional concrete algorithm proposals that could shortcut §H's design work.
- Whether `primary_driver_system_id`/system-capacity-score selection (a third, independent ranking system observed in the UAT trace) should be brought into the same governed framework as signal ranking and IDL, or remains intentionally separate.

**8. Recommended next non-implementation work package:**
A bounded Stage 0/Gate-1-preparation work package that: (a) takes this document plus the two KB-S54B preflight docs as its evidence base; (b) produces a concrete algorithm proposal for generalising the existing near-tie ambiguity detector to within-`signal_id` ties (the smallest, most clearly-scoped, most clearly-justified-by-evidence first step); (c) separately and explicitly scopes the `signal_hepatic_alt_context` WHY-silence as an independent candidate work package, since it is a real content gap unrelated to the ranking/presentation question and should not be allowed to block or be blocked by it.

---

```text
CURRENT ARCHITECTURE SUPPORTS ADDITIVE CONCERN SET
```

This conclusion applies specifically to product shape 1 (§H.1, single lead plus visible secondary concerns) and, with care, shape 2. It does **not** apply to shapes 3 or 4, which require breaking contract changes and new governed clinical-policy inputs not present in the repository today.
