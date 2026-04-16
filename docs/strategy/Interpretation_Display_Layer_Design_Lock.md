# HealthIQ — Interpretation Display Layer (IDL) Design Lock

**Status:** Proposed design lock (approval-ready)
**Scope:** Governs the contract, classification, naming, and frontend rendering model for Section 5 — “Patterns across your body”.
**Inputs used (do not re-derive here):**
- `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` (Section 5, Phase 2 gate)
- `docs/strategy/Phenotype_Terminology_Proposal.md`
- `docs/strategy/healthiq_future_screening_priorities.md`
- `docs/investigations/FE_R7_SECTION_5_PATTERN_LAYER_EXISTENCE_CHECK.md` (existence-check conclusion: display layer must be built before Section 5 ships)

This document is a **design lock**. It is not a sprint prompt, it is not code, and it does not re-open research already completed.

---

## 1. Executive summary

1. Build a governed **Interpretation Display Layer (IDL)** as a new **backend contract** that sits on top of the existing 9 phenotype entities. The IDL is the **sole authority** the Section 5 UI reads from.
2. The IDL carries a strict **`scientific_class` enum** — `phenotype`, `risk_construct`, `organ_pattern`, `syndrome_state` — and a strict **`frontend_allowed_term`** enum that controls whether the word **“phenotype”** is permitted on the retail surface per entity.
3. Of the current 9 entities, **exactly one** is approved to carry the word **“phenotype”** on the retail UI (`ph_metabolic_early_ir_v1`). All others must ship with clinical or plain-English labels only. Internal IDs keep their `ph_…` prefix; that is an engineering convention, not a product claim.
4. Section 5 cards must be driven by 5 required IDL fields (label, subtitle, why-it-matters, severity/state, supporting summary) plus 3 required governance fields (scientific class, frontend term permission, enabled flag). Everything else is optional.
5. The next implementation sprint is a **backend + content** sprint (working name: **BE-IDL-1**) that creates the IDL contract, authors the 9 display records, and exposes them on the analysis result payload. A frontend Section 5 sprint (**FE-R8**) is **blocked** on BE-IDL-1.

---

## 2. Why this layer is needed

The existing cluster/system layer was built for engine grouping, not user-facing interpretation. It ships `cluster_id`, `name`, `category`, `severity`, `description`, `biomarkers`, and an optional educational explainer. It does **not** carry:

- a governed **scientific class** (phenotype vs risk construct vs organ pattern vs syndrome state),
- a **separate clinical display label** distinct from internal naming,
- a **retail plain-English label**,
- a disciplined **why-it-matters** field,
- a **frontend term permission** gate (can this row say “phenotype” on retail or not),
- a **display ordering / enablement** control.

Without those fields:

- Section 5 either **invents** taxonomy in component code (UX/medical risk) or falls back to generic labels (“Metabolic Health”) that collapse the value of the middle layer.
- Naming will drift across product, commercial, and technical surfaces the moment we add a tenth entity.
- Commercially, we cannot align new entities to the screening priorities (dysglycaemia, ASCVD, CKD, MASLD, integrated metabolic, iron deficiency) without a contract that enforces what each entity is.

The IDL exists to remove these ambiguities before Section 5 ships, and to make the future pattern layer cleanly extensible.

---

## 3. Interpretation classification model

Four classes only. No overlap. Each entity picks **exactly one**.

### 3.1 `phenotype`

**Definition.** A biologically recognisable, multi-marker biological pattern with scientific standing in metabolic / cardiometabolic literature (e.g. insulin-resistant phenotype).

**Use when:**
- there is a clearly named biological pattern in the literature,
- it is defined by a multi-marker signature (not a single organ lab),
- the pattern is useful as an interpretive identity (“this is a recognisable state of the body”),
- the retail framing is strategically aligned with HealthIQ’s phenotype positioning.

**Do not use when:**
- the construct is primarily an **actuarial / risk** frame (use `risk_construct`),
- it describes a **single organ system** (use `organ_pattern`),
- it describes a **clinical state** best named directly (use `syndrome_state`, e.g. iron deficiency).

**Retail UI allowed?** Yes, paired with a plain-English subtitle. Never bare.

**May the word “phenotype” appear on the frontend?** Yes (retail label may end in “Phenotype”).

### 3.2 `risk_construct`

**Definition.** An actuarial / prognostic frame: the chance of future disease events based on a signature of markers, not a present-tense biological identity.

