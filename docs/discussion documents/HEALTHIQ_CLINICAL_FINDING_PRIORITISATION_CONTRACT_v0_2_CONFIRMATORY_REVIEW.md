---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001-REVIEW-V02
title: Confirmatory Independent Medical Review — Prioritisation Contract v0.2
reviews: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.2
compares_against: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001-REVIEW (v0.1 review)
reviewer_role: Independent medical research and red-team reviewer
review_type: CONFIRMATORY (not a fresh full review)
verdict: VALIDATE_WITH_REQUIRED_REVISIONS
---

# Confirmatory Review — Contract v0.2

## 0. Summary

All fifteen defects raised against v0.1 are resolved. The clinical model is unchanged, which is correct — it was not the problem.

Three new defects were introduced by the revisions themselves. All three are sentence-level and none requires redesign, but two sit in the tier-floor and override machinery, which is precisely where the v0.1 review said silent failures would recur. They are recorded as N1–N3 and must be corrected before the hepatic pilot is authored.

The verdict is `VALIDATE_WITH_REQUIRED_REVISIONS` rather than `VALIDATE` on the strength of N1 alone: §12.2 opens a downgrade route that the §6.1 floor rule does not cover.

---

## 1. Prior-defect disposition

| ID | Defect | Status | Where resolved | Note |
|---|---|---|---|---|
| B1 | Confidence leakage via clinical significance | **RESOLVED** | §4.3, §8, §10, §18.3 | §4.3 now reads "given that this finding is present as characterised" and states significance is a property of the finding, not of certainty. Reinforced three times: §8 ("must not lower severity, clinical significance, tier or lead eligibility merely because they are absent"), §10's reframed priority question, and §18.3 as a standalone prohibition. Belt, braces and a third fastening. Correctly done. |
| B2 | Undefined tier-assignment function | **RESOLVED** | §6.1 | Two-tier derivation, floor rule, one-tier promotion cap, and an explicit exclusion list. See N2 for a wording ambiguity in the floor sentence. |
| B3 | Missing no-concern / all-normal policy | **RESOLVED** | §16 | Stronger than requested. The five must-state items and four must-not-imply items are the right shape, and requiring the same governance as Tier 0 language is correct. See N3 for one framing caution. |
| B4 | Unaddressed regulatory scope | **RESOLVED** | frontmatter `regulatory_status`, §22, §23.4, §23.6.4, §25.2 | §22 is materially better than the minimum asked for. Stating that ratification does not determine non-device status, and that disclaimers do not settle the question, are the two sentences that matter. Naming Tier 0 permissibility as itself subject to regulatory determination (§22.5) was not requested and is a good addition. |
| R1 | Contextual role assignable to serious findings | **RESOLVED** | §4.8, §18.17 | |
| R2 | Trend permissive where mandatory | **RESOLVED** | §12.1, §12.2, §20.13 | Change-defined / change-modified split is correct. Baseline validity delegated to domain rules with age and comparability checks. See N1. |
| R3 | Acceptance case asserted an underivable answer | **RESOLVED** | §19 | Reclassified as regression fixture; §19.3 evidence discipline explicitly forbids reverse-engineering thresholds and requires adjudication on discrepancy. §19.2 qualifies Tier 1 as "subject to independent hepatic rule derivation and adjudication." No residual inconsistency with the deferred hepatic work in §20.1. |
| R4 | Overrides unconstrained | **RESOLVED** | §13, §18.18, §18.19 | Six-property requirement including directional constraint. See N2. |
| R5 | In-range values cannot form findings | **RESOLVED** | §3.1, §3.2, §18.21 | The platelet trend example in §3.2 is a good concrete anchor. |
| R6 | Co-lead cap unspecified | **RESOLVED** | §7.4, §23.3 | Cap ratified by product with recommended maximum two; overflow behaviour specified. |
| R7 | No Tier 1 volume control | **RESOLVED** | §15.1, §15.2, §23.3 | The four compression prohibitions, particularly "conceal that additional Tier 1 findings exist," close the failure mode. |
| R8 | "Tier 0 normally empty" stated as property | **RESOLVED** | §6.2, §24 | Replaced with membership-by-rule plus empirical monitoring. §24's "firing rates are empirical safety indicators, not targets" is the correct formulation, and adding under-firing as a review trigger was the right call. |
| R9 | No Tier 0 operational pathway | **RESOLVED** | §17, §20.17, §23.6.8 | Nine-item pathway including the artefact-retraction case and duty-of-care implications. Gating production release on it is appropriate. |
| R10 | Reliability sequenced before urgency | **RESOLVED** | §5, §4.6, §11 | Reliability now sits after tier assignment as an annotation, with §11 stating explicitly it is not an input to urgency, severity or tier. §7.3 also adds analytical-reliability status to the lead-selection exclusion list, which was not requested and is correct. |
| R11 | Orphan Tier 3 findings undefined | **RESOLVED** | §6.5, §18.20 | Two-branch resolution plus "must remain reconcilable with the raw result." |

