# DYNAMIC-PROSE-ARCH-1 — Dynamic Personalised Prose Architecture Review

**Document ID:** DYNAMIC-PROSE-ARCH-1
**Date:** 2026-06-29
**Author:** Claude Code (B2 architecture review)
**Mode:** B2 — strategic architecture review; no implementation; no SOP; no runtime file modification
**Triggered by:** Post-PROSE-INVENTORY-1 / pre-P4-1 strategic planning

---

## 1. Executive decision

**`RECOMMEND_HYBRID_MINIMUM_VIABLE_COMPOSITION`**

The existing HealthIQ architecture is already a hybrid minimum viable composition system. It does not need a new composition engine. What it needs is controlled extension of the assets, modifier binding, and content depth within the existing governed path. The recommendation is to proceed with this controlled extension — not to redesign, not to build a bespoke paragraph library, and not to wait until a novel dynamic engine is designed.

The key insight from the evidence base: the architecture is correct. The gap is asset depth and modifier activation, not architecture.

---

## 2. Sanity check: are we building a monster?

### The monster risk is real — and specific

A prose library becomes a content monster under exactly one condition: when it attempts to create a bespoke paragraph for every combination of personalisation axes.

For HealthIQ's ~79 biomarkers:
- 79 markers × 3 result directions = 237 base assets
- × 2 sex groups = 474
- × 4 age bands = 1,896
- × 6 lifestyle factors (each full prose variant) = 11,376
- × 12 medication classes = 136,512

At this scale the library becomes unmaintainable within six months, medically inconsistent within twelve, and a permanent millstone.

### What would be unmanageable

- Bespoke paragraphs per sex per biomarker where sex affects only the reference range (not the clinical interpretation)
- Age-band-specific prose per biomarker where age affects only normal-range thresholds, not interpretation framing
- Full paragraph rewrites per lifestyle modifier rather than additive context fragments
- Prose variants per medication class applied universally regardless of whether the drug affects that marker
- Supplement wording per supplement per biomarker without evidence that the supplement materially changes interpretation
- Positive resilience language added without a governing signal state that earns it

### What is manageable

- One base biomarker explainer per marker (educational, non-personalised, ~79 assets)
- One signal/frame prose asset per signal per direction (governed by signal activation, ~150–200 assets across all signals)
- One pathway explainer per pathway (~10–12 assets across all Wave 1 domains)
- One subsystem card prose per subsystem (~15–20 assets)
- Additive context modifier fragments: short governed caveats appended when a modifier fires (not replacing the base prose — augmenting it with 1–2 sentences)
- Missing-marker caveats (~25–40 assets across all major biomarkers)
- Weak-evidence fallbacks (~10–15 governed fallback blocks)
- Positive resilience qualifiers (~10–20 assets, each requiring a governing signal state to be earned)

Total manageable asset count: approximately 400–600 distinct prose units. This is a prose library, not a prose explosion.

### What the product needs for beta

- Complete retail explainer coverage (79/79 base biomarker educational content)
- Frame-level signal prose for the six launch-core domains
- Pathway prose for all six launch-core domains (hepatic and metabolic domains still absent)
- Modifier fragments for high-value lifestyle factors (alcohol/hepatic, smoking/inflammatory) and medication classes (statin/LDL, metformin/glucose, NSAID/renal) — not all 35 catalogue entries
- At least bootstrapped positive resilience wording for stable system states
- Missing-marker caveats for the full Wave 1 panel set

### What should be deferred

- Sex-specific prose (sex handles reference range at Layer A; prose separation unwarranted until a signal requires it)
- Age-band-specific prose (same logic — Layer A handles thresholds)
- Supplement modifier wording beyond the high-evidence cases (creatine/creatinine, iron supplements/ferritin-iron interpretation are the immediate candidates)
- Rare medication classes that affect no Wave 1 launch signal
- Positive resilience language beyond earned-signal cases
- Gemini-generated personalised narrative synthesis (P4-2 gate, CEO approval)

---

## 3. Existing documented architecture

The prompt's baseline is largely correct. Corrections and confirmations follow.

### Layer B role (confirmed and extended)

Layer B owns all deterministic medical intelligence including **boilerplate and prose asset selection**. This is explicit in ADR-LAYER-BOUNDARY-RECONCILIATION-1 (2026-06-17):

> "Layer B may produce deterministic prose assets, report sections, explainer selections, structured narrative briefs (`NarrativePayloadV1`), and DTO fields consumed by the frontend."

Layer B selects *which* governed prose modules apply to a given result set. It does not delegate this selection to Layer C, Gemini, or the frontend.

### Layer C role (confirmed)

Layer C is presentation and translation only. The narrative compiler (`narrative_report_compiler_v1.py` and `narrative_compiler_lc_s3_assembly_v1.py`) assembles governed fragments selected by Layer B into `NarrativeReportV1`. It does not add medical reasoning.

### Frontend role (confirmed)

Render-only. `frontend/app/(app)/results/page.tsx` consumes the DTO and renders all three DTO surfaces (clinician report, narrative report, IDL). UAT R2 HIGH=0. No medical inference in frontend code.

### NarrativePayloadV1 role (confirmed, now hardened)

The formal Layer B → Layer C handoff object. Hardened at P2-4 (2026-06-29) with:
- LLM deny-by-default (`future_llm_may_rewrite=False`)
- Deny-all semantics on translation allowlist
- Explicit `introduce_findings_not_in_governed_brief` prohibition
- Non-empty `required_caveats` enforcement when section intents present
- `report_story_priority` validated against section IDs
- `missing_marker_caution_refs` field for missing-marker caveats
- Clinician-reserved sections blocked from LLM translation allowlist

