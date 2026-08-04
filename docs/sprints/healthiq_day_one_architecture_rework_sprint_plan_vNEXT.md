# HealthIQ AI — Day-One Architecture Rework Sprint Plan vNEXT

**Supersedes (for sequencing purposes only):** `healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`
**Does not supersede:** any clinical, product, or architecture decision already ratified/approved. Those stand unchanged.
**Status:** Provisional — presented for Anthony/GPT review alongside `CLIN-PRIORITY-CORE-1`
**Prepared by:** Claude Code, Stage 0 architecture and package-definition review

## 1. Why this reset

The FINAL plan sequenced work (`ARCH-RT-0` through `ARCH-RT-5`) before the Cross-Domain Clinical Findings and Prioritisation programme existed as a ratified target. Two things have since changed:

1. **The clinical and product prioritisation policy is now complete and approved** — contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4, closure report v0.4, the 109-scenario acceptance estate (approval pack v1.2), the clinician-first product ratification, and the architecture-hardening report are all in force. This did not exist when the FINAL plan was authored.
2. **Repository inspection (`CLIN-PRIORITY-IMPLEMENTATION-RESET-1_repository_inspection.md`) found that some FINAL-plan sequencing assumptions no longer match repository reality** — most materially, `SignalRegistry`'s `activation_key` multi-frame keying (FINAL plan's "ARCH-RT-2 identity runtime pilot") is **already implemented and live**, not a pending pilot.

This plan does not discard the FINAL plan's completed work. It re-sequences what comes next around the now-ratified programme objective and corrects sequencing assumptions repository evidence has overtaken.

## 2. Preserved: architecture work already completed

Nothing here is redone or reopened:

- **Sprint 0** (`WAVE1-EQUIV1_total_bilirubin_false_missing_fix`) — resolved, per the carry-forward register.
- **Sprint 1** (`ARCH-RT-0_inventory_and_identity_decisions`) — resolved; ADR-RT-001 through ADR-RT-004 ratified and, per this inspection, substantively implemented.
- **`activation_key` multi-frame registry** (originally scoped as part of Sprint 3 `ARCH-RT-2`) — **repository-confirmed already live** in `SignalRegistry` (`signal_evaluator.py:26-202`). Re-verify at Package A start (§4 of `CLIN-PRIORITY-CORE-1`) rather than re-implement.
- Sprint 2's compile-manifest and provenance foundation work, where completed, is preserved and reused directly by the new package's compiled prioritisation artefact.

## 3. Obsolete sequencing assumptions — corrected, not carried forward

| FINAL plan assumption | Correction |
|---|---|
| Card-evidence vertical slice (`ARCH-RT-3`) and hypothesis/root-cause slice (`ARCH-RT-4`) must precede any further intelligence-layer work | Neither is a prerequisite for Cross-Domain Clinical Findings and Prioritisation. They address a different layer (Health Systems Card evidence, WHY/root-cause compilation) with no architectural dependency on finding consolidation or tiering. Moved to the follow-on register (§4) as `OPTIONAL_FUTURE_CAPABILITY` / `REQUIRES_DEEPER_INSPECTION`, not sequenced ahead of the core package. |
| "ARCH-RT-2 identity runtime pilot" is upcoming, unstarted work | Repository-confirmed already implemented (§2). Re-verify only; do not re-sequence as future work. |
| Full estate regeneration (`ARCH-RT-5`) is the natural next large step after the identity pilot | Superseded as the next objective. The programme objective is now Cross-Domain Clinical Findings and Prioritisation; estate regeneration for other purposes (card evidence, root-cause) remains valid future work but is not next. |

## 4. Next implementation outcome

> Complete the Cross-Domain Clinical Findings and Prioritisation programme so HealthIQ can surface current and longitudinal findings in the already-ratified clinical priority order.

Delivered by one bounded package: **`CLIN-PRIORITY-CORE-1`** (full definition: `docs/sprints/CLIN-PRIORITY-CORE-1_cross_domain_clinical_findings_and_prioritisation.md`).

## 5. Minimum safe sprint count and anti-micro-sprint position

**One implementation package, with internal checkpoints, not multiple sprints.**

1. **Product outcome:** a working, auditable, deterministic pipeline that consolidates governed signals into clinical findings, assigns urgency/severity/tier, resolves lead/co-lead/no-forced-lead, incorporates governed trend effects, and exposes the result through an extended DTO to a render-only frontend — proven end-to-end against the hepatic domain first, then extended to the remaining five domains.
2. **Minimum safe sprint count: 1.** The architecture-hardening report already established (and this inspection reconfirms) that the model, identity, concern-construction service, and Tier 0 gate cannot be meaningfully tested without at least one real domain's rules running through them. Splitting model-definition, compiler, service, DTO extension, and hepatic-pilot fixtures into separate sprints would recreate exactly the governance overhead the anti-micro-sprint rule exists to prevent, and none of those pieces is independently shippable or independently testable.
3. **Why not split further:** no genuine safety-separation reason applies. Risk class is uniformly HIGH/MIXED across all sub-components (they all touch Intelligence Core). File ownership does not conflict. No sub-component requires a different formal authority approval than another. The six-domain rollout (internal checkpoint 2, §6) is a genuine sequencing dependency on the hepatic pilot succeeding first — that is handled as an **internal checkpoint inside one package**, not a second package, because it uses the same architecture, the same compiler, the same service, and the same test harness; only the domain content differs.

