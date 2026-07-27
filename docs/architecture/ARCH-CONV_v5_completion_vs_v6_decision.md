# ARCH-CONV — v5 Completion vs v6 Decision

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Inputs:** residual runtime inventory · active authority map · legacy dependency register · dual-authority findings · day-one layer assessment · programme closure record  
**Runtime change:** NONE — decision-support only  

---

## 1. Decision question

> Can the active v5 runtime estate be brought fully onto the accepted Day-One architecture through a bounded completion programme, or do the remaining dependencies justify freezing v5 and moving to v6?

Accepted target:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured Layer B DTOs
→ frontend render / translation only
```

---

## 2. Principal recommendation

```text
GO — RETAIN V5 AND COMPLETE BOUNDED CONVERGENCE
```

**Confidence:** HIGH that kill-criteria for freeze are not met; MEDIUM-HIGH that remaining work is bounded under wave-gated medical review.

This is **not** a claim that estate-wide Day-One convergence is already complete.

---

## 3. Why not NO-GO / v6 now

### Kill-criteria check (planning paper §11)

| Criterion | Met? | Evidence |
|---|---|---|
| 11.1 Cohort-isolation failure | **No** | Pilot cohort isolated; PKG1–3 + CORRECT-1 completed without whole-estate rewrite |
| 11.2 Canonical-lineage failure | **No** | Pass 3 lineage recoverable for material INCLUDE cohorts; PKG2 attached Wave 1 kb47 lineage |
| 11.3 Authority-retirement failure (pilot) | **No** | Pilot COMPILED_ACTIVE exclusivity proven; REJECTED frame inert |
| 11.4 Unfixable cross-layer duplication | **No** | Residual duals are localised (elevation-context; layered why templates), not uncentralisable |
| 11.5 Scope-growth ceiling (>1 mandatory correction) | **No** | CORRECT-1 was the single authorised correction package |
| 11.6 Time/cost ceiling breach forcing freeze | **Not evidenced** | No formal ceiling-breach record found that mandates freeze |
| 11.7 Medical-review viability failure | **No for pilot** | Gate 2.5 closed; estate completion needs continued capacity but route exists |
| 11.8 Independent-assurance failure | **No** | CORRECT-1 closed under human authority with live UAT |

### What v6 would actually buy

| Factor | Bounded v5 completion | v6 clean implementation |
|---|---|---|
| Active legacy dependency complexity | LARGE but enumerable (36 WHY targets, verified exact count + local duals; frame count per target unresolved until Phase 1 identity closure) | Would still confront same medical content volume |
| Architectural coupling | Single orchestrator path already exists | Must re-integrate FE, auth, billing, persistence, cards |
| Medical re-review | Required for each WHY wave | **Also required** — content does not vanish |
| Data / schema migration | MEDIUM (versioning/stale/regenerate) | LARGE (dual-run or cutover) |
| Regression-estate reuse | HIGH | MEDIUM (porting cost) |
| Frontend reuse | HIGH (Layer C already corrected) | HIGH if strangler; LOW if rewrite |
| Provenance / replay continuity | MEDIUM gap, fixable in-place | Continuity break risk LARGE |
| Deletion risk | Managed retirement behind register | Higher if assets imported without Day-One proof |
| Compatibility preservation cost | REAL but declining as waves complete | High during strangler dual-run |
| Hidden residual authority likelihood | Declining with register + gates | Risk of reproducing transitional duals if rushed |
| Relative size | **LARGE** | **VERY LARGE** |
| Risk of restarting unfinished work | Low if packages stay outcome-based | **High** |

**Verdict:** v6 would not remove the medical-review or compile burden; it would add platform migration cost while the target authority model is already proven on v5.

---

## 4. Why GO is still conditional on boundedness

GO is justified only if completion remains:

- outcome-based (not open-ended re-architecture);
- wave-gated with medical STOP gates;
- exclusive-authority enforced per activation_key before legacy retirement;
- forbidden from silent dual emit.

If a future package discovers that legacy WHY cannot be retired without retaining competing authority for the same frame after compiled introduction, that specific wave triggers STOP / local V6 reconsideration under §11.3 — it does not retrospectively invalidate this estate decision.

---

## 5. Minimum safe completion programme (no implementation prompts)

Anti-micro-sprint rule applied: governance and policy absorbed into implementation packages; separate packages only where runtime safety domains diverge.

**Minimum safe package count: 3**

### Package A — Estate WHY Authority Completion

| Field | Content |
|---|---|
| product outcome | Every production-reachable WHY target uses compiled per-activation_key authority (or an explicit fail-closed skip), with legacy YAML non-selected |
| scope | Remaining `ROOT_CAUSE_TARGET_SPECS` outside the migrated pilot; absorb register/gate updates; refresh stale compiled estate index |
| active legacy pathways retired | L-01 emit path (wave by wave); pilot compatibility loaders as waves finish |
| new authority made canonical | Compiled WHY artefacts + authority register rows |
| medical review required | **Yes** — internal STOP gate per wave |
| risk level | HIGH (content) / MEDIUM (engineering machinery reuse) |
| change type | RUNTIME + CONTENT |
| internal phases | (1) inventory & wave plan (2) compile+lineage (3) Gate C medical review (4) activate exclusivity (5) legacy non-select proof |
| STOP gates | Medical capacity; lineage inventability; dual-emit detection; >25% scope growth |
| success criteria | For each completed wave: compiled exclusivity tests green; legacy not selected; consumer/clinician parity review signed |
| deletion / retirement criteria | Legacy YAML may remain on disk only as history after non-select proven; deregister loaders when safe |

### Package B — Residual Dual-Authority and Fallback Hardening

| Field | Content |
|---|---|
| product outcome | No unresolved dual answering the same medical question on live paths; missing WHY fails closed under ratified policy |
| scope | Homocysteine elevation-context disposition; layered why-it-matters selector; fallback quarantine; explicit family-aggregation policy where `signal_id` grain remains; co-service generalisation only where medically required |
| active legacy pathways retired | L-02 dual; L-04 unconstrained fallback; DUAL-05 selector gap |
| new authority made canonical | Single selector rules + explicit aggregation policy artefacts |
| medical review required | **Yes** for elevation-context and any new co-service families |
| risk level | MEDIUM–HIGH |
| change type | RUNTIME + GOVERNANCE |
| internal phases | (1) dual closure design (2) implement selectors (3) medical STOP (4) exclusivity gates |
| STOP gates | Cannot eliminate dual without new medical invention; FE boundary regression |
| success criteria | Dual-authority findings DUAL-01/05 closed or explicitly accepted as non-overlapping with tests; fallback policy enforced |
| deletion / retirement criteria | Remove or seal unused legacy hypothesis branches once non-select proven |

### Package C — Replay, Provenance, and Post-Authority Versioning

| Field | Content |
|---|---|
| product outcome | After medical-authority changes, results are stale/regenerable under explicit policy; provenance keys are real activation identities; historic waist debt is dispositioned |
| scope | Result-versioning advancement; waist historic remediation policy execution; output-authority provenance key fix; absorb related governance notes |
| active legacy pathways retired | L-11 uncontrolled historic use; L-12 bare provenance key debt |
| new authority made canonical | Versioning/stale policy as runtime contract |
| medical review required | No (integrity/policy), unless remap changes clinical inputs |
| risk level | MEDIUM |
| change type | RUNTIME + DATA POLICY |
| internal phases | (1) policy ratification (2) emitter/test fixes (3) historic disposition (4) regenerate UX proof |
| STOP gates | Silent historic rewrite without audit trail |
| success criteria | Provenance tests use real keys; waist historic rows classified disposition executed; regenerate-after-authority-change behaviour proven |
| deletion / retirement criteria | N/A beyond retiring bad fixture keys |

**Not authorised as standalone micro-sprints:** estate-index refresh, gate wiring, docs-only dual registers — absorb into A/B/C.

---

## 6. Relative sizing summary

| Option | Relative size | Major risks | Medical-review burden |
|---|---|---|---|
| Bounded v5 completion (3 packages) | **LARGE** | Wave backlog; dual regression; historic data | High but wave-bounded |
| Freeze v5 → v6 | **VERY LARGE** | Continuity break; dual-run; reintroducing transitional architecture | High (same content) plus migration overhead |

---

## 7. Evidence gaps (do not block this decision)

These are tracked, not STOP blockers for the principal recommendation:

1. Production traffic share per signal family not measured (static loader reachability is proven).
2. Live production LLM allow-flag state should be ops-confirmed at deployment time.
3. Full per-package medical maturity outside WHY registry remains a beta-readiness concern, not a freeze trigger by itself.

If GPT/Anthony require environment-level LLM flag proof before ratification, that is a **small ops confirmation**, not a new architecture package.

---

## 8. Next authorised action

1. GPT architectural review of this decision pack.  
2. Anthony ratification of `GO — RETAIN V5 AND COMPLETE BOUNDED CONVERGENCE` **or** explicit override.  
3. Only after ratification: author Automation Bus implementation prompts for Package A (then B, then C).  

**No implementation, deletion, migration, registry edit, or Knowledge Bus regeneration is authorised by this document.**