### NarrativeReportV1 role (confirmed)

The Layer C deterministic prose output of `compile_narrative_report_v1()`. Not a place for medical reasoning or new analytical content. Current limitation: one lead block per report (signal-aware routing via `_LEAD_SIGNAL_HINTS` covers iron, thyroid, homocysteine, lipid). Frame-level discrimination deferred to P2-FRAME-ROUTING-ARCHITECTURE-1.

### Existing prose asset locations

| Asset type | Location | Status |
|---|---|---|
| Base biomarker explainers | `backend/ssot/retail_explainer_v1/registry.yaml` | Partial — 40/~79 |
| System prose (domain level) | `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`; compiled health system cards | Partial — 3 Wave 1 domains documented; 6 domains active |
| Subsystem evidence prose | `knowledge_bus/compiled/health_system_cards/` | Partial — 6+ subsystems |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` | Partial — 5 (homocysteine, lipid, iron, thyroid, renal) |
| Signal/frame interpretation prose | KB packages `signal_library.yaml`; YAML interpretation entities in narrative compiler | Partial — iron, thyroid, homocysteine, lipid lead routing wired |
| Context modifier governance | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` | 35 entries catalogued, all `runtime_active: false` |
| Medication modifier source | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml` | Catalogued, not wired |
| Supplement modifier entries | Within `context_modifier_catalogue_draft_v1.yaml` | 7 entries (creatine, iron, B12, vitamin D, folate, protein, testosterone) — all inactive |
| Missing-marker caveats | `knowledge_bus/missing_marker_explainers_v1/missing_marker_explainers_v1.yaml` | Bootstrapped — 6 entries |
| Positive/resilience qualifiers | Not yet as a dedicated asset type | Absent as governed library |
| Lifestyle modifier engine | `backend/core/analytics/lifestyle_modifier_engine.py` | Engine exists; binding extent unknown |

### Baseline correction: supplement modifiers are not unknown

The prompt states supplement modifiers are unknown. They are documented. The context modifier catalogue contains seven supplement modifier entries (creatine, iron, B12, vitamin D, folate, protein, testosterone/hormone supplementation), all with `runtime_active: false`, all with `requires_governed_wording` or `requires_clinical_review_before_activation` safety status. The gap is runtime binding and governed prose fragments, not a catalogue gap.

### What is already implemented or partial

- Layer B signal activation, scoring, root-cause compilation: implemented
- NarrativePayloadV1 B→C brief contract: implemented and hardened
- Layer C narrative compiler with signal-aware lead routing: implemented
- Triple DTO surface (clinician report, narrative report, IDL): implemented
- Retail explainer registry load and assembly: implemented
- Missing-marker caution representability via NarrativePayloadV1: implemented (P2-4)
- Frame-level routing: deferred
- Context modifier runtime binding: architecture documented, none active

---

## 4. Options comparison

| Dimension | Option A — Flat prose library | Option B — Fully dynamic composition engine | Option C — Hybrid minimum viable composition |
|---|---|---|---|
| **Description** | One complete bespoke paragraph per biomarker/result/context combination | Small fragments selected and composed by deterministic rules into personalised explanations | Base explainers + frame prose + additive modifier fragments; deterministic selector in Layer B |
| **Simplicity** | High initially; degrades rapidly as context axes are added | Low — requires new composition engine, fragment taxonomy, testing matrix | Medium — builds on existing architecture without redesign |
| **Speed to beta** | Fast initially; content authoring bottleneck within weeks | Slow — engine build + testing precedes any content | Fastest — architecture exists, gap is asset depth |
| **Maintenance burden** | Extreme — content explosion at scale | Medium — fragments are small but governance of interactions is complex | Low — modifier catalogue + governed fragments; reuse model keeps growth controlled |
| **Risk of duplication** | Very high — same clinical content repeated across many permutations | Low — fragments authored once, applied by rule | Low — base assets authored once; modifiers are additive only |
| **Personalisation quality** | High for authored combinations; absent for un-authored ones | High in theory; constrained by fragment interaction rules | Good — personalisation comes from signal activation + additive modifier context |
| **Medical safety** | Risk of contradictory wording across variants; unreviewed combinations | Risk if fragment interactions are not governed; low if governed | Controlled — base prose + governed modifier fragments; no invention |
| **Long-term scalability** | Poor — does not scale beyond a narrow panel set | Good if engine is correct | Good — asset catalogue grows incrementally by governed batch |
| **Combinatorial explosion risk** | High | Medium (fragments are small) | Low if guardrails enforced |
| **Gemini compatibility** | Gemini polishes pre-written paragraphs | Gemini polishes assembled fragments | Gemini polishes NarrativePayloadV1 sections — best compatibility |
| **Frontend usefulness** | High if authored; inconsistent if coverage patchy | High if engine works | High — existing render path already handles this |

**Verdict:** Option C is the correct path. Option A becomes a millstone within months. Option B requires a new engine that does not exist in the codebase and would delay beta by sprints. Option C is what the architecture already implements; the work is extension, not redesign.

---

## 5. Recommended target architecture

The existing architecture is the target. The diagram below reflects it as it should be extended:

```
[Research / PSI / investigation specs]
        ↓
[Knowledge Bus packages: signal_library.yaml, PSI, pathway explainers, missing-marker caveats]
        ↓