**Use when:**
- the entity answers “how much risk is accumulating” rather than “what state is the body in,”
- the construct lives natively in risk/stratification language (e.g. atherogenic burden, ASCVD risk, cardiometabolic inflammatory risk).

**Do not use when:**
- the underlying mechanism is cleanly localised to one organ (use `organ_pattern`),
- there is a well-established clinical state to name directly (use `syndrome_state`).

**Retail UI allowed?** Yes.

**May the word “phenotype” appear on the frontend?** **No.** These ship as “risk,” “burden,” or “stratification.”

### 3.3 `organ_pattern`

**Definition.** A pattern of signals localised to (or best explained by) a single organ or axis — kidney, liver, thyroid, etc.

**Use when:**
- the signature is dominated by one organ system,
- the clinical convention is organ-specific (e.g. kidney stress, thyroid-linked metabolic pattern).

**Do not use when:**
- the pattern is multi-system enough that organ framing is reductive (use `phenotype` or `risk_construct`).

**Retail UI allowed?** Yes.

**May the word “phenotype” appear on the frontend?** **No.** Organ patterns ship as “pattern” / “stress” / “strain.”

### 3.4 `syndrome_state`

**Definition.** A clinically established state with a canonical name — use the canonical name directly.

**Use when:**
- the condition has a stable, medically legible label (iron deficiency, iron overload, dysglycaemia, prediabetes, hypothyroidism-adjacent states),
- renaming it would obscure what it actually is.

**Do not use when:**
- the entity is better served as a risk frame or a multi-marker phenotype.

**Retail UI allowed?** Yes, using the clinical state name plus a plain-English subtitle.

**May the word “phenotype” appear on the frontend?** **No.** These ship as the clinical state.

### 3.5 Rule about overlap

If an entity plausibly fits two classes, pick the class that **best matches the dominant user action** (what should they do with this card?):

- Action = *“understand I have a recognisable biological identity”* → `phenotype`.
- Action = *“understand my risk trajectory”* → `risk_construct`.
- Action = *“focus on a specific organ / axis”* → `organ_pattern`.
- Action = *“recognise an established clinical state”* → `syndrome_state`.

No entity may carry two classes.

---

## 4. Current 9-entity mapping table

| internal_id | scientific_class | clinical_display_label | retail_display_label | subtitle (plain-English) | why_it_matters (≤ 1 sentence) | frontend_allowed_term | rationale |
|---|---|---|---|---|---|---|---|
| `ph_metabolic_early_ir_v1` | `phenotype` | Early insulin-resistance phenotype | Insulin Resistance Phenotype | A pattern suggesting early impaired sugar and lipid handling | Left unaddressed, early insulin resistance progresses toward prediabetes and cardiometabolic risk. | `phenotype_allowed` | Flagship phenotype case in the terminology proposal; multi-marker, biologically recognisable, retail-ready. |
| `ph_hba1c_metabolic_stress_v1` | `syndrome_state` | Dysglycaemic metabolic stress | Blood Sugar Stress State | A pattern suggesting sustained blood-sugar strain on the body | Sustained glycaemic strain raises long-term metabolic and vascular risk. | `clinical_only` | Dysglycaemia is best named as a syndrome-state per screening priorities; phenotype framing weakens medical legibility. |
| `ph_vascular_hcy_inflammation_v1` | `risk_construct` | Vascular inflammation risk (homocysteine-linked) | Vascular Inflammation Risk | A pattern combining inflammation and homocysteine signals associated with vascular risk | Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. | `clinical_only` | Inflammation + Hcy is an actuarial modifier of vascular risk, not a recognisable phenotype identity. |
| `ph_hepatic_alt_inflammatory_v1` | `organ_pattern` | Hepatic inflammatory pattern | Liver Stress Pattern | A pattern suggesting metabolic or inflammatory strain in the liver | Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored. | `clinical_only` | Single-organ (liver) focus; MASLD-adjacent routing pattern, not a phenotype. |
| `ph_renal_stress_v1` | `organ_pattern` | Renal stress pattern | Kidney Stress Pattern | A pattern suggesting the kidneys are under strain in this snapshot | Kidney strain is common, expensive, and highly actionable when caught early. | `clinical_only` | Clean organ localisation; aligns to CKD screening lane without overclaiming disease. |
| `ph_thyroid_lipid_disturbance_v1` | `organ_pattern` | Thyroid-linked lipid disturbance pattern | Thyroid–Lipid Pattern | A pattern where thyroid-axis signals are accompanied by lipid disturbance | Thyroid axis changes can drive lipid disturbance and warrant joint review. | `clinical_only` | Thyroid is best framed as an organ-pattern per screening priorities; phenotype framing inappropriate. |
| `ph_tsh_axis_metabolic_v1` | `organ_pattern` | Thyroid-axis metabolic pattern | Thyroid Axis Pattern | A pattern suggesting the thyroid axis is influencing metabolic signals | Thyroid axis shifts can quietly reshape metabolic reads and are worth monitoring. | `clinical_only` | Same organ-pattern rationale; distinct entity from thyroid-lipid, but same class. |
| `ph_iron_deficiency_inflammation_v1` | `syndrome_state` | Iron-deficient state with inflammation context | Iron Deficiency (with inflammation) | A pattern suggesting iron deficiency, read in the context of inflammation | Iron deficiency is highly actionable; inflammation can mask it and must be read together. | `clinical_only` | Iron deficiency is a canonical clinical state; phenotype language weakens it. |
| `ph_iron_overload_v1` | `syndrome_state` | Iron-overload state | Iron Overload | A pattern suggesting excess iron stores that warrant clinical review | Iron overload has real downstream organ risk and is worth catching early. | `clinical_only` | Clinical state; phenotype allowed only in narrow heritable contexts, not on retail UI. |

