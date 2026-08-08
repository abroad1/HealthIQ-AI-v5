# HealthIQ V5 vs V6 — Strategic Architecture Viability Reassessment

**Purpose:** decision-support reassessment of the ratified `GO — RETAIN V5` decision, in light of repository-reality evidence discovered after that decision. No implementation, no code changes, no medical policy. For GPT + Anthony reconciliation.
**Method:** original decision material read in full; three parallel disjoint research passes (guardrail-failure + registry-determinism diagnosis; 15-category architecture-debt inventory; V6 reuse asset assessment), each independently citing file evidence, one high-severity claim independently re-verified by the coordinator before inclusion.

## A. Executive recommendation

```
RETAIN_V5
```

**Confidence: MEDIUM-HIGH** (down from the original decision's HIGH/MEDIUM-HIGH — not because V5 has gotten worse, but because this reassessment found the assurance mechanisms protecting it are less robust than the original decision assumed).

**Concise rationale:** substantial genuine convergence progress has been made since the original decision (one of three minimum-safe packages fully closed, another's flagship item closed, roughly half of the largest package's content-compilation work done). The newly-discovered lipid-authority defect is real, systemic, and serious — but it is a *missing validation invariant* between two existing registries, not evidence that V5's architecture is unrecoverable, and the fix is bounded and well-understood. The reuse assessment confirms the overwhelming majority of governed clinical/research content is already cleanly portable regardless of which option is chosen — meaning a V6 rewrite would not avoid the medical-review burden, would discard real progress already banked, and would introduce a continuity-break risk the evidence does not show V5 currently carries. This recommendation is conditioned on urgently closing the specific invariant gap found (§8 decision threshold below) — this is not an unconditional "everything is fine."

## B. Previous-decision premise reassessment

Source: `docs/architecture/ARCH-CONV_v5_completion_vs_v6_decision.md` (2026-07-27), kill-criteria table §3.

| Previous premise | Evidence then | Evidence now | Status | Consequence |
|---|---|---|---|---|
| 11.1 No cohort-isolation failure | Pilot cohort isolated; PKG1-3 + CORRECT-1 completed without whole-estate rewrite | No new evidence of cohort-isolation failure found in this pass | **STILL TRUE** | No change |
| 11.2 No canonical-lineage failure | Pass 3 lineage recoverable for material INCLUDE cohorts | Independently re-counted `source_spec_id` provenance: **21 of 194 manifests** now carry it, up from the baseline's claimed 0 — genuine progress, though the current-state baseline document itself is stale on this number | **STILL TRUE, STRENGTHENED** | Current-state baseline needs a documentation correction (separate from this reassessment) |
| 11.3 No authority-retirement failure (pilot) | "Pilot COMPILED_ACTIVE exclusivity proven; REJECTED frame inert" | **The pilot-specific claim remains true** (not retested, not contradicted). But a **non-pilot REJECTED frame was found NOT inert**: three lipid signals explicitly rejected by ratified Gate1+Gate2 decision (`ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md:61-63,173-175`, 2026-07-28) are runtime-loaded today, traced to a 2026-07-31 commit (`a260c5376`) that bootstrapped the runtime-activation register by snapshotting whatever was already running in production, with **zero cross-check** against the medical-decision registry that correctly recorded the rejection | **PARTIALLY TRUE — pilot claim holds, generalization beyond pilot INVALIDATED** | This is the single most consequential finding of this reassessment — see §8 |
| 11.4 No unfixable cross-layer duplication | "Residual duals are localised... not uncentralisable" | Debt inventory confirms: legacy-vs-compiled WHY coexistence is real and large (42 legacy targets, 22 now compiled = 52%) but resolved through a **single real selector** (`resolve_frame_why_authority` in `root_cause_compiler_v1.py`) enforcing compiled-first exclusivity — not simultaneous dual-answering. The debt is retained dead legacy code after compilation, not unfixable duplication | **STILL TRUE** | No change to this premise; separately, the *activation*-layer duplication (5 overlapping "is this signal allowed to run" mechanisms — item 4 below) is a different, newly-surfaced concern not addressed by this premise at all |
| 11.5 No scope-growth ceiling breach (>1 mandatory correction) | CORRECT-1 was the single authorised correction | Since then: multiple additional correction-shaped packages have run (PKGB-1, PKGC-1, PKGC-2, ARCH-CONV-I-ALT-IDPROV-1, THYROID-FT3-TSH-FIRING-FIX-1) | **PARTIALLY TRUE / criterion needs re-reading** | These were mostly *planned* Package A/B/C wave content and one genuine bug fix, not runaway scope growth — but the criterion as originally framed ("single authorised correction") no longer literally holds; recommend GPT re-baseline this criterion's wording rather than treat it as breached |
| 11.6 No time/cost ceiling breach | "Not evidenced" | No formal ceiling-breach record found now either; substantial real work has been completed in the interval, consistent with steady (not stalled, not runaway) progress | **STILL TRUE** | No change |
| 11.7 Medical-review viability (pilot) | "No for pilot; estate completion needs continued capacity but route exists" | The dual-gate (GPT + Anthony) review route has continued operating (multiple Gate1/Gate2 decisions since) — but the lipid finding shows a **ratified rejection can still become runtime-active downstream of review**, meaning review viability alone is not sufficient without an enforcement invariant | **PARTIALLY TRUE** | Review process works; enforcement of review outcomes does not yet fully work — see §8 |
| 11.8 No independent-assurance failure | "No — CORRECT-1 closed under human authority with live UAT" | The lipid discrepancy went undetected for 9+ days through everything that ran in that window — kernel gates, baseline tests, multiple subsequent work-package audits — and was found only by an unrelated ad hoc reconciliation exercise, not by any guardrail | **INVALIDATED FOR THE GENERAL CASE** (CORRECT-1's own specific assurance was fine; the broader claim that independent assurance reliably catches authority violations is not supported by this new evidence) | Most consequential secondary finding — see §C, §8 |

## C. V5 systemic-risk assessment

**Confirmed architectural defects (systemic, cross-verified):**
1. **No cross-validation invariant between the medical-authority-decision registry and the runtime-activation registry.** `compiled_why_authority_register_v1.yaml` correctly records the lipid rejection; `package_runtime_activation_register_v1.yaml` was bootstrapped independently, once, by snapshotting production state, and nothing since has reconciled the two. This is the root cause of the headline finding, not a one-off data-entry mistake.
2. **Runtime "is this signal allowed to fire" authority is split across five independent mechanisms**: `package_runtime_eligibility_v1`, `frame_runtime_authority_v1`, `package_activation_register_v1`, `provenance_status_v1`, and an ad hoc `is_launch_critical_package_id` check, all consulted separately inside `SignalRegistry._load` (`backend/core/analytics/signal_evaluator.py:54-94`). This is architecturally consistent with, and likely a structural contributor to, finding #1 — more independent gates means more places a check can be silently absent.
3. **Estate-wide test coverage does not exist as a structural guarantee.** `backend/scripts/run_baseline_tests.py` runs a fixed, curated list of exactly 12 test files — by construction it can only prove what those 12 files assert, not estate-wide behaviour across the ~128-197-signal estate. This is why a defect affecting 3 specific signals could survive multiple "PASS" gates.
4. **Legacy/compiled WHY coexistence is large and will remain so for some time**: 20 of 42 registered legacy targets (48%) have no compiled alternative yet; 31 `pkg_s24_*` legacy-generation packages remain on disk and (per registry) potentially active alongside newer generations.

**Confirmed local defects (isolated, not evidence of a pattern):**
- The thyroid FT3/TSH evaluator fail-closed-on-absent-metric bug (already found and fixed this session, `THYROID-FT3-TSH-FIRING-FIX-1`) — a genuine bug, narrowly scoped, correctly diagnosed and corrected with evidence-backed root cause, not indicative of a broader class.
- A documented, disclosed carve-out in `SignalRegistry._load` for non-standard package locations (`signal_evaluator.py:80-81`) — intentional and commented, not hidden, but is a second, less-governed activation path worth closing eventually.

**Unresolved suspicious behaviour (investigated, not confirmed as defects):**
- The SignalRegistry loaded-signal-count variance (128 vs 183 vs 197 observed across different sessions) was investigated directly this pass: the loader is provably deterministic (sorted glob, no caching, content-hash-verified identical across 5 fresh runs and across repeated in-process instantiation). **Could not be reproduced.** Most likely a transient repo-state artefact from concurrent tooling (e.g. a git worktree operation) during an earlier session, not a registry-determinism defect. Downgrade this from "architecture debt" to "investigated and cleared."

**Historical debt already successfully eliminated:**
- The ferritin-high signal-identity collision (two packages claiming the same signal_id) was fully resolved via a dedicated ADR (`ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1`) — proof the programme can and does resolve exactly this class of problem when it's found.
- The three "separately retained follow-ups" explicitly named as unclosed at the original decision (homocysteine provenance regression, historic waist-unit impact, result-versioning policy) are now **all three closed** (PKGB-1, PKGC-1, CLIN-PRIORITY-RESULT-REGEN-1 respectively) — the bounded-completion model has demonstrably worked for everything it's been pointed at so far.

## D. V6 reuse assessment

| Asset class | Approx size | Reuse as-is | Recompile/revalidate | Rebuild | Do not migrate | Reason |
|---|---|---|---|---|---|---|
| Investigation-spec research | 50 files | ✅ | | | | Pure clinical YAML, zero runtime code coupling |
| Ratified medical decisions (Gate1/Gate2, ADRs, decision registers) | ~12 + 13 + 13 files | ✅ | | | | Portable governance history, architecture-agnostic |
| Biomarker/lifestyle/questionnaire SSOT | 1882 lines | ✅ | | | | Clean canonical data, no embedded code coupling found |
| `ClinicalFinding`/`ConsolidatedConcernSet` contract + `concern_constructor.py` | — | ✅ | | | | Genuinely isolated — only imports same-era CLIN-PRIORITY-CORE-1 modules, no legacy coupling |
| `InsightGraphV1` container | — | | | ✅ (extract concern-set field, don't lift whole) | | Imports 8 legacy contract modules; the container is coupled even though the concern-set contract inside it is not |
| Compiled artefact schemas | — | | ✅ | | | Schema shape reasonable; surrounding dual-authority governance machinery needs simplification, not blind copy |
| 109-scenario acceptance estate | 2 fixture files | ✅ | | | | Portable JSON input→expected-output pairs, separate from runner code |
| KB packages: `pkg_kb*` generation | ~150 of 194 (≈77%) | ✅ | | | | Pass-3-era, cleaner identity |
| KB packages: `pkg_s24_*` + `KBP-00xx` legacy generation | ~32 of 194 (≈16%) | | ✅ (identity reconciliation) | | | Legacy naming/identity, not necessarily bad content — needs reconciliation, not rewrite |
| Test panels / regression fixtures | 31 files | ✅ | | | | Realistic, portable panel data |
| Safe consumer content (interventions, pathway explainers) | ~430 lines combined | ✅ | | | | Content-only YAML |
| Pure UX/design-system components | 15 files sampled, 0 medical-logic hits | ✅ | | | | Genuinely presentation-only where sampled; higher-level result components not sampled, likely carry logic |
| `SignalRegistry` loader + 5-mechanism activation gating | — | | | | ✅ | V5-specific orchestration; this is exactly the "kernel" a controlled migration would replace |
| Legacy root-cause YAML wiring (uncompiled targets) | 20 of 42 targets | | | | ✅ (loader only — underlying research is portable, see row 1) | Runtime-loader-specific wiring, not a content asset |

**What a minimum clean V6 kernel would need to accept, per the reuse fork:** investigation-spec YAML as canonical input, the SSOT files as-is, the concern-construction contract lifted largely intact, the acceptance-scenario fixtures as its day-one regression suite, the ~150 clean-generation KB packages directly plus the ~32 legacy-generation packages after reconciliation, all governance/decision documents as historical record, and the UX design-system layer directly. It would need to newly build: a single-mechanism signal-activation gate (replacing the current five), a loader without the current branching complexity, and a clean home for the concern-set contract without dragging in the seven other legacy contract modules `InsightGraphV1` currently bundles it with.

## E. Comparative risk matrix

| Dimension | V5 convergence (RETAIN) | V6 clean foundation (BUILD) |
|---|---|---|
| Medical safety | MEDIUM — real gap just found and not yet closed, but a known, bounded, fixable gap | MEDIUM — same medical content, same review burden; a rebuild does not remove medical-safety work, and introduces a fresh chance to reintroduce equivalent gaps during a rewrite |
| Architectural comprehensibility | LOW-MEDIUM today (5-mechanism gating, dead legacy branches) — improves as Package A/B complete | HIGH once built, but only after absorbing full re-integration cost |
| Determinism | Loader itself confirmed deterministic this pass (cleared, not a defect) | Would be built deterministic from scratch, at cost |
| Testability | MEDIUM — estate-wide gap confirmed real (12-file curated baseline), independently fixable without a rewrite | Would need building from scratch either way |
| Provenance | MEDIUM, improving (21/194 clean vs. baseline's stale claim of 0) | Would need full re-attachment; V5's Pass-3 lineage work would still be the source material either way |
| Hidden-defect risk | Confirmed non-trivial (this session found one live instance) — but the exact class of risk is now named and fixable | A rewrite carries its own hidden-defect risk during the transition, on top of not eliminating the medical-content risk |
| Migration risk | Low — no migration, in-place completion | HIGH — dual-run/cutover, re-integration of FE/auth/billing/persistence/cards not proven necessary by any evidence found this pass |
| Engineering effort (qualitative, no hour estimates per instruction) | Bounded — roughly half of the largest package's content work already done | Would still need the same content-compilation effort, **plus** platform rebuild |
| Clinical/research rework | LOW — the reuse assessment shows research/decision content is almost entirely portable regardless of option | Same as V5 for content; zero saved by rebuilding |
| Ability to reuse existing work | HIGH — demonstrated concretely in §D | HIGH for content, LOW for the orchestration layer being discarded |
| Future maintainability | Improves directly as Package A/B/C-style work continues; the gating-mechanism consolidation is a known, nameable target | Would be better once done, unproven that it's cheaper to reach |
| Enterprise-readiness | Not yet — explicitly not claimed by this reassessment | Not yet either, and further away given full rebuild timeline |
| Likelihood of continuing to discover legacy contradictions during beta prep | MEDIUM — this pass found one; the pattern (bootstrapped-without-cross-check) suggests there could be others of the *same* class not yet found (worth a targeted sweep, not a full rewrite) | Would not eliminate this risk — new code can encode new versions of the same class of gap if the missing invariant (cross-registry validation) isn't designed in from day one either way |

## F. What would have to happen next

**If RETAIN_V5 (recommended):**
- Close the specific missing invariant: a validator that cross-checks `package_runtime_activation_register_v1.yaml` entries against `compiled_why_authority_register_v1.yaml`'s rejected/retired states, run at CI/gate time, not just at registry-bootstrap time.
- A targeted sweep for other instances of the same failure class (ratified-rejected content that entered a registry via a bootstrap/snapshot mechanism rather than an explicit reviewed activation) — bounded in scope, not a full estate audit.
- Complete the remaining ~48% of Package A's content-compilation work (already itemised by domain in the prior residual reconciliation).
- Confirm Package B's full scope beyond the homocysteine item (layered why-it-matters selector, fallback quarantine, family-aggregation policy) — not verified closed this pass.
- Expand estate-wide test coverage beyond the current 12-file curated baseline, so the next instance of this defect class is caught by a gate, not by chance.
- Consolidate the five signal-activation gating mechanisms toward one canonical gate — this is the "controlled kernel" work the reuse assessment scoped, worth doing as an in-place refactor rather than a full V6, given how contained the reuse assessment shows it to be.
- Full-estate regression/replay validation once the above land.

**If BUILD_V6 (not recommended, listed for completeness):**
- All of the medical-content compilation and review work listed above would still be required — nothing here is avoided.
- Additionally: re-integration of frontend, auth, billing, persistence, and card-rendering surfaces; a dual-run or cutover migration strategy; re-attachment of provenance/lineage continuity; rebuilding the acceptance-scenario harness around new runtime code (even though the fixtures themselves are portable); and absorbing a new round of hidden-defect risk inherent to any large rewrite, on top of the medical-content risk that doesn't go away.

## G. Final decision argument (ignoring sunk cost)

Judged strictly from today's repository state forward, not from what has already been invested: the question is whether the remaining problem is "V5's architecture is fundamentally unable to enforce medical authority" or "V5 is missing one specific, nameable validation step, discovered late, in an otherwise largely-working bounded-convergence programme." The evidence gathered this pass supports the second reading. The lipid-authority defect is real and serious, and this reassessment does not minimise it — it is the reason confidence is MEDIUM-HIGH rather than HIGH. But its own root cause (a one-time bootstrap-by-snapshot with no cross-registry check) is precisely identified, has not been shown to be one of several independent leak paths, and is fixable without discarding anything. Meanwhile, the reuse assessment shows that the assets a V6 would most want — clean research, ratified decisions, a genuinely well-isolated clinical-prioritisation contract, portable test estates, safe consumer content, a clean UX layer — are already separable from the parts that actually need work (the loader and its five-mechanism gating). That is close to the exact shape the original decision predicted a full rewrite would face — "would not remove the medical-review or compile burden; would add platform migration cost while the target authority model is already proven" — and nothing found this pass overturns that logic. What has changed is narrower and more useful than a verdict reversal: it names exactly which piece of V5's machinery (registry cross-validation, gating-mechanism count, estate-wide test coverage) needs attention next, ahead of continuing Package A/B content work.

## Stop condition

Per the brief, this reassessment stops here for GPT and Anthony reconciliation. No implementation, migration, or sprint sequencing is authorised by this document.
