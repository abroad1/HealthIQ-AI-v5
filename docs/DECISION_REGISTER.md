# HealthIQ AI — Decision Register

**Last updated:** 2026-05-04  
**Status:** LIVE — add decisions here when they are settled, not after  
**Purpose:** Stop the same questions being repeatedly reopened

This register captures durable architectural, product, and governance decisions. A decision belongs here when:
- it has been made and should not be relitigated without new evidence
- it currently lives scattered across strategy docs, audits, or chat
- reopening it without acknowledging it is a recurring cost

Each entry states the decision, who/what established it, and where the full reasoning lives.

---

## Architecture Decisions

### A-1: HealthIQ is a deterministic three-layer platform — no LLM in Layer B

**Decision:** LLM reasoning is permanently excluded from the analytical core (Layer B). Gemini is confined to parsing/translation surfaces. Any proposal to introduce LLM reasoning into analytical output generation must be rejected.

**Established by:** ADR-001, ADR-002; CLAUDE.md §4  
**Authority:** `architecture/ADR-001-platform-non-negotiables.md`  
**Status:** Locked. Not subject to review without a new ADR.

---

### A-2: Gemini is the sole runtime LLM

**Decision:** Gemini (not GPT, Claude, or other) is the runtime LLM. It is used for upload parsing and Layer C narrative translation only.

**Established by:** CLAUDE.md §4  
**Status:** Locked.

---

### A-3: The AB / VR panels are test harnesses, not the product boundary

**Decision:** AB (Anthony Broad) and VR (validation panel) are internal development harnesses for testing analytical depth. They are not the product's analytical scope ceiling. Phase 1 commercial scope is broader than these two panels.

**Established by:** Strategic Vision v1.5 §1; PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md  
**Status:** Settled.

---

### A-4: Biomarkers do not lead the user experience

**Decision:** The results experience leads with phenotype-level interpretation, not a biomarker list or lab report view. Biomarkers are a premium evidence layer, not the primary narrative.

**Established by:** Results Journey Paper v6; Strategy Stack Authority Map decision 3  
**Authority:** `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`  
**Status:** Settled.

---

### A-5: Schema authority is the locked schema file — not memory or prior batches

**Decision:** When schema conflicts arise, the locked schema file is the authority. Prior batch outputs or remembered schema states must not be treated as canonical.

**Established by:** CLAUDE.md §7 rule 5  
**Status:** Standing rule.

---

### A-6: No hardcoded reference ranges (except governed calculated-ratio policy cases)

**Decision:** Reference ranges must come from the governed SSOT, not from hardcoded values in code. Exception: calculated-ratio policy cases where ranges are derivable from first principles and governed as such.

**Established by:** CLAUDE.md §7 rule 1; ADR-002  
**Status:** Locked.

---

## Signal / Intelligence Decisions

### I-1: The lead finding must be explained, not merely stated

**Decision:** Every primary finding surfaced to the user must include a WHY explanation — either a governed hypothesis or an explicit fallback indicating WHY reasoning is not yet available for that signal. Silent omission of WHY is not acceptable.

**Established by:** PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md Sprint 1 Bug 3; Strategy Stack decision 5  
**Implementation:** R-1 fallback mechanism; R-8 Wave 1 governed WHY  
**Status:** Settled. Gap remains for Wave 2 signals (WHY Wave 2 not yet started).

---

### I-2: WHY Wave 1 target signals are lipid panel and Vitamin D

**Decision:** The first WHY expansion wave covers total cholesterol high and Vitamin D low — the highest-prevalence signals in UK commercial blood panels. Complete. Wave 2 targets are iron panel, inflammatory markers, renal, and expanded thyroid — not yet started.

**Established by:** `docs/RESET_SPRINT_PLAN_2026-04.md` Sprint 8  
**Implementation:** R-8 (`2f0b346`)  
**Status:** Wave 1 settled and complete. Wave 2 pending.

---

### I-3: Contradictory signals on the same analyte value are a defect, not a feature

**Decision:** A single panel value must not simultaneously activate both the high-signal and low-signal for the same analyte. This is a trust-destroying bug. The `enable_upper_bound` / `enable_lower_bound` flags in signal definitions are the authority for which direction is valid.

**Established by:** `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §2.1  
**Implementation:** R-1 (`7f48cb6`)  
**Status:** Fixed. Regression guard is part of Sentinel Phase 1.

---

### I-4: One-sided lab ranges are valid and must be scored

**Decision:** A biomarker range is valid and scoreable if it has either a min or a max — not both required. LDL (upper bound only) and HDL (lower bound only) are the canonical examples. Requiring both min and max is a bug.

**Established by:** `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §2.2  
**Implementation:** R-1B (`7679f89`)  
**Status:** Fixed.

---

## Governance Decisions

### G-1: Full Automation Bus SOP applies to Intelligence Core only