**Summary of phenotype term permission across the 9:**
- `phenotype_allowed`: **1** (`ph_metabolic_early_ir_v1`).
- `clinical_only`: **8**.

This is intentional. It prevents phenotype overreach while still anchoring the word to its strongest commercial example.

---

## 5. Recommended display contract fields

The IDL is an **ordered set of records** on the analysis result. Exact field names below are the governance contract; engineering is free to mirror casing conventions of the DTO.

| field | requirement | notes |
|---|---|---|
| `internal_id` | **required** | The current `ph_…` id. Never rendered on retail UI; allowed in clinician export and diagnostics. |
| `scientific_class` | **required** | Enum: `phenotype` \| `risk_construct` \| `organ_pattern` \| `syndrome_state`. Drives governance, not UI copy. |
| `clinical_display_label` | **required** | Label used in clinician report, PDF, and B2B surfaces. May use technical terms. |
| `retail_display_label` | **required** | Label used on Section 5 cards for consumer UI. Must be plain enough to read without training. |
| `subtitle` | **required** | One short plain-English line. Mandatory for every entity — there are no bare labels on retail UI. |
| `why_it_matters` | **required** | One-sentence rationale for the user. No lifestyle advice, no diagnosis claim. |
| `severity_state` | **required** | Enum-driven state for the card (e.g. `watch` / `monitor` / `attention` / `strong_signal`). The engine-side severity/score feeds this but is normalised here. |
| `supporting_biomarkers_summary` | **required** | Short human-readable summary string of 2–4 top markers. Not the full list. Not raw IDs. |
| `supporting_systems_summary` | optional | Short string naming system groups this pattern sits near (e.g. “metabolic, hepatic”). Nice-to-have for cross-linking, not necessary for every card. |
| `user_safe_description` | optional | Longer paragraph for an expand state. If absent, expand state simply hides. |
| `frontend_allowed_term` | **required** | Enum: `phenotype_allowed` \| `clinical_only`. Hard gate on whether the UI may render the word “phenotype” for this record. |
| `future_commercial_domain` | optional (governance-useful) | Enum mapping to the commercial screening lanes (§8). Not rendered on retail UI. Used for product analytics and roadmap alignment. |
| `display_order_priority` | **required** | Integer used for deterministic card ordering when multiple entities qualify. Ties broken by `scientific_class` order then `internal_id`. |
| `enabled_for_frontend` | **required** | Boolean. A record can exist in the contract but be held back from retail UI (e.g. during phased rollout or while copy is under review). |
| `display_caveat` | optional | Short caveat string shown under the card (e.g. “read alongside your headline pattern”) when editorial deems it needed. |
| `confidence_display` | optional (usually **not**) | Raw engine confidence is **not** rendered. This field exists only if we ever want to expose a coarse confidence band; default behaviour is to omit. |

**Not included in the IDL:**
- Raw biomarker IDs. Those live on biomarker cards, not pattern cards.
- Engine confidence numbers. Those live in governance/diagnostics.
- Recommendations / action copy. Action sits in Section 8 (Phase 2 / Phase 3), not in Section 5 cards.

**Design discipline.** We intentionally keep the contract small. Every field above either (a) shows on the card, (b) governs whether/how the card shows, or (c) drives ordering. Nothing else.

---

## 6. Frontend rendering requirements for Section 5

