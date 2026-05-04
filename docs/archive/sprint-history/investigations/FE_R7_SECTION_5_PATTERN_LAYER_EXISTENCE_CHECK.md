# FE-R7 — Section 5 pattern layer: existence check and specification gate

**Work ID:** FE-R7-RESULTS-JOURNEY-V6  
**Date:** 2026-04-16  
**Type:** Research and specification only (no code changes in this sprint)

**Governing context:** Results Journey v6 (`docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`, esp. Section 5 ~L326–L403, Phase 2 gate ~L359–L379, ~L592, ~L736, ~L790–L792); taxonomy direction (`docs/strategy/Phenotype_Terminology_Proposal.md`); commercial screening direction (`docs/strategy/healthiq_future_screening_priorities.md`).

---

## 1. Executive conclusion

**Section 5 (“Patterns across your body”) is not implementation-ready as a governed pattern-card layer.**

The frontend results path exposes **clusters** with **generic names**, **severity/score/confidence**, **descriptions**, optional **system educational explainers**, and **biomarker lists**. There is **no** scientific classification field (phenotype / risk construct / syndrome-state / organ-pattern), **no** dedicated clinical display name or plain-English subtitle contract, and **no** governed “why it matters” field separate from free-text description or explainer body.

The component currently shipped as “Section 5” in the retail journey (**`SystemUnderstandingSection`**, FE-R5) is a **compact “how to read your results” explainer** (three static blocks). It is **not** the v6 **pattern-card** layer described for Section 5.

**Decision: Option B — contract / content / DTO work must come before an R-8 frontend surfacing sprint** that pretends to be the full Section 5 pattern layer with strong retail naming and taxonomy discipline.

A **limited** R-8 could still surface **existing** cluster cards with copy improvements **only if** explicitly scoped as “thin surfacing” and not as the full governed pattern layer—otherwise UX risk is high (see §8).

---

## 2. Current Section 5 source asset inventory

### 2.1 Frontend DTO — `clusters[]`

**Source:** `frontend/app/types/analysis.ts` (`Cluster`, ~L106–L120).

| Asset | Present on path | Notes |
|--------|-----------------|--------|
| `cluster_id` / `id` | Yes | Internal identifiers |
| `name` | Yes | Primary user-visible label for the cluster |
| `category` | Yes | Broad bucket (e.g. metabolic), not a governed taxonomy class |
| `summary` / `description` | Yes | Free text; strength varies |
| `severity`, `score`, `confidence` | Yes | Usable for emphasis, not naming |
| `biomarkers` / `biomarkers_involved` | Yes | Supporting markers |
| `recommendations` | Yes | List strings |
| `system_educational_explainer` | Yes (optional) | `{ title, body }` — educational, not a three-layer naming model |

**Not present:** `scientific_classification`, `clinical_display_name`, `plain_english_subtitle`, `why_it_matters` as first-class fields.

### 2.2 Backend cluster hit model

**Source:** `backend/core/models/results.py` (`ClusterHit`, ~L121–L135).

Fields align with a **retail cluster hit**: `cluster_id`, `name`, `biomarkers`, `confidence`, `severity`, `description`, optional `system_educational_explainer`. **No** taxonomy or dedicated subtitle / why-it-matters contract.

### 2.3 API emission

**Source:** `backend/app/routes/analysis.py` (~L193–L207) + `extend_cluster_client_dict_from_hit` in `backend/core/dto/builders.py` (~L125–L131).

Stored clusters include the base dict plus **`system_educational_explainer`** when present on the hit. **No** additional interpretation-display taxonomy fields are merged.

### 2.4 SSOT cluster definitions

**Source:** `backend/ssot/clusters.yaml` (~L8–L90).

Canonical clusters (metabolic, cardiovascular, hepatic, etc.) use **short internal descriptions** (e.g. “Metabolic biomarkers (glucose, HbA1c, insulin)”). These are **schema/membership labels**, not a user-facing governed naming system with classification and subtitle layers.

### 2.5 What users see today — UI

**`ClusterSummary`** (`frontend/app/components/clusters/ClusterSummary.tsx`): Renders name, severity, description, biomarkers, scores, recommendations, optional `systemEducationalExplainer`. **Not** a pattern taxonomy layer; names can read as **generic system buckets**.

**`SystemUnderstandingSection`** (`frontend/app/components/results/SystemUnderstandingSection.tsx`, comment ~L40–L42): **FE-R5 “Section 5”** in code comment refers to **educational framing** (“How to understand your results”), **not** v6 **“Patterns across your body”** pattern cards.

### 2.6 Governed interpretation-display layer

**Conclusion:** **No.** There is no separate contract that carries **internal id + scientific class + clinical name + subtitle + why-it-matters** as specified in the v6 paper’s Phase 2 target. Existing pieces are **cluster name + description + optional explainer**.

---

## 3. Naming / display contract assessment

| Desired element (v6 / gate) | Status |
|-----------------------------|--------|
| Internal id | **Exists** (`cluster_id`) |
| Scientific classification (phenotype / risk / syndrome-state / organ-pattern) | **Missing** — `category` is not this taxonomy |
| Clinical display name (distinct from internal) | **Missing** — single `name` field only |
| Plain-English subtitle | **Missing** as a dedicated field (only narrative fragments in `description` / explainer) |
| Why-it-matters explainer | **Partial** — `description`, `system_educational_explainer.body`; not structured as a governed “why it matters” line |