[Layer B — deterministic selection engine]
  - Signal activation (evaluators, scoring)
  - Frame selection (per signal/direction/pattern)
  - Prose asset selection:
      · Base biomarker explainer from retail_explainer_v1/registry.yaml
      · Signal/frame interpretation entity from narrative compiler YAML
      · Pathway explainer from pathway_explainers_v1.yaml
      · Applicable context modifier fragments from modifier catalogue
      · Missing-marker caution refs
      · Positive/resilience qualifier (if earned by signal state)
  - NarrativePayloadV1 construction:
      · Section intents with evidence boundaries
      · required_caveats (non-empty when intents present)
      · missing_marker_caution_refs
      · LLM deny-by-default
      · may_translate_section_ids allowlist (deny-all when empty)
        ↓
[NarrativePayloadV1 — governed B→C handoff object]
        ↓
[Layer C — deterministic compiler]
  - compile_narrative_report_v1() + LC-S3 assembly
  - Signal-aware lead entity selection
  - Graceful fallback when no scoped entity matches
  - No new medical reasoning
        ↓
[NarrativeReportV1 — deterministic prose output]
        ↓
[DTO — triple surface: clinician_report_v1, narrative_report_v1, interpretation_display_layer_v1]
        ↓
[Gemini (when CEO-approved and P4-2 active)]
  - Receives NarrativePayloadV1 or governed brief only
  - May polish presentation wording within claim boundaries
  - May not add findings, change confidence, or select new fragments
  - Constrained by validate_llm_output_v2
        ↓
[Frontend — render-only]
  - Consumes DTO
  - No medical inference
  - Journey v6 IA target
