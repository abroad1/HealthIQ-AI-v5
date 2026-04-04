# Primary Concern and Ranked Ambiguity Policy

**Policy ID:** `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY`  
**Version:** `v1`  
**Status:** ADOPTED (governance record)  
**Workpackage:** `KB-S54B-POLICY` (Phase 1 — policy only)  
**Supersedes:** _None_ (first formal policy in this domain)  
**Related:** `docs/investigations/KB-S54B_PRIMARY_CONCERN_RANKED_AMBIGUITY_PREFLIGHT.md`, `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`, `docs/investigations/KB-S53_VR_FIXTURE_OPERATOR_REVIEW.md`  

---

## 0. Stage 1C — Policy scope preflight (record)

Verified before authoring this artifact:

1. **Strategic decision already recorded:** Current deterministic ranking remains **operational** until replaced by governed implementation; **no ad hoc** ranking-policy changes during unrelated sprints (e.g. KB-S53 harness work); **future** behaviour should support **ranked ambiguity** and **confidence-weighted interpretation** where justified — per investigation and operator acceptance docs cited above.
2. **Current repo behaviour (reference, not normative):** `compile_report_v1` orders `report_v1.top_findings`; `compile_clinician_report_v1` selects **`top_findings[0]`** for the singular clinician **`primary_concern`** string and aligned root-cause block — see preflight §3.
3. **This sprint did not modify:** runtime code, report compilers, contracts/DTOs, fixtures, or frontend rendering.
4. **Authority of this document:** This policy is the **governance source** later implementation phases **must follow**. It does not, by itself, change product behaviour.

---

## 1. Purpose

This policy defines what **primary concern** means in HealthIQ, how **ranked ambiguity** should be handled in principle, and how **confidence** and **evidence completeness** should inform interpretation — **before** any runtime, contract, fixture, or UI change is authorised.

It exists to:

- Prevent **silent** or **convenience-based** ordering from being mistaken for **clinical or product truth**
- Give delivery a **single explicit philosophy** for later phased implementation
- Separate **governed evidential intent** from **deterministic implementation mechanics**

---

## 2. Background / problem statement

Structured reports necessarily **compress** many signals into a **readable** narrative. Compression creates two risks:

1. **False certainty:** A single “lead” line can imply one dominant interpretation when **several** interpretations are **similarly supported** or **similarly uncertain**.
2. **Opaque ranking:** When ties are broken by **implementation convenience** (e.g. lexicographic identifiers), downstream users may infer **intentional clinical prioritisation** where none was decided.

HealthIQ has operated with a **transparent but minimal** ordering rule in code (severity, then confidence, then deterministic tie-break). That behaviour is **reproducible** and was **accepted as operational truth** for harness purposes; it is **not** by itself a statement of long-term clinical prioritisation philosophy.

This policy records **what HealthIQ should aim to communicate** and **how future implementation must relate to deterministic machinery**.

---

## 3. Current operational state (declarative summary)

Until superseded by governed implementation:

- **Ranking for `top_findings`** is produced by the existing report compiler ordering (see preflight).
- **Clinician headline** reflects **`top_findings[0]`** only; **no** parallel ambiguity field exists in the clinician contract.
- **Multi-finding** root-cause data may exist in **`RootCauseV1`**, but the **clinician summary** foregrounds **one** signal-aligned finding for page-1 narrative.

This section describes **what runs today**, not **what is ultimately desired**. Desired behaviour is in §5–§8.

---

## 4. Policy decision (summary)

HealthIQ **commits** to the following:

1. **Primary concern** is a **governed concept**: it must reflect **evidential and product intent**, not only sort order.
2. Where **multiple interpretations** are **materially plausible** and **similarly supported**, the product should **surface ranked ambiguity** rather than **collapse** to an arbitrary single winner — subject to UX and contract work in later phases.
3. **Confidence** and **evidence state** (supporting markers, contradictions, missing data, confirmatory tests) are **first-class inputs** to how concerns are **ranked** and **described**, not cosmetic adornments.
4. **Deterministic fallback** remains **required** for engineering reproducibility, but must be **labelled as such** in implementation and must **not** be mistaken for **clinical primacy** when used only to break ties.