**Decision:** The full Automation Bus SOP (Stages 0–5, prompt hardening, gate) is required for changes to `backend/core/`, `backend/ssot/`, `backend/scripts/` (run_work_package, golden_gate, update_cursor_status), and Knowledge Bus hypothesis YAMLs consumed by the Intelligence Core. Frontend, API routes, and commercial surfaces use a lightweight branch-PR-review model.

**Established by:** `docs/RESET_SPRINT_PLAN_2026-04.md` governance calibration table  
**Authority:** `docs/AUTOMATION_BUS_SOP_v1.3.1.md`  
**Status:** Standing governance rule.

---

### G-2: No implementation or merge on main without a branch

**Decision:** All implementation work — however small — begins on a named branch. Never build directly on main.

**Established by:** CLAUDE.md §13  
**Status:** Non-negotiable. Standing rule.

---

### G-3: No CONFIRMED claim without cited file path and line number

**Decision:** In hardening JSON and audit outputs, no field may carry "CONFIRMED" without a specific file path and line number citation. Uncited confirmations are treated as incomplete.

**Established by:** CLAUDE.md §7 rule 6; MEMORY.md hardening discipline  
**Status:** Non-negotiable. Standing rule.

---

### G-4: Docs-only bypass requires all changes under `/docs/`

**Decision:** The Docs-Only Bypass (SOP §11) applies only when every changed file in the branch is under `/docs/`. A single file outside `/docs/` requires the full bus.

**Established by:** `docs/AUTOMATION_BUS_SOP_v1.3.1.md` §11  
**Status:** Non-negotiable rule.

---

## Product / UX Decisions

### P-1: HealthIQ is a guided reasoning journey, not a better lab report

**Decision:** The product's primary narrative is a reasoning journey — what was found, why it matters, what it means for the user — not a structured lab report or marker-by-marker alert list.

**Established by:** Strategy Stack Authority Map decision 1; Results Journey Paper v6  
**Status:** Settled. Locked.

---

### P-2: The results page leads with one primary finding, above the fold

**Decision:** The results page must answer "what is my most important finding and what does it mean?" without requiring the user to scroll. Progressive disclosure gates depth behind deliberate interaction. Wall-of-sections is not acceptable.

**Established by:** `docs/RESET_SPRINT_PLAN_2026-04.md` Sprint 3 specification  
**Implementation:** Sprint 3 (`284d188`)  
**Status:** Settled and implemented.

---

### P-3: Phenotype is a strategic umbrella term, not every entity is called a phenotype

**Decision:** "Phenotype" is used strategically to describe pattern-level metabolic constructs. Not every governed interpretation entity (signal, cluster, interaction pattern) should be publicly labelled as a phenotype. Internal IDs (`ph_*_v*`) must not appear on customer-facing surfaces.

**Established by:** Strategy Stack Authority Map decision 9; Sentinel Phase 1 slug leakage guard  
**Status:** Settled. Slug leakage guard enforces it at test time.

---

### P-4: Clinician handoff remains distinct from the retail journey

**Decision:** The clinician report and the retail user journey are separate surfaces with separate design contracts. Clinician content must not bleed into the primary retail experience without intentional disclosure.

**Established by:** Strategy Stack Authority Map decision 12; Results Journey Paper v6  
**Status:** Settled.

---

### P-5: Section 5 / pattern-layer implementation is gated behind an existence check

**Decision:** The Section 5 pattern layer is not rendered unless the underlying asset exists and passes an existence check. No empty or placeholder rendering.

**Established by:** Strategy Stack Authority Map decision 11  
**Status:** Settled.

---

## Open Questions (not yet settled)

The following are known but not yet decided. They should not be treated as settled even if they appear in documents.

| Question | Status | Where it lives |
|---|---|---|
| Pricing model (first free / subscription / per-analysis) | **UNDECIDED** | Sprint 7 was implemented with a model; the commercial decision to confirm or revise is pending leadership confirmation |
| Privacy disclosure copy for LLM parsing at upload | **UNDECIDED** | April 2026 review identified the gap. Whether copy exists in the current upload flow is unverified. |
| Release confidence gate definition (what must be true before first paying user) | **UNDEFINED** | No formal document exists |
| WHY Wave 2 start date and priority order | **UNSCHEDULED** | Reset Sprint 8 defines Wave 2 targets but the sprint has not been authored |
| Frontend design system documentation | **UNDEFINED** | No single source exists |
| ADR-006 — existence or intentional gap | **UNCLEAR** | ADR-007 exists but ADR-006 is absent from the registry with no explanation |

---

## How to Add a Decision

When a material decision is made:
1. Add it under the relevant section with a short, declarative title
2. State the decision directly — not "we decided to consider" but "X is Y"
3. Cite the document or event that established it
4. Note the status: Locked / Settled / Standing rule / Pending confirmation
5. If the decision supersedes a prior one, note what changed