```

### Component responsibilities

| Component | Role | Owns |
|---|---|---|
| Asset library | Governed prose fragments | Retail explainers, pathway explainers, frame prose, modifier fragments, missing-marker caveats, resilience qualifiers |
| Selector rules | Layer B deterministic logic | Signal state → applicable fragment set; modifier eligibility check |
| Composer | Layer B NarrativePayloadV1 builder | Assembles section intents from selected fragments; enforces boundaries |
| NarrativePayloadV1 | B→C contract | Section intents, evidence boundaries, LLM constraints, missing-marker refs |
| NarrativeReportV1 | Layer C output | Compiled prose from governed brief |
| DTO | API contract | Carries all three output surfaces |
| Frontend | Presentation | Render-only; no inference |
| Gemini constraints | Deny-by-default; translate-only; no new findings; CEO-gated |

---

## 6. Prose asset taxonomy

The following taxonomy extends the existing asset set. All new asset types follow the same governed authoring and promotion path.

| Asset type | Description | Authored by | Scope |
|---|---|---|---|
| **Base biomarker explainer** | Non-personalised educational explanation of what the biomarker is and what it measures. Does not state patient conclusions. | MR LLM candidate → human review | Per biomarker_id; reused across all results for that marker |
| **Result-direction explainer** | Frame-level interpretation of a high/low/borderline signal for a specific marker within a specific clinical context. Activated by signal state. | MR LLM candidate → medical review | Per signal_id + direction |
| **System explainer** | Consumer-facing explanation of what a health system measures and why it matters at a whole-system level. | MR LLM candidate → review | Per domain system |
| **Subsystem explainer** | Explanation of a specific subsystem card (e.g. bio-oxygen carrying capacity, hormonal axis). | MR LLM candidate → review | Per subsystem_id |
| **Pathway explainer** | Explanation of a metabolic/clinical pathway and how it relates to the user's result pattern. | MR LLM candidate → review | Per pathway_id |
| **Signal/frame explainer** | The central interpretation for a specific signal frame: what the pattern means, why it arises, clinical relevance. Contains mechanism/biological pathway content. | MR LLM candidate → medical review | Per frame_id (from signal_library.yaml) |
| **Lifestyle modifier fragment** | Short additive caveats (1–2 sentences) clarifying how a lifestyle factor affects interpretation of a specific biomarker or signal. Not a full paragraph. | MR LLM candidate → review | Per modifier_id + biomarker_id/signal_id binding |
| **Medication modifier fragment** | Short additive caveats clarifying how a medication class affects interpretation. Does not diagnose or treat. | MR LLM candidate → medical review | Per modifier_id + drug class + affected marker |
| **Supplement modifier fragment** | Short additive caveats clarifying how a supplement may affect a biomarker value. Does not imply treatment. | MR LLM candidate → review | Per supplement_modifier_id + biomarker_id |
| **Missing-marker caveat** | Governed caveats explaining what a missing marker would add to the interpretation, without implying a conclusion from its absence. | MR LLM candidate → review | Per missing biomarker_id + context |
| **Weak-evidence fallback** | Governed fallback prose used when no specific frame prose applies, so the system can still produce something accurate and non-alarmist. | Human-authored | Per domain or general fallback |
| **Positive/resilience qualifier** | Short positive framing for a system that is within normal ranges and stable. Earns its place from governed signal state — not applied generically. | Human-authored with clinical input | Per system / per signal state combination |
| **Clinician-facing detail** | Technical clinical language for the clinician report sections. Governed by ClinicianReportV1 and blocked from LLM translation. | Governed separately; not MR LLM for direct clinical prose | Per clinician report section |
| **Retail/user-facing summary** | Consumer-accessible language summarising the key interpretation in plain English. Sources from governed base + frame prose; Gemini may polish when activated. | Compiled from base assets; Gemini polish later | Per user-facing narrative section |

---

## 7. Personalisation axes

| Axis | Status | When may it be used | Evidence required | Risk if misused |
|---|---|---|---|---|
| **Sex** | Restricted | Only when clinical interpretation (not just reference range) differs by sex — e.g. hormonal markers where sex defines normal physiology. Reference range stratification is Layer A; prose stratification is Layer B only when interpretation framing genuinely differs. | Clinical evidence that the biomarker interpretation (not merely the threshold) changes materially by sex. | False reassurance for one sex; unnecessary complexity; duplication without clinical benefit |
| **Age band** | Restricted | Only when age materially changes the clinical framing — e.g. FT3 low in menopausal vs reproductive-age context, eGFR in elderly. Not for general biomarker educational prose. | Clinical evidence that interpretation (not threshold) changes. | Same as sex: duplication without benefit; misleading framing for groups that don't require it |
| **Result direction** | Allowed | For all signals — high vs low vs borderline always warrant distinct interpretation framing. | Signal activation state (already governed by signal evaluators). | Low risk if signal activation is correct |
| **Lab-derived reference range position** | Allowed | For contextualising results within the user's lab-specific reference range. NarrativePayloadV1 supports this. | Lab-provided reference range on the input record. | Low risk; only a problem if lab ranges are unreliable (governance issue not prose issue) |
| **Biomarker pattern** | Allowed | For multi-marker clustering, phenotype detection, pattern-level interpretation. This is the core HealthIQ differentiator. | Signal activation + frame selection by Layer B. | Risk if pattern is overstated beyond what biomarker evidence supports; controlled by evidence boundaries |
| **System/subsystem** | Allowed | For system-level narrative. Existing pathway/system explainer architecture handles this. | Domain assembler and subsystem card wiring. | Low |
| **Lifestyle** | Allowed with guardrails | Only when there is a specific, medically documented relationship between the lifestyle factor and the biomarker or signal being explained. Alcohol/hepatic, smoking/inflammatory, exercise/creatinine, hydration/creatinine, diet/metabolic-lipid are the documented cases. | `modifier_effect` is not `no_interpretive_effect`; clinical evidence exists for the specific marker-lifestyle link. | Overstating lifestyle as cause; implying diagnosis from lifestyle data; recommending lifestyle changes (prohibited) |
| **Medication** | Allowed with guardrails | When a medication class is known to affect the biomarker value or interpretation. Must be additive differential context, not replacement of biomarker interpretation. | Intervention effects registry entry with clinical basis; `requires_medical_review: true` for safety-sensitive classes before runtime activation. | Patient believes medication is "protecting" them when result is still abnormal; failure to escalate when needed |
| **Supplement** | Allowed with guardrails | When a supplement is known to distort the biomarker value (creatine/creatinine; iron supplement/ferritin). Only explains possible cause; never recommends supplementation. | CONTEXT-MOD-1 catalogue entry; evidence role must be `measurement_distortion` or `supplement_confounder`. | False reassurance if supplement explanation substitutes for clinical concern |
| **Missing markers** | Allowed | Always appropriate to note what additional markers would improve confidence. Existing missing-marker caveat library handles this. | Missing marker detected at Layer B (absent from result set). | Low — only risk is over-dwelling on absences; controlled by maximum caveat count |
| **Phenotype/persona** | Restricted | Only when a governed phenotype (IDL record) is active and its classification meets the scientific threshold. Multiple classification types exist: phenotype, risk construct, syndrome/state, organ-pattern. | Active IDL record from Layer B with governed why_it_matters content. | Misclassifying a probabilistic risk construct as a certain phenotype; controlled by IDL governance |
| **Positive resilience language** | Restricted | Only when a signal is explicitly in a stable/normal state AND a governed positive qualifier exists for that state. Never inferred from absence of abnormality alone. | Active signal state is "normal" or "below threshold" AND positive qualifier asset is reviewed. | False reassurance; clinically dangerous if it masks a marginal result |
| **Clinician vs retail audience** | Allowed | Always separate: clinician sections blocked from Gemini translation; retail sections governed by retail safety boundaries. | Audience routing already in NarrativePayloadV1 section intents; clinician section LLM block post P2-4. | Cross-contamination (clinical language in retail; retail tone in clinician sections) |

---

## 8. Preventing combinatorial explosion

The following rules are mandatory. Violation triggers content review.

### Authoring guardrails

1. **Sex-specific prose only when clinically warranted.** Sex stratifies reference ranges at Layer A. Layer B prose is stratified by sex only when the clinical interpretation (not merely the threshold) genuinely differs. Default: one prose asset per marker, sex-neutral.

2. **Age-band prose only when clinically warranted.** Same logic as sex. Default: one prose asset, age-neutral educational framing.

3. **Lifestyle modifier fragments are additive caveats, not paragraph replacements.** A lifestyle modifier fragment must be 1–3 sentences. It appends to the base prose; it does not replace it.

4. **Medication modifier fragments are additive context only.** "You are taking a medication that can affect this marker" — not a rewrite of the interpretation.

5. **Supplement modifier fragments are measurement context only.** "Supplementation may contribute to this reading" — not clinical advice.

6. **Positive resilience wording requires a governing signal state.** A result in normal range is not sufficient grounds alone — the asset must be explicitly listed as applicable for that signal state.

7. **Do not create modifier fragments for relationships that have no clinical evidence.** The modifier catalogue `modifier_effect: no_interpretive_effect` entries (age, sex, sleep, stress, health goals) must not receive prose fragments.

8. **Maximum fragment count per final prose output.** Per biomarker section: 1 base + 1 direction/frame + max 2 modifier fragments + 1 missing-marker caveat = 5 fragments maximum. Enforce in the NarrativePayloadV1 builder.

### Naming and reuse rules

9. **Reuse existing governed prose before authoring new prose.** MR LLM must first check the existing registry/YAML for any asset that covers the intended content. Only create new assets when no existing asset applies or when existing assets are classified unsafe, obsolete, or incompatible.

10. **Asset ID naming convention** follows the existing pattern: `{domain}_{signal/marker}_{direction}_{audience}_v{n}`. Example: `renal_creatinine_high_consumer_v1`. IDs are immutable once promoted to runtime.

11. **Do not duplicate educational content across asset types.** Base biomarker explainers are educational (what the marker is). Frame/signal prose is interpretive (what this result means). Do not repeat educational content in the frame prose.

### Suppression rules

12. **Gemini must never infer a modifier relationship.** If the modifier catalogue does not list a modifier-biomarker relationship, Gemini may not create one from NLP pattern matching.

13. **Suppress modifier fragments when the modifier effect would duplicate the base prose.** If the base prose already says "elevated creatinine may reflect kidney stress," a NSAID modifier fragment should not simply repeat this — it should add the specific drug context.

14. **Do not suppress positive resilience wording from the clinician report.** Positive findings are clinically relevant. The restriction applies to retail-facing prose only where retail framing could create false reassurance.

---

## 9. MR research asset model

The Medical Research LLM may draft candidate prose assets only within a defined schema. The schema must enforce the following fields before any draft is accepted as a candidate.

### Required fields

| Field | Type | Purpose |
|---|---|---|
| `asset_id` | String | Unique kebab-case ID following naming convention above |
| `asset_type` | Enum | One of: `base_biomarker_explainer`, `result_direction_explainer`, `system_explainer`, `subsystem_explainer`, `pathway_explainer`, `signal_frame_explainer`, `lifestyle_modifier_fragment`, `medication_modifier_fragment`, `supplement_modifier_fragment`, `missing_marker_caveat`, `weak_evidence_fallback`, `positive_resilience_qualifier`, `clinician_detail` |
| `audience` | Enum | `retail`, `clinician`, `both` |
| `scope.biomarker_ids` | List\[str\] | Which biomarker_ids this asset applies to (or empty for system-level assets) |
| `scope.signal_ids` | List\[str\] | Which signal_ids activate this asset (or empty for base explainers) |
| `scope.direction` | Enum\|null | `high`, `low`, `borderline`, `normal`, `null` (null for educational assets) |
| `scope.system` | String\|null | Health system this asset belongs to, if system-level |
| `evidence_refs` | List\[obj\] | At least one: `{source, year, finding}`. No evidence = REJECT. |
| `evidence_strength` | Enum | `established`, `probable`, `emerging` |
| `safety_boundaries` | List\[str\] | Explicit list of what this asset MUST NOT claim |
| `review_status` | Enum | `CANDIDATE` on creation; `APPROVED` after medical review; `REJECTED`; `DEPRECATED` |
| `destination_mapping` | Obj | `{asset_type, registry_path, section_intent_id}` — where this asset routes at runtime |
| `prose_content` | Obj | `{retail: str|null, clinician: str|null}` |
| `max_word_count` | Integer | Base explainers ≤ 120 words; modifier fragments ≤ 60 words; pathway explainers ≤ 200 words |
| `authored_by` | Enum | `MR_LLM_CANDIDATE`, `HUMAN`, `HUMAN_EDITED_FROM_LLM` |
| `authored_utc` | ISO datetime | |

### Evidence requirements

- Base biomarker explainers: no clinical evidence threshold required (educational), but must not make clinical claims
- Signal/frame explainers: established or probable evidence for the interpretation
- Modifier fragments: at least one citation supporting the modifier-biomarker relationship
- Positive resilience qualifiers: clinical evidence that the signal state is genuinely stable, not merely normal-range-adjacent

### Safety boundaries

Mandatory safety boundaries for all asset types:

- Must not diagnose or imply diagnosis
- Must not name a specific disease unless the framing is purely educational (e.g. "MASLD is a condition where…" not "You may have MASLD")
- Must not recommend specific treatments, dosage changes, or medication decisions
- Must not recommend specific supplements
- Must not imply causality beyond what the evidence supports
- Must not create symptom associations not present in the governing PSI or frame logic

### Promotion path

```
MR LLM draft (review_status: CANDIDATE)
    → human content review (medical/clinical)
    → review_status: APPROVED
    → compile into target registry/YAML with hash
    → validate against schema
    → runtime load
