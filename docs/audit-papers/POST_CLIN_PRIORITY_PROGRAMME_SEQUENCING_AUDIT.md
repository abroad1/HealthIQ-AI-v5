# Post-CLIN-PRIORITY Programme Sequencing Audit

**Mode:** B1A pipeline throughput review, repository-grounded, document-only (no code discovery performed).
**Date:** 2026-08-05

## Current programme position (repository-verified)

The beta-readiness build programme (BUILD_DELIVERABLE_REGISTER.md) has run through the eight-block domain/signal build-out and, since 2026-08-01, an "architecture convergence" track (ARCH-CONV-A through ARCH-CONV-PKGC-2 / ARCH-CONV-I-ALT-IDPROV-1) that closed compiled-WHY identity and provenance gaps. That track's own carry-forward register left one item explicitly open across four consecutive closures (ARCH-CONV-PKGC-1, PKGC-2, ARCH-CONV-I, ARCH-CONV-I-ALT-IDPROV-1): **`CF-ARCH-CONV-VERSION-1` — result-versioning / regeneration authority.**

Two packages have since closed on top of that track, both independently audited this session:
- **CLIN-PRIORITY-CORE-1** (merged to `main`, 2026-08-05) — cross-domain clinical finding/prioritisation authority. Independent post-finish audit: `PASS` with only non-blocking carry-forwards (consumer wording, legacy field schema retirement).
- **CLIN-PRIORITY-RESULT-REGEN-1** (kernel-complete, branch `feature/clin-priority-result-regen-1`) — analysis-policy version, `result_date`, regeneration lineage, and a new backend-owned trend/supersession authority. Independently audited this session: `PASS`. **This closes `CF-ARCH-CONV-VERSION-1`**, though the carry-forward register text has not yet been updated to say so.
- **`fix/uat-alt-prioritisation`** — a bounded fix making `clinical_concern_set` the sole hero/body-overview/lead-narrative authority. Independently audited this session: `PASS` on its own narrow scope.

A **fresh, evidenced UAT investigation** on that same live branch (`UAT_RESULTS_PAGE_PRESENTATION_INVESTIGATION_1ce310e1.md`, 2026-08-05) then found that even with correct ranking, the consumer results page still fails as a coherent consumer surface. Verdict: `RESULTS_PAGE_REQUIRES_PRODUCT_COPY_DECISION` — explicitly a **presentation/copy-boundary defect, not a ranking defect**.

**Documented programme commitment vs. repository state:** the BUILD_DELIVERABLE_REGISTER.md has no entries yet for CLIN-PRIORITY-RESULT-REGEN-1 or `fix/uat-alt-prioritisation` — register hygiene is lagging actual repository state by at least two closed packages. This is a documentation gap, not a defect in the work itself, but it means the register cannot currently be read as authoritative for "what's done."

## Newly evidenced UAT defects (repository-verified, this session)

With the concern-set ranking fix in place, the live results page still:
1. Renders the internal finding `label` (snake_case, mechanically title-cased) as the consumer headline — repeated across at least four surfaces (hero, body overview, Clinical Priority row, Primary Finding card).
2. Injects raw `urgency_time_band` / `severity_band` enum values into generated narrative prose (`buildDiscussFirstSentence`), not just technical metadata rows.
3. Retains legacy `narrative_report_v1` fragments (lifestyle, cardiovascular-context, related-systems list) after the conflicting MCV lead sentence is stripped — the suppression is a regex sentence-filter (`CONFLICT_LEAD_RE`), not a governed authority, and visibly under-covers the surrounding paragraph.
4. Shows a domain-mismatched IDL as hero "broader context" (One-carbon/MCV-family pattern) while the correctly hepatic-aligned IDL ("Liver Stress Pattern") exists but is hidden as `clinical_only`.
5. Has **no `consumer_display_label` field anywhere on `ClinicalFindingV1`** — there is no DTO surface to carry an approved consumer title even once one is authored.
6. Still shows the wrong cluster ("Cardiovascular") as "headline" framing in `SystemUnderstandingSection`/balanced-systems copy.

The investigation itself splits these into two classes: items 3, 4, 6, and the deduplication/enum-stripping in 1–2 are **fixable without medical or product judgement**; a governed consumer label (item 5) and any urgency-in-prose wording are **not** — they require a product/clinical copy decision, the same class of decision already gated by the existing dual-authority model (Head of Medical Research + Anthony ratification) used earlier in the programme.

## Readiness assessment by authority surface

| Surface | Stable for consumer-page consolidation? |
|---|---|
| Clinical finding & prioritisation authority | **Yes.** Independently audited PASS, merged, no open defects. |
| Analysis regeneration / result-version authority | **Yes.** Independently audited PASS this session; closes `CF-ARCH-CONV-VERSION-1`. |
| Narrative-report authority (`narrative_report_v1`) | **No.** Legacy, MCV-led, only partially suppressed by a text-pattern heuristic — the single largest blocker. |
| IDL / pattern-label authority | **Partially.** Subordinate positioning is structurally correct; content is domain-mismatched against the hepatic lead in this case. |
| Cluster / primary-driver / system-understanding authority | **No.** Frontend-generated bridge copy still names the wrong system as headline when concern-set authority is active. |
| Clinician-report / advanced-view authority | **Yes, as a demoted secondary surface.** Confirmed correctly gated behind `clinicalConcernAuthority` in the CLIN-PRIORITY-CORE-1 audit; legacy MCV fields visible only in advanced/clinician views is acceptable. |
| DTO support for governed consumer labels/narratives | **No.** `consumer_display_label` does not exist on the finding contract — this is the concrete backend gap blocking the programme. |
| Legacy fallback and suppression rules | **Partially.** The "concern set absent" fallback path is clean and tested; the "concern set present, suppress conflicting legacy text" path is a best-effort regex, not a contract, and is proven incomplete by the UAT investigation. |