## 6. Internal checkpoints (within `CLIN-PRIORITY-CORE-1`)

1. **Checkpoint 0 — Phase 0 verification.** Confirm `SignalRegistry` activation-key behaviour live; confirm/deny live FIB-4/CV-risk computation paths (inspection report §10 risk 2); confirm forbidden-path boundaries.
2. **Checkpoint 1 — Hepatic pilot.** Canonical model, identity, concern-construction service, Tier 0 gate, DTO extension, hepatic-domain compiled artefact, hepatic acceptance scenarios (approval pack v1.2 §9.1) passing.
3. **Checkpoint 2 — Estate rollout.** Extend to haematology, renal/electrolyte, iron/inflammatory, thyroid/endocrine, cardiometabolic/nutritional; full 109-scenario estate passing.
4. **Checkpoint 3 — Trend integration.** Governed trend effects (§8 of the inspection report) wired into within-tier ordering and change-defined findings; trend-tier-promotion explicitly left unimplemented and recorded as follow-on.
5. **Checkpoint 4 — Frontend and closure.** Frontend consumes the new DTO field, retires `technical_tiebreak_lead`-dependent UI logic, full regression, closure documentation.

STOP gates between checkpoints are specified in the package definition (§9).

## 7. Provisional follow-on register

| Item | Classification |
|---|---|
| Tier 0 operational escalation pathway (contract §17, R1) | `ESSENTIAL_BEFORE_RELEASE` |
| Consumer-facing disease-name release (R4) | `ESSENTIAL_BEFORE_RELEASE` |
| Cardiovascular-risk calculation activation (R2) | `ESSENTIAL_BEFORE_RELEASE` (capability-specific) |
| FIB-4 activation (R3) | `ESSENTIAL_BEFORE_RELEASE` (capability-specific) |
| Population exclusions / intended-purpose wording (R5) | `ESSENTIAL_BEFORE_RELEASE` |
| Renal/electrolyte release with Tier 0 suppressed (R6) | `ESSENTIAL_BEFORE_RELEASE` |
| Questionnaire pregnancy question + server-side enforcement (`CF-QUESTIONNAIRE-CONTEXT-1/2`) | `ESSENTIAL_BEFORE_RELEASE` |
| Trend-triggered tier-promotion override rule | `REQUIRES_DEEPER_INSPECTION` — needs a future bounded medical adjudication before it can be classified further |
| Health Systems Card evidence vertical slice (FINAL plan `ARCH-RT-3`) | `OPTIONAL_FUTURE_CAPABILITY` |
| Compiled hypothesis / root-cause slice (FINAL plan `ARCH-RT-4`) | `OPTIONAL_FUTURE_CAPABILITY` |
| Full estate regeneration beyond this programme's scope (FINAL plan `ARCH-RT-5`) | `OPTIONAL_FUTURE_CAPABILITY` |
| Frontend UI built around `technical_tiebreak_lead` | `ESSENTIAL_TO_CORE_FUNCTION` — must be retired as part of Checkpoint 4, not deferred |
| Emergency-service routing / user follow-up monitoring | `OUT_OF_SCOPE_DISCARD` — outside HealthIQ's product boundary entirely, not merely deferred |
| Laboratory-provider integrations | `OUT_OF_SCOPE_DISCARD` for this programme |
| Specialist pregnancy interpretation ruleset | `RETAIN_QUARANTINED` — contract §26 interim policy stands; a dedicated future ruleset is separate work |
| Broad questionnaire redesign (beyond the two essential items above) | `OPTIONAL_FUTURE_CAPABILITY` |
| Existing `precedence_engine`/cluster-level arbitration | `RETAIN_QUARANTINED` from this programme — left running for its existing purpose, not touched, not extended to clinical findings |
| Final regulatory release approval | `ESSENTIAL_BEFORE_RELEASE` |

## 8. Dependencies that block implementation versus release only

**Block implementation (must resolve before/within `CLIN-PRIORITY-CORE-1`):** none outstanding — all clinical and product authority is ratified; the one architecture verification item (live FIB-4/CV-risk path) is a Phase 0 checkpoint inside the package, not a pre-package blocker.

**Block release only (do not block this package):** R1 (Tier 0), R2 (CV-risk), R3 (FIB-4), R4 (disease-name), R5 (population/intended-purpose), R6 (renal/electrolyte Tier 0 suppressed release), questionnaire remediation. All are represented correctly and fail-closed by the package; none is activated by it.