```

### Illustrative example

```yaml
asset_id: hepatic_alt_high_consumer_metabolic_context_v1
asset_type: signal_frame_explainer
audience: retail
scope:
  biomarker_ids: [alt]
  signal_ids: [signal_hepatic_alt_context]
  direction: high
  system: hepatic
evidence_refs:
  - source: "AASLD Practice Guidance 2023"
    year: 2023
    finding: "ALT >40 U/L in the absence of other causes most commonly reflects hepatocellular injury; metabolic-steatotic pattern is the most prevalent aetiology in Western populations"
evidence_strength: established
safety_boundaries:
  - Must not state MASLD diagnosis
  - Must not imply alcohol is the cause without alcohol modifier fragment being present
  - Must not recommend liver biopsy or referral directly — next-step routing is from Layer B safety_class
review_status: CANDIDATE
destination_mapping:
  asset_type: signal_frame_explainer
  registry_path: knowledge_bus/packages/pkg_kb52c_alt_high_hepatocellular_injury_pattern/signal_library.yaml
  section_intent_id: primary_finding
prose_content:
  retail: "Your ALT enzyme is elevated, which typically reflects the liver working harder than usual. In many cases this pattern arises from metabolic loading — excess weight, dietary fat, or metabolic strain. Understanding what's driving it depends on the wider picture."
  clinician: null