**Prior-defect result: 15 of 15 RESOLVED.**

---

## 2. New defects introduced by the revisions

### N1 — §12.2 creates a downgrade route outside the floor rule

**Severity: material. Must be corrected before the hepatic pilot.**

§6.1 constrains downgrades from clinical significance and actionability. §13 constrains downgrades from overrides. §12.2 states that trend "may then increase or **decrease** concern according to an explicit governed rule" — and nothing constrains it.

Three readings are available to a domain rule author, and the contract does not choose between them: trend adjusts within-tier ordering only (§7.2 item 5 suggests this); trend acts through a governed override and inherits §13's floor protection; or trend independently lowers tier.

Under the third reading, a rule such as "potassium is chronically stable in this patient, therefore reduce concern" could lower a finding below its urgency floor. That is the exact class of silent downgrade the floor rule exists to prevent, reached by a route the floor rule does not name.

**Required correction.** State in §12.2 that trend acts either within-tier or through a governed override subject to §13, and that trend may not lower a finding below the floor set by urgency or severity. One sentence.

### N2 — Two ambiguities in the tier algebra

**Severity: minor wording. Both should be corrected.**

**N2a — "higher-priority" is ambiguous under inverted tier numbering.** §6.1 reads: *"The initial tier is the higher-priority of those two tiers."* Tier 0 is the most serious and numerically lowest. A rule author or implementer reading "higher" numerically selects Tier 3 — exactly inverting the intended behaviour. The rest of the contract makes intent obvious, but this sentence is the single load-bearing statement of the tier algebra and should not depend on context to be read correctly.

**Correction:** *"The initial tier is the more serious of the two — that is, the numerically lower tier."*

**N2b — override promotion depth is unstated relative to the §6.1 cap.** §6.1 caps promotion by clinical significance and actionability at one tier. §13 places no depth limit on override promotion. This is almost certainly intentional — a combination rule must be able to promote a finding from Tier 2 to Tier 0 in one step, and the v0.1 review supported that. But as written, a rule author who wants a two-tier promotion can route it through an override to avoid the §6.1 cap, and nothing in the document says whether that is legitimate use or circumvention.

**Correction:** state in §13 that governed overrides may promote across more than one tier where the clinical rule requires it, and that this is the only permitted route for multi-tier promotion.

### N3 — §16 folds "could not assess" into the no-concern output class

**Severity: minor framing. Should be corrected in the language templates at the latest.**

§16 lists *"incomplete data that prevents meaningful assessment"* alongside all-normal and Tier 2-only panels as triggers for the same governed output. These are clinically different situations. "We looked and found little of concern" and "we could not meaningfully assess this" carry different implications, and a shared output risks the second being received as the first — which is the false-reassurance hazard §16 exists to prevent.