Section 5 is a **gallery of pattern cards**, rendered only when at least one IDL record has `enabled_for_frontend = true` and passes a simple per-card render gate.

### 6.1 A pattern card **must** show

1. **Retail display label** (`retail_display_label`).
2. **Subtitle** (`subtitle`) — plain-English line under the label. Never omitted.
3. **Severity/state** — a visually calm chip or badge driven by `severity_state`.
4. **Supporting summary** — one line drawn from `supporting_biomarkers_summary` (optionally plus `supporting_systems_summary` if present).
5. **Why it matters** — one-sentence line drawn from `why_it_matters`.

### 6.2 A pattern card **may** show (nice-to-have)

6. Expand affordance revealing `user_safe_description`, only when that field is populated. No expand control when empty.
7. A `display_caveat` line under the card, only when populated.

### 6.3 A pattern card **must not** show

- `internal_id` (or any `ph_…` value).
- Raw engine confidence numbers.
- Biomarker reference ranges or values (those belong to biomarker cards).
- The word **“phenotype”** unless the record’s `frontend_allowed_term` is `phenotype_allowed`.
- Any claim of diagnosis.
- Any lifestyle prescription.

### 6.4 Section-level behaviour

- **Section render gate.** Section 5 renders only if at least one IDL record has `enabled_for_frontend = true`. Otherwise the section is omitted cleanly (no heading, no empty state).
- **Card limit.** Maximum of **5 cards** visible by default. If more than 5 qualify, select by `display_order_priority` ascending, tie-break `scientific_class` in the order `phenotype → risk_construct → organ_pattern → syndrome_state`, then `internal_id`. The rest are available on expand or in the clinician view — not dumped onto the retail page.
- **Placement.** Section 5 sits between Section 4 (“Why this lead won”) and the biomarker-heavy sections, as defined in the Results Journey v6. The existing FE-R5 component (“How to understand your results”) is an **explainer bridge**, not Section 5; it stays and is renamed in the UI context once Section 5 ships, to avoid two things called Section 5.

### 6.5 Clinician / B2B surface

- Clinician PDFs and exports may use `clinical_display_label`, `scientific_class`, `internal_id`, and (if ever exposed) `confidence_display`. These views do not use `retail_display_label`.

---

## 7. Naming rules

Operational, not philosophical.

1. **Every card has a subtitle.** No exceptions. If we cannot write a one-line plain-English subtitle for a record, that record does not ship to retail.
2. **“Phenotype” is a gated term.** It may only appear on retail when `frontend_allowed_term = phenotype_allowed`. Internal IDs using the `ph_` prefix are an engineering convention and do **not** grant retail permission.
3. **Clinical labels may use technical language.** Retail labels must not. There are two labels precisely so we stop arguing about which surface a word is for.
4. **No generic-bucket labels on Section 5 cards.** “Metabolic Health,” “Organ Health,” “Heart Health,” etc. are banned as card labels. They are system-group language and they collapse the middle layer. System-group language is fine for `supporting_systems_summary`.
5. **No risk-as-phenotype.** Risk constructs (`risk_construct`) never carry the word “phenotype” on any surface. Cardiovascular/ASCVD framing is risk, not identity.
6. **Organ patterns ship as “pattern,” “stress,” or “strain.”** Never as “phenotype,” never as bare organ names (“kidney” alone is not a card label).
7. **Syndrome states use the clinical name.** “Iron deficiency” stays “iron deficiency.” Retail subtitle softens the impact; the label does not.
8. **One name per surface, stable across releases.** Retail label, clinical label, and internal id each have exactly one allowed value per record at a time. Changing any of them is a governance event, not a copy tweak.
9. **Drift check is explicit.** The IDL is the single source of truth. Product, marketing, and engineering all pull labels from the IDL or a materialised view of it. Marketing decks do not invent names that do not exist in the IDL.
10. **Acronyms allowed only in clinical surfaces.** “ASCVD,” “MASLD,” “IR,” etc. are allowed in `clinical_display_label` and in clinician exports. Retail labels expand or rephrase them.

---

## 8. Commercial alignment note

The screening priorities doc ranks six commercial lanes. Mapping the current 9 against those lanes:

| lane | current 9 fit |
|---|---|
| Dysglycaemia / insulin resistance | **Strong.** `ph_metabolic_early_ir_v1` (flagship phenotype) and `ph_hba1c_metabolic_stress_v1` (syndrome-state) already populate this lane. |
| Atherogenic cardiometabolic / ASCVD | **Partial.** `ph_vascular_hcy_inflammation_v1` is a cardiometabolic modifier; we do not yet have a first-class ASCVD/atherogenic-burden record. Future addition needed. |
| CKD / kidney risk | **Partial.** `ph_renal_stress_v1` covers early kidney strain, but a dedicated CKD-risk record is a natural next entity. |
| MASLD / liver fibrosis | **Partial.** `ph_hepatic_alt_inflammatory_v1` is the MASLD-adjacent lane. A formal liver-fibrosis risk record is a natural next entity. |
| Integrated metabolic clustering | **Not represented.** This is a future synthesis record across metabolic + cardiometabolic + hepatic lanes. Deliberately out of the current 9. |
| Iron deficiency (high-volume adjunct) | **Strong.** `ph_iron_deficiency_inflammation_v1` and, structurally, `ph_iron_overload_v1` cover the iron lane. |
| Thyroid (secondary) | **Covered.** `ph_thyroid_lipid_disturbance_v1` and `ph_tsh_axis_metabolic_v1` sit here as organ-patterns. Appropriately secondary. |

**Implications for future expansion (brief, not a roadmap).**
- The weakest lanes against the current 9 are **ASCVD / atherogenic risk** and **CKD risk** as first-class risk constructs, plus **integrated metabolic clustering** as a stratification layer. These are the likely shapes of new IDL records, not more `phenotype` entries.
- Future additions of `risk_construct` / `organ_pattern` / `syndrome_state` records are preferred over new `phenotype` records. Phenotype slots are earned, not defaulted.
- `future_commercial_domain` on each record makes this alignment machine-readable, so product and commercial can report coverage against the six lanes without tribal knowledge.

---

## 9. Final design decision

1. **Adopt the Interpretation Display Layer (IDL)** as defined in §5 as the governing contract for Section 5.
2. **Lock the four-class model** (`phenotype`, `risk_construct`, `organ_pattern`, `syndrome_state`) with the usage rules in §3. No new classes added without design review.
3. **Lock the 9-entity mapping** in §4, including `frontend_allowed_term` values. Exactly one retail-phenotype record (`ph_metabolic_early_ir_v1`) on day one.
4. **Lock the required card composition** in §6 (label, subtitle, severity, supporting summary, why-it-matters) and the retail-forbidden list.
5. **Lock the naming rules** in §7, in particular: gated use of “phenotype,” mandatory subtitles, banned generic-bucket labels.
6. **Treat the IDL as the single source of truth** for interpretation labels across product, commercial, and engineering surfaces.

Anything that contradicts items 1–6 requires a governance amendment to this document before it ships.

---

## 10. Next implementation consequence

The next sprint must be a **backend + content** sprint that creates the IDL. Proposed working name: **BE-IDL-1 — Interpretation Display Layer v1**.

Scope of BE-IDL-1 (sketch, not a prompt):

1. Define the IDL contract as a new versioned Pydantic model (e.g. `InterpretationDisplayRecordV1`, `InterpretationDisplayLayerV1`) with the fields in §5.
2. Author the **9 display records** using the table in §4 as the sole source of labels, subtitles, and why-it-matters copy.
3. Add a deterministic compiler/publisher step that:
   - reads the engine-side interpretation entities,
   - matches them by `internal_id`,
   - emits an `interpretation_display_layer_v1` bundle on the analysis result,
   - enforces `enabled_for_frontend` and `frontend_allowed_term` at publish time (no secrets leak to retail shape).
4. Extend the analysis result DTO and the API emission path to expose the bundle (typed) to the frontend.
5. Add governance tests:
   - every IDL record has a non-empty `retail_display_label`, `subtitle`, `why_it_matters`, `scientific_class`, `frontend_allowed_term`;
   - only records with `frontend_allowed_term = phenotype_allowed` carry “phenotype” in their `retail_display_label`;
   - banned generic-bucket labels (configurable list) never appear in any `retail_display_label`;
   - `display_order_priority` values are unique within an analysis bundle.

**FE-R8 is blocked** until BE-IDL-1 lands. When it does, FE-R8 becomes a thin surfacing sprint (render the IDL, obey §6) rather than a design sprint.

**Out of scope for BE-IDL-1:**
- New interpretation entities beyond the current 9.
- New commercial lanes (ASCVD first-class, CKD risk, integrated metabolic cluster) — those are future IDL records, not BE-IDL-1 work.
- Any change to engine scoring, ranking, or severity logic.
- Any Gemini/LLM narrative generation for Section 5 copy. All §4 copy is human-authored and governed.