---

## 5. Definition of primary concern

### 5.1 Meaning

**Primary concern** (in HealthIQ) means: the **lead interpretation** the product chooses to foreground **for discussion**, representing the **most salient** signal-level concern **after** applying governed rules for severity, confidence, evidence completeness, and ambiguity.

It is **not**:

- a **diagnosis**
- a **treatment directive**
- an assertion that **other concerns are unimportant**

### 5.2 When one lead concern is appropriate

A **single** lead concern is appropriate when:

- One interpretation is **materially stronger** on **state severity**, **confidence**, and **evidential support** relative to alternatives, **or**
- Alternatives are **clearly secondary** (e.g. lower severity, materially lower confidence, or materially weaker marker support) under rules to be encoded later.

### 5.3 When a single dominant line is **not** appropriate

A single dominant headline is **misleading** when:

- Two or more concerns **tie** on coarse severity **and** are **close** on confidence **and** have **competing** plausible mechanistic stories **without** a governed reason to prefer one, **or**
- **Missing** or **contradictory** markers make **any single** “winner” **under-supported** relative to honest uncertainty.

In those situations, policy expects **ranked ambiguity presentation** (§6), not silent tie-break as **clinical ranking**.

---

## 6. Ranked ambiguity rules

### 6.1 Definition

**Ranked ambiguity** means: HealthIQ **explicitly presents** two or more **plausible interpretations** in **ranked** form — with **transparent** rationale for order — rather than pretending **exactly one** concern fully captures the situation.

### 6.2 When to surface multiple plausible interpretations

Implementation **should** surface ranked ambiguity when **all** apply:

- **Plurality:** At least two distinct signal-level concerns (or hypotheses) are **credible** given the panel.
- **Parity or uncertainty:** They are **not** cleanly ordered by a **strong** evidential margin (to be operationalised in a later sprint).
- **User trust:** Hiding the ambiguity would **materially overstate** certainty.

### 6.3 Communication standard

- Prefer **structured** ranked lists or labelled tiers over **vague** language.
- **Rank** must be **explainable** from evidence factors (§7), not from opaque sorting.
- **Ambiguity** is a **feature** of honest interpretation when evidence supports it; it is **not** a failure mode by default.

### 6.4 What ranked ambiguity is not

- It is **not** an exhaustive enumeration of every weak signal.
- It is **not** permission to abandon **determinism**; the **same inputs** must yield the **same** ranked ambiguity structure under the same policy version.

---

## 7. Confidence-weighting principles

This section defines **policy logic** for later encoding. It does **not** mandate a specific numeric formula in v1.

Factors that **should** influence ranking and narrative emphasis:

| Factor | Principle |
|--------|-----------|
| **Primary metric / signal state** | Higher **clinical salience** states (as defined by product/clinical governance) should **generally** rank above lower salience, **holding evidence parity**. |
| **Signal confidence** | Higher **warranted** confidence (given available markers and ranges) should **generally** rank above lower — **provided** confidence is **calibrated** to missing/contradictory evidence. |
| **Supporting markers** | Broader **consistent** support across relevant markers should **strengthen** ranking; **absence** of expected support should **weaken** it. |
| **Contradictory markers** | **Active contradiction** should **penalise** ranking or **trigger** ambiguity presentation rather than a clean single lead. |
| **Missing informative markers** | **Material gaps** that block differentiation between hypotheses should **reduce** implied certainty and may **elevate** ranked ambiguity. |
| **Confirmatory tests** | **Presence** of actionable confirmatory paths may **clarify** differentiation; **Absence** where differentiation depends on them may **increase** ambiguity — without implying tests were “required” for basic discussion where not appropriate. |
| **Evidential completeness overall** | The **whole-panel** context (ranges, quality flags) should modulate how strongly a single lead is asserted. |