**Naming quality:** Current **cluster `name`** values are often **adequate for a system list** but **not sufficient** for the **middle interpretation layer** described in v6: weak or generic naming would **collapse perceived value** of Section 5 (v6 paper ~L402–L403). SSOT descriptions reinforce **functional grouping language**, not retail pattern branding.

---

## 4. Taxonomy alignment assessment

Approved direction: **not everything is a phenotype**; supported classes may include phenotype, risk construct, syndrome/state, organ-pattern (`Phenotype_Terminology_Proposal.md`; v6 ~L333–L339).

**Current assets:** Clusters do **not** carry an explicit, validated classification enum aligned to those classes. **`category`** is a loose bucket, not medically governed taxonomy for Section 5.

**Alignment verdict:** **Cannot** honestly map current cluster rows to the four-class model **without inferring** classification from free text—**out of scope** for a truthful user-facing pattern layer.

---

## 5. Commercial alignment assessment

Strategic screening lanes (e.g. dysglycaemia / IR, cardiometabolic risk, CKD, MASLD, integrated metabolic clustering, iron deficiency) are **directional** (`healthiq_future_screening_priorities.md`). They require **stable, evolvable constructs** and **credible naming**.

**Current cluster SSOT** is **organ- and domain-scoped** (metabolic, cardiovascular, hepatic, renal, …) in a way that **could eventually** map to those lanes, but **without** a governed display and classification layer, the **product cannot evolve** those constructs **without taxonomy and copy chaos** (duplicate “metabolic” stories, phenotype overreach, weak differentiation).

**Verdict:** **Future alignment is possible structurally** (systems/clusters as seeds) but **not safe to productize as Section 5** until **contract + content** catch up.

---

## 6. Decision

**Option B — Contract / content / interpretation-display work first** (before treating R-8 as “implement full Section 5 pattern layer”).

**Section 5 is not implementation-ready** for the **v6 Phase 2 pattern-card experience** with **strong naming and taxonomy discipline** using **only** today’s surfaced fields.

---

## 7. Consequences for R-8

**If R-8 is scoped as “full Section 5 (Patterns across your body)” per v6:**

- Define or extend an **interpretation-display contract** for pattern rows: at minimum **classification** (governed enum), **clinical display name**, **subtitle**, **why it matters** (or equivalent structured fields), with **clear separation** from raw cluster engine labels.
- **Content pipeline** or **compiler** work to populate those fields deterministically (no Gemini as authority for clinical class).
- **Backend/API** paths to emit the new structure on `clusters` or a dedicated `pattern_interpretations[]` (exact shape is a design decision—**not** specified in FE-R7).
- **Frontend** only after the above: pattern cards that consume the contract without inferring taxonomy.

**If R-8 is scoped narrowly:** e.g. improve **ClusterSummary** copy and layout using **existing** fields only—label it explicitly as **Phase 1.5 / thin surfacing**, not the gated Phase 2 pattern layer.

---

## 8. Risks if we proceed incorrectly

- **Weak middle layer:** Generic pattern names and no taxonomy → users perceive **marketing fluff** or **incoherence** between lead finding and “patterns.”
- **Phenotype overreach:** Calling clusters “phenotypes” without a governed class → **medical and credibility risk**.
- **Commercial drift:** Screening lanes **named in strategy** but **not supported by contracts** → roadmap churn and rework.
- **Technical debt:** Frontend work that **encodes inferred taxonomy** in components → **hard to unwind** when real DTOs arrive.

---

## Explicit questions (sprint checklist)

| # | Question | Answer |
|---|------------|--------|
| 1 | What is the current Section 5 source layer? | **Clusters[]** (+ optional system explainers, descriptions); **not** a separate pattern taxonomy layer. **FE-R5 “Section 5” in UI is an explainer block, not pattern cards.** |
| 2 | Is there a governed interpretation-display layer? | **No.** |
| 3 | Can current assets support pattern cards without weak naming? | **Not at the v6 bar** without new contract/content. |
| 4 | Do assets support the approved taxonomy direction? | **No explicit support**; inference would be speculative. |
| 5 | Can the pattern layer evolve toward commercial screening constructs cleanly? | **Only after** contract + naming discipline; **not** with current fields alone. |
| 6 | Is R-8 frontend-first or contract-first? | **Contract/content first** for the **full** Section 5 vision; **optional** thin frontend only if explicitly scoped. |

---

## Acceptance criteria mapping

| Criterion | Met |
|-----------|-----|
| Clear yes/no on implementation-readiness | **Yes** — **No**, not for full Section 5 as specced in v6 Phase 2 |
| Grounded in existing assets | **Yes** — citations to `analysis.ts`, `results.py`, `analysis.py`, `clusters.yaml`, `ClusterSummary`, `SystemUnderstandingSection` |
| Naming quality assessed | **Yes** — §3 |
| Taxonomy alignment assessed | **Yes** — §4 |
| Commercial alignment assessed | **Yes** — §5 |
| What R-8 must be next | **Yes** — §7 |