## Readiness verdict for consumer presentation work

**Do not begin the full consumer-copy and presentation-authority programme as one undifferentiated package now.** The backend ranking/versioning foundations it would sit on are genuinely stable (both independently audited this session). But the specific next step the evidence points to — governed consumer display labels — depends on a product/clinical decision and a DTO field that do not yet exist. Starting broad frontend copy work now risks building UI against an unstable assumption (which IDL titles get reused vs. new copy authored; whether urgency ever appears in consumer prose) that could force rework once that decision lands.

A **bounded subset is safe to start immediately**: the structural/suppression fixes the UAT investigation itself classifies as not requiring medical or product judgement (enum/label leakage removal, conflicting-legacy-narrative suppression, deduplication, wrong-cluster-headline fix). These do not depend on the outstanding product decision and do not risk rework.

## Recommended next package sequence (three to five)

1. **`FE-RESULTS-PRESENTATION-STRUCTURE-1`** (immediate, bounded, frontend-only) — remove raw enum/label leakage from narrative prose to metadata-only display; suppress conflicting legacy `narrative_report_v1`/IDL/cluster fragments when `clinical_concern_set` authority is active; deduplicate the repeated lead statement; stop naming a mismatched cluster as "headline." No clinical, product, or ranking change. Matches the UAT investigation's own §10 "fixable without medical judgement" list exactly.
2. **Consumer-label product/clinical decision** (not an implementation SOP — a scoping/ratification package) — Head of Medical Research + product authority decide: (a) approved consumer display title per finding_type (starting with HEP-F1/CN-F7), (b) whether/how urgency appears in consumer prose, (c) whether to reuse existing IDL retail titles as concern-set lead titles or author new copy. This is the same decision class already used for prior ARCH-CONV Gate-2 ratifications and is the long-standing carry-forward first flagged in CLIN-PRIORITY-CORE-1's closure ("final consumer serious-result wording").
3. **Backend DTO addition** — add an optional `consumer_display_label` (and, only if Package 2 authorises it, a short approved discuss-first sentence) to `ClinicalFindingV1`/`ConsolidatedConcernSet`. Additive only; no ranking, threshold, or activation change. Standard/contract-adjacent risk given prior classification patterns in this programme.
4. **`FE-RESULTS-CONSUMER-COPY-BOUNDARY-1`** (the UAT investigation's own named next task) — wire the governed label from Package 3 into hero, body overview, Clinical Priority, and Primary Finding surfaces, replacing the humanize-fallback. Entry criteria: Packages 2 and 3 complete.
5. **Register hygiene** (parallel, non-blocking, documentation only) — append the missing BUILD_DELIVERABLE_REGISTER.md entries for CLIN-PRIORITY-RESULT-REGEN-1 and `fix/uat-alt-prioritisation`, and update the day-one architecture Active Carry-Forward Register to mark `CF-ARCH-CONV-VERSION-1` resolved. Can happen at any point; does not gate or depend on 1–4.

## Rationale for sequencing dependencies

Package 1 has no dependency because it touches only frontend suppression/formatting logic already proven safe (no ranking recomputation, no new copy invented). Package 4 cannot precede Packages 2–3 because it needs both an authorised label *and* a field to carry it — attempting it earlier would mean either inventing consumer copy (explicitly prohibited) or wiring against a DTO shape that doesn't exist yet. Package 2 is placed before Package 3 because the DTO shape (single label vs. label + sentence) should follow the decision, not precede it. Package 5 is independent of all of the above and is sequenced last only because it is lowest-consequence, not because it is blocked.

## Items explicitly deferred

- Full schema-level retirement of legacy `primary_concern_mode` (already flagged non-blocking in the CLIN-PRIORITY-CORE-1 audit; safe as-is, opportunistic only).
- R2/R3 quarantines (CV-risk %, FIB-4 consumer finding) — unrelated, unchanged, correctly not activated.
- Package B Wave 2 (homocysteine L-04/L-05/L-06), further Package C waves, P1-4 thyroid domain retry, MR-BATCH-001B Round 2 — all independent long-running tracks; none are inputs to or blocked by the consumer-copy programme and should not be bundled into it.
- Any reopening of the ratified clinical prioritisation model, signal activation, or thresholds — out of scope for this entire sequence; nothing above touches them.

## Recommendation for next SOP to author

Author the SOP for **Package 1 (`FE-RESULTS-PRESENTATION-STRUCTURE-1`)** now — it is bounded, frontend-only, requires no product/clinical decision, and is fully supported by evidence already gathered (this audit + the UAT investigation's surface-to-source map). In parallel, GPT/Anthony should schedule the **Package 2 product/clinical consumer-label decision** as a ratification item, since it is the actual long-pole dependency for the rest of the sequence — but that is a decision package, not an implementation SOP, and this audit does not author it.

## Provisional nature of this sequencing recommendation

This sequence is a repository-grounded recommendation for programme planning, not an authorisation to implement. It reflects current evidence only; if either the CLIN-PRIORITY-RESULT-REGEN-1 or `fix/uat-alt-prioritisation` branches change materially before merge, or if the product/clinical decision in Package 2 lands differently than scoped here, this sequence should be re-checked against the then-current repository state before an SOP is issued.