**Ordering rule (policy intent):** Implementation must **not** treat **lexicographic signal identifiers** (or any **purely technical** key) as a **clinical** reason for primacy. Such keys may remain **only** as a **last-resort deterministic fallback** (§8).

---

## 8. Deterministic fallback rules

### 8.1 Why deterministic fallback exists

HealthIQ requires **reproducible** outputs for testing, replay, and audit. Some **total order** over concerns is **always** required in code.

### 8.2 When deterministic fallback is acceptable

Fallback ordering (e.g. stable tie-break after all **policy-relevant** comparisons are exhausted) is acceptable **only** when:

- It is **documented** as **technical tie-break**, not clinical priority, **and**
- The product **does not** present it as **evidence-based preference**, **or**
- The UI/copy **explicitly** reflects **ambiguity** when fallback is invoked for **near-tie** situations (to be implemented in later phases).

### 8.3 Lexicographic and similar tie-breaks

**Lexicographic `signal_id` (or similar)** may continue as **engine stabiliser** **until** replaced, but **must** be treated as:

- **Non-clinical**
- **Non-product**
- **Non-authoritative** for “why this concern leads”

Future implementation **should** replace pure lexicographic primacy with either:

- A **governed** tie policy (explicit clinical/product rule), **or**
- **Ranked ambiguity** presentation when no governed primacy exists.

### 8.4 What fallback must not be mistaken for

Fallback must **never** be documented or marketed as “the clinically correct order” solely because it is **deterministic**.

---

## 9. Implementation implications (for later phases only)

This policy **does not** authorise code changes. Future work **is expected** to include, as **separate** governed sprints:

| Phase | Expected content |
|-------|-------------------|
| **Runtime / report selection** | Encode ordering and ambiguity detection in `compile_report_v1` and related logic; introduce **policy version / rationale** stamping if required for replay. |
| **Clinician report compiler** | Align `compile_clinician_report_v1` with primary vs ambiguity presentation; avoid implying sole primacy when policy demands ambiguity. |
| **Contracts / DTOs** | Extend `ClinicianReportV1` (and related types) if multiple foreground concerns or ambiguity labels are required — **extra="forbid"` schemas imply versioned change**. |
| **Fixtures / harness** | Update AB/VR and other golden artefacts to match **declared** policy behaviour. |
| **Frontend** | Render additional concern lines or ambiguity UI; update types and tests. |

**Cross-cutting:** Regression strategy must tie **policy version** to **expected outputs** where applicable.

---

## 10. Explicit non-goals (this policy artifact)

This document **does not**:

- Change **runtime** behaviour
- Specify **exact** numeric weighting functions
- Replace **clinical governance** for severity taxonomies
- Define **regulatory** claims or **diagnostic** labels
- Subsume **system-burden** or **arbitration** semantics (separate domains; alignment with headline policy is a **later** design question)
- Reopen **KB-S53** or reinterpret harness acceptance as **ranking** authorisation

---

## 11. Handoff to later implementation phases

**Prerequisites before runtime sprint:**

1. **Freeze** this policy version (`v1`) as the **authoritative intent** for primary concern and ranked ambiguity.
2. **Author** an implementation workpackage that maps §5–§8 to **concrete** algorithms, **contract** deltas, **fixture** plans, and **FE** changes.
3. **Accept** that **changing** the clinician headline contract or UI is **likely** if true ranked ambiguity is required.

**Success criteria for implementation (future):**

- No **silent** lexicographic primacy as **user-visible clinical reasoning**
- **Deterministic** outputs with **explicit** handling of ties and ambiguity
- **Tests** and **fixtures** that encode the **policy**, not accidental sort side-effects

---

## Document control

| Field | Value |
|-------|--------|
| Owner | Product / Intelligence governance (assign owner at implementation) |
| Review cadence | When ranking semantics or contracts change materially |
| Next revision trigger | First runtime release claiming compliance with this policy |