max_word_count: 60
authored_by: MR_LLM_CANDIDATE
authored_utc: "2026-06-29T00:00:00Z"
```

---

## 10. Runtime compiled asset model

### Why MR draft assets must not be directly consumed in production

1. MR LLM prose has not been medically reviewed. The review_status CANDIDATE means precisely this.
2. MR LLM may invent plausible-sounding but clinically incorrect claims — this is its known failure mode.
3. The safety boundaries field is a governance declaration, not a runtime enforcement mechanism.
4. Prose consistency requires human editorial review across assets; MR LLM will produce inconsistent tone and scope without it.
5. The existing PSI promotion protocol (Pass 3 → staged → production) is the correct model. Prose must follow the same discipline.

### Promotion protocol for prose assets

1. MR LLM authors draft with `review_status: CANDIDATE`
2. Medical/clinical reviewer reads the prose against the evidence_refs and safety_boundaries
3. If approved: `review_status: APPROVED`; if rejected: `review_status: REJECTED` with reason
4. Approved asset is compiled into its target registry/YAML file (retail registry, pathway YAML, signal_library.yaml, etc.)
5. SHA-256 hash computed and stored in compile manifest
6. Validation script checks hash integrity before runtime load
7. Runtime loads only APPROVED, hash-validated assets

### Where validation occurs

- Schema validation: at draft acceptance (before medical review)
- Safety boundary check: at medical review (human) and optionally LLM-assisted at draft time
- Hash integrity: at runtime load (existing compile manifest pattern)
- Content gate: medical reviewer, not automated

### Import/compile route

The existing compile manifest pattern from the PSI promotion work (P1-13/P1-14) is the correct model. Prose assets are not loaded raw from MR draft files. They are compiled into their registry/YAML files with:
- Byte-identical copies from approved drafts
- Hash integrity in compile manifest
- No runtime reads from draft directories

---

## 11. Composer decision model

The composer is Layer B's NarrativePayloadV1 builder, not a separate new component. The existing `narrative_payload_builder_v1.py` is the right location for this logic.

### Eligibility

A prose fragment is eligible for inclusion in the NarrativePayloadV1 if:
1. Its `scope.biomarker_ids` or `scope.signal_ids` include the current biomarker/signal
2. Its `scope.direction` matches the current signal state (or is null for direction-agnostic assets)
3. Its `review_status` is `APPROVED`
4. Its hash has been verified against the compile manifest
5. It does not violate any evidence boundary declared in the relevant `NarrativeSectionIntentV1`

### Ranking

When multiple fragments are eligible for a section:
1. Signal/frame explainer outranks base biomarker explainer for interpretation sections (base explainer is supplementary educational context)
2. Pathway explainer outranks generic system prose
3. More specific modifier fragment (single biomarker scope) outranks class-level modifier fragment
4. Positive resilience qualifier is added only after all other eligible fragments are resolved

### Suppression

Suppress a fragment when:
- The section already has content that makes the fragment redundant (duplicate suppression)
- The modifier effect would contradict the base interpretation (conflict suppression)
- The fragment's audience does not match the target section audience
- The maximum fragment count per section would be exceeded (clutter suppression)

### Conflict resolution

If two modifier fragments contradict each other (e.g. medication lowers LDL, but result shows high LDL), do not suppress either — include both with a governing "despite" connector. The governed prose for this case must be authored as a specific conflict-resolution fragment, not improvised by Gemini.

If a positive resilience qualifier conflicts with a modifier fragment (e.g. system appears stable but a safety modifier is present), suppress the resilience qualifier and keep the modifier.

### Missing-marker handling

If a marker is absent and a missing-marker caveat exists for it in context:
1. Add caveat ref to `NarrativePayloadV1.missing_marker_caution_refs`
2. Include in the appropriate section intent as a confidence limiter
3. Do not infer what the result would have been

### Uncertainty handling

`NarrativePayloadV1.required_caveats` must always include a confidence caveat when confidence is Moderate or Limited. The caveat is a governed string from the confidence caveat library (existing infrastructure in ClinicianReportV1 and domain narrative contract), not Gemini-generated.

### Positive/resilience wording control

Positive wording is only added when:
1. The signal_state for the relevant system is explicitly "normal" or "below_threshold"
2. A specific positive resilience qualifier asset exists for this signal state
3. No safety modifier is active that would make positive wording inappropriate

### Maximum narrative length / clutter control

- Per biomarker section: max 5 fragments (base + direction + 2 modifiers + 1 caveat)
- Per system section: max 3 fragments (system prose + pathway + 1 modifier or caveat)
- Per NarrativeReportV1: max total prose budget (to be determined in P2-FRAME-ROUTING design sprint; recommend 600–900 words for retail-facing output)
- Enforce as hard limits in the NarrativePayloadV1 builder

---

## 12. Gemini role

### What Gemini may do (when CEO-approved and P4-2 active)

- Receive `NarrativePayloadV1` (or a curated brief derived from it) as sole input
- Polish wording, flow, and readability within the claim boundaries declared in the payload
- Improve connective tissue between governed sections
- Adapt tone (e.g. more empathetic, less clinical) within the retail audience constraints
- Translate governed section intents into more natural-sounding prose
- Operate only on `may_translate_section_ids` allowlist sections

### What Gemini must never do

- Add findings not present in the governed brief
- Change confidence levels or severity
- Activate or suppress signals
- Infer a modifier relationship not present in the payload
- Write unsupported lifestyle/medication/supplement links
- Rewrite clinician-reserved sections (blocked by `may_translate_section_ids` — clinician sections are always denied)
- Override evidence boundaries declared in the section intents
- Claim diagnostic conclusions
- Create treatment, dosage, or medication advice
- Rename or reclassify a finding

### Deny-by-default

`future_llm_may_rewrite=False` is the default for all sections (P2-4 hardening). A section must be explicitly added to the `may_translate_section_ids` allowlist to permit Gemini translation. This allowlist is authored per consumer surface by the builder, not by Gemini.

### CEO-gated activation

Production Gemini narrative activation (P4-2) requires explicit CEO approval. The design sprint (P4-1) does not activate production Gemini. The `future_llm_may_rewrite` opt-in on consumer surfaces is scoped in P4-1 and only instantiated in P4-2 under CEO approval.

---

## 13. Frontend / UAT implications

### Architecture smoke UAT (can run now)

Purpose: Verify that the prose-to-UX rendering path functions end-to-end. Content quality is not the criterion.

Requirements:
- Any retail explainer entries in the registry (40 exist)
- NarrativePayloadV1 built for a test result (P2-4 hardened contract)
- NarrativeReportV1 compiled and carried on DTO
- Frontend rendering all three DTO surfaces

Status: Achievable today. This validates the architecture, not the product.

### Product-quality UAT (not yet achievable)

Purpose: Verify that a real user can read the results, understand their body, and trust the explanation.

Requirements:
- Retail explainer coverage ≥ 70/79 (currently 40)
- Frame-level routing active (P2-FRAME-ROUTING-ARCHITECTURE-1, not yet done)
- At least two activated modifier classes (lifestyle and/or medication) with governed fragment prose
- Pathway prose for all six launch-core domains (hepatic and metabolic pathways still absent)
- Missing-marker caveats for full Wave 1 panel set (currently 6; need ~25–30)
- Positive/resilience qualifier library bootstrapped (not yet started)
- Gemini narrative path active for prose coherence improvement (P4-2 gate)
- Journey v6 IA implemented (Phase 5 frontend work)

Status: Not achievable until the above are delivered. Do not schedule product-quality UAT until at minimum: frame routing, modifier activation, full retail coverage, and at least one Gemini pilot are delivered.

### Beta cohort UAT (beyond current programme phase)

Purpose: Real external users evaluate the product.

Requirements:
- All product-quality UAT requirements met
- Security hygiene gate passed (post beta-recheck blockers cleared)
- CEO approval for external cohort
- Six-domain results page with Journey v6 IA
- Full modifier library active for at least high-priority classes
- Gemini pilot evaluated and passed quality threshold

Status: Requires multiple sprints beyond the current P4-1 position.

---

## 14. Recommended next work package

### P3-PROSE-DEPTH-1 — Prose Library Depth and Modifier Activation Sprint

**Or continue with P4-1 if CEO approval is received first.**

The programme sequencing choice is:
- If CEO approves P4-1: proceed with P4-1 Gemini activation design as recommended by PROSE-INVENTORY-1. This unblocks the Gemini path, which is the prerequisite for product-quality UAT.
- If CEO approval is delayed: P3-PROSE-DEPTH-1 is the correct parallel work. It does not block P4-1 but increases prose quality before the Gemini design sprint.

For P3-PROSE-DEPTH-1 specifically:

**Name:** P3-PROSE-DEPTH-1 — Prose Library Depth and Modifier Schema Sprint

**Risk:** STANDARD

**Change type:** CONTENT

**Product output:**
- Prose asset schema definition (YAML schema for the MR candidate asset model defined in §9 of this review)
- MR LLM candidate prose batch for hepatic and metabolic pathway explainers (the two missing launch-core pathways)
- MR LLM candidate prose for the top-10 missing retail biomarker explainers by launch-panel frequency
- Positive resilience qualifier draft for at least one system (cardiovascular or metabolic — the two systems with most complete IDL content)
- Modifier prose fragment authoring template for lifestyle modifier classes (alcohol/hepatic, smoking/inflammatory) — governance only, no runtime activation

**Primary agent:** GPT (SOP authoring) → Claude (Stage D hardening + audit) → human review → Cursor (implementation if CONTENT scope touches registry files)

**Why before P4-1:** P3-PROSE-DEPTH-1 is not a prerequisite for P4-1 design. Run them sequentially if CEO approval for P4-1 is pending; run P3 in parallel if CEO approval arrives before P3 completes.

**Why before P5 (UX):** Product-quality frontend UAT needs prose depth that P3 begins to provide. Do not invest Phase 5 frontend sprint work into a skeleton content layer.

**STOP gates:**
- No modifier runtime binding in this sprint (governance schema only)
- No Intelligence Core file touches
- No Gemini activation
- No new clinical inference rules — content only
- All new prose assets go to `review_status: CANDIDATE` until medical review

---

## 15. What not to do

1. **Do not build a new composition engine.** The existing NarrativePayloadV1 builder + Layer C compiler is the composition engine. Extending it is a sprint-sized task, not an architecture redesign.

2. **Do not create sex-specific or age-specific prose variants as a default authoring practice.** These axes are restricted. Default to sex-neutral, age-neutral educational framing.

3. **Do not activate context modifiers en masse in one sprint.** Each modifier class binding requires a governed prose fragment library and a Stage D hardening sprint per class. Batch: lifestyle first, then high-impact medication classes, then supplements.

4. **Do not use Gemini to "fill in" missing prose coverage.** The prompt template for Gemini receives `NarrativePayloadV1`, not raw biomarker data. Gemini cannot expand the prose library — only human-authored + MR LLM candidate + medical-reviewed assets are legitimate.

5. **Do not schedule product-quality frontend UAT before frame routing, modifier activation, and Gemini pilot.** Architecture smoke UAT is valid now. Product UAT with insufficient prose quality will mislead the assessment.

6. **Do not treat the PROSE-INVENTORY-1 verdict (PROCEED_TO_P4_1) as a reason to skip prose depth work.** PROSE-INVENTORY-1 correctly noted that retail at 40/79 is not blocking P4-1 *design*. It does not say prose depth is sufficient for product-quality UAT.

7. **Do not deploy MR LLM candidate assets directly to production.** Every candidate must clear medical review and hash-verify through the compile manifest.

8. **Do not create positive resilience prose "generically" for all systems.** It is earned by signal state. Generic positive framing for users who have no abnormal findings is bland and dilutes the product differentiator.

9. **Do not create a parallel prose authoring system outside the Knowledge Bus.** All prose assets must be trackable, versioned, hashed, and governed within the existing KB promotion infrastructure.

10. **Do not confuse the product differentiator.** HealthIQ's differentiator is governed reasoning, not beautiful prose. Gemini can improve the wording; it cannot improve the analytical truth behind it. The prose library matters because it carries the analytical truth clearly — it is not the differentiator itself.

---

## 16. Open questions and deferred decisions

### Requiring medical review before proceeding

- **Modifier binding rules per modifier class:** The context_modifier_catalogue_draft_v1.yaml is a governance catalogue, not a binding specification. Before any modifier class is runtime-activated, a medical reviewer must confirm the binding rules for that class (when to add the fragment, what the fragment is allowed to say, and what it is prohibited from saying).
- **Positive resilience qualifier authoring:** Which signal states genuinely warrant positive framing? This requires clinical input — a blank "all normal" qualifier is medically bland and potentially misleading.
- **Sex-specific prose eligibility list:** Which specific biomarkers/signals require sex-specific interpretation framing beyond reference range stratification?

### Requiring B1 blocker check before SOP authoring

- **P2-FRAME-ROUTING-ARCHITECTURE-1:** The frame-level routing sprint is deferred and requires a B2 advisory (per PROSE-INVENTORY-1 and BUILD_DELIVERABLE_REGISTER) before its SOP can be authored. The architecture of signal-to-frame discrimination at runtime is non-trivial.
- **Lifestyle modifier engine runtime extent:** The `backend/core/analytics/lifestyle_modifier_engine.py` exists. Its current runtime binding extent is unknown from documentation alone. A B1B blocker check is needed before a modifier binding sprint can be scoped.
- **Modifier prose fragment format in NarrativePayloadV1:** How exactly should context modifier fragments appear in the NarrativePayloadV1 section intents? The existing `NarrativeSectionIntentV1` and `NarrativeEvidenceBoundaryV1` structures may need extension. This is a Stage D hardening question, not a B2 question.

### Requiring B2 or strategic decision

- **P2-FRAME-ROUTING-ARCHITECTURE-1 advisory:** Already flagged as requiring B2 advisory per programme register.
- **Full Wave 1 prose completion scope:** Should the programme commit to 79/79 retail coverage as a blocking gate for beta, or is a prioritised 60/79 based on launch-panel frequency acceptable? This is a CEO/programme decision.

### Requiring CEO decision

- **P4-1 Gemini activation design:** CEO approval gate preserved. No progress until explicitly approved.
- **P4-2 controlled Gemini pilot:** Separate approval gate from P4-1.
- **Beta cohort readiness:** CEO approval required for any external user access.
- **Positive resilience language in beta:** Some users will have all-normal results. What should HealthIQ say to them? This is partly a clinical decision and partly a product/CEO decision about tone.

### Requiring frontend design decision

- **Journey v6 IA alignment:** Phase 5 frontend work (P5-1, P5-2 in programme). How does the prose library depth map to progressive disclosure in Journey v6? Specifically: how many modifier fragments are visible by default vs expandable? Journey v6 UX decisions should guide this but the mapping has not been formalised.
- **Retail vs clinician audience routing in the frontend:** The DTO carries both surfaces. How the frontend surfaces each depends on Journey v6 IA decisions.

---

## Single recommended next action

**If CEO approval for P4-1 is available:** Author and harden the P4-1 SOP (Gemini Activation Design + Test Harness). This unblocks the Gemini narrative path, which is the prerequisite for product-quality UAT. Prose depth work (P3-PROSE-DEPTH-1) runs in parallel.

**If CEO approval for P4-1 is not yet available:** Author P3-PROSE-DEPTH-1 starting with the prose asset schema (§9 of this review), then MR LLM candidate prose batch for the two missing launch-core pathway explainers (hepatic, metabolic). This is meaningful programme progress that does not require CEO approval and does not activate any governed boundary.

In either case, do not start building a new composition engine. The architecture is correct. The work is content depth and modifier activation.

---

*End of DYNAMIC-PROSE-ARCH-1 — 2026-06-29.*
*This document is a B2 strategic architecture review only. It does not authorise implementation, modify runtime files, or constitute a work package SOP.*
*Implementation requires GPT-authored work packages, Claude Stage D hardening, and kernel execution per Automation Bus SOP v1.3.1.*