The required content in §16 items 1 and 3 partially covers this, but the framing is set by which output class fires, not by a clause inside it.

**Correction:** separate the insufficient-data case as a distinct output class, or require the language templates (§20.15) to lead with the assessment limitation rather than with the findings summary when it fires.

---

## 3. Specific checks requested

| Check | Result |
|---|---|
| New clinical contradiction | **One found.** §5 sequences "recognised combination and override rules" *before* "concern-tier assignment", but §13 defines overrides as moving findings *across tiers*. At the point the override step runs, no tier exists to move across. Either overrides act on urgency and severity classes pre-tier (in which case §13's wording should say so and the floor language should refer to urgency/severity classes rather than tiers), or the override step belongs after tier assignment. This is a sequencing inconsistency, not a clinical error, but it will be resolved by default during the hepatic pilot if left. Fold into the N2b correction. |
| New route for confidence to affect prominence | **None found.** B1's fix closes the §4.3 path. §7.3, §6.1 and §18.3 each independently block re-entry. |
| New route for panel completeness to affect prominence | **None found.** §6.1 and §7.3 both name panel completeness explicitly; §8 closes the missing-marker route. |
| New route for presentation logic to affect prominence | **None found.** §15.2's four compression prohibitions and §18.11 are adequate. |
| Ambiguity in tier floors | **Yes — N1 and N2a.** |
| Ambiguity in promotion rules or overrides | **Yes — N2b and the §5 sequencing point.** |
| Unsafe wording around Tier 0 | **None found.** §6.2 and §17 are appropriately cautious. §17's inclusion of the artefact-retraction case and of duty-of-care implications is the right level of seriousness. |
| Unsafe wording around no-concern outputs | **N3 only.** The four must-not-imply clauses are otherwise well drafted, particularly the exclusion of "symptoms are explained or excluded". |
| Unsafe wording around regulatory status | **None found.** §22 does not overclaim in either direction. `regulatory_status: OPEN_SPECIALIST_REVIEW_REQUIRED` in the frontmatter is appropriate. |
| Fixture / deferred-threshold inconsistency | **None found.** §19.2's qualification and §19.3's evidence discipline resolve R3 cleanly. §19 and §20.1 are consistent. |

---

## VERDICT: VALIDATE_WITH_REQUIRED_REVISIONS

Required revisions: **N1, N2a, N2b (including the §5 sequencing point), N3.**

These are four sentence-level corrections. No section requires redesign and no clinical position in the document is in question. The verdict is not `VALIDATE` solely because N1 leaves an unconstrained downgrade path in the tier machinery, and the v0.1 review's central lesson was that unconstrained paths in this machinery close quietly and reopen under delivery pressure.

### Readiness

**1. Anthony's product ratification — READY, proceed now.**
None of N1–N3 touches a decision on Anthony's §23.3 list. The lead-plus-tiered model, co-lead cap, tier visibility, Tier 1 volume control, tier naming, missing-data transparency, no-concern presentation, governance authority and threshold versioning are all ratifiable as drafted. Ratification need not wait for the corrections.

**2. Specialist regulatory review in parallel — READY, and this should start immediately.**
§22 gives a regulatory adviser everything needed to scope the question. This is the longest-lead item in the programme and may constrain tier naming, urgency wording, action recommendations, supported users and market scope. Starting it after the hepatic pilot would risk rework of clinically governed content. N1–N3 do not affect it.

**3. Hepatic pilot specification after ratification — NOT READY until N1 and N2 are corrected.**
The pilot must assign tiers, apply overrides, and handle trend. All three corrections sit in exactly that machinery. A pilot authored against the current text will resolve N1, N2b and the §5 sequencing question by implicit choice, and those choices will then be treated as precedent by every subsequent domain. Correct the four sentences first; this is hours of work, not a revision cycle.

No further independent medical review is required after the corrections. A confirmation by the Head of Medical Research that the four sentences read as intended is sufficient to close this out.
