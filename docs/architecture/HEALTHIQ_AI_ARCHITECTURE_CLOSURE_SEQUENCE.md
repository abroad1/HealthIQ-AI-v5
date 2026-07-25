# HealthIQ AI — Architecture Closure Sequence

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1 |
| **Companion** | `HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION.md`; `HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS.md` |
| **Date** | 2026-07-25 |
| **Rule** | Minimum safe **outcome-based** packages to complete the original target architecture posture for launch-critical claims. No implementation prompts. |

---

## 1. Anti-micro-sprint gate

Do **not** split further into:

- separate sprints per collapse surface file;
- separate sprints per package generation prefix;
- separate sprints for docs-only inventory refresh vs the package that changes the estate;
- a “PSI wiring” sprint without a new launch-critical claim;
- a prose/content-promotion sprint under the banner of architecture closure.

Do **not** combine:

| Must stay separate | Why |
|---|---|
| Frame-identity consumer completion | Runtime behaviour change on analytics compilers |
| Provenance / investigation-spec lineage | Knowledge-asset / governance change; medical extraction dependency |
| WHY authority completion | Medical-intelligence compile + compiler behaviour; medical review dependency |
| Medical prose depth | Content programme; explicitly out of this architecture closure sequence |
| Secrets hygiene re-proof | Operational/security; not Intelligence Core architecture |

**Whole-estate** activation compile (OBL-ARCH-006) and **whole-estate** card expansion (OBL-ARCH-008) remain deferred-with-authority and are **not** required to close the original *launch-critical* architecture honesty target once PKG-1…3 land.

---

## 2. Target outcome of this sequence

After PKG-1…3, the repository should be able to truthfully claim:

1. Launch-path consumers preserve activation frames (or fail closed) — not only the registry.
2. Launch-critical packages either have **explicit** research lineage or are **explicitly non-claimable / non-reachable** for beta.
3. Launch-critical WHY is either compiled-governed or honestly classified as legacy-active without “compiled estate complete” language.
4. Controlled beta remains a separate programme gate (OBL-ARCH-009) that still requires medical-content work (OBL-ARCH-010) — **not** declared here.

This sequence does **not** declare architecture complete or beta ready.

---

## 3. Package sequence (minimum: 3)

```text
PKG-1  Launch-path activation-frame identity completion
  → PKG-2  Launch-critical provenance and blocked-cohort honesty
    → PKG-3  Launch-critical WHY / root-cause authority completion
```

Optional follow-ons (not in the minimum set): inventory hygiene (OBL-ARCH-013), visibility-tier enforcement (OBL-ARCH-011), secrets re-audit (OBL-ARCH-012), medical prose programme (OBL-ARCH-010), deferred PSI wiring (OBL-ARCH-007), estate-wide activation compile (OBL-ARCH-006).

---

### PKG-1 — Launch-path activation-frame identity completion

| Field | Content |
|---|---|
| **product outcome** | Every launch-path consumer that ranks, joins, or explains signals uses `activation_key` (or an explicit governed frame-selection policy) so distinct medical frames cannot silently collapse. |
| **obligations closed** | OBL-ARCH-001 (to CLOSED). Partially advances OBL-ARCH-009 readiness (architecture honesty). |
| **why it cannot safely be absorbed into another package** | Pure runtime behaviour change across analytics compilers; mixing with knowledge-asset extraction (PKG-2) or hypothesis compile (PKG-3) recreates the governance failure the day-one plan forbade (behaviour + content + schema in one package). |
| **medical-review dependency** | None for identity preservation mechanics. Medical review only if a new frame-selection *policy* chooses among competing frames rather than preserving all. |
| **runtime boundary** | `backend/core/` analytics/report/root-cause/interaction consumers and related tests. No medical YAML invention. No frontend medical selection. |
| **STOP gates** | STOP if scope expands to PSI wiring, prose promotion, or estate regeneration. STOP if a consumer requires inventing medical priority among frames without an approved policy ADR. |
| **acceptance condition** | No remaining documented launch-path `signal_id`-only collapse on the analysis→DTO path for multi-frame families; architecture/identity gates PASS; Jul-audit-class collapse findings addressed or explicitly fail-closed. |

---

### PKG-2 — Launch-critical provenance and blocked-cohort honesty

| Field | Content |
|---|---|
| **product outcome** | Launch-critical packages either carry explicit `source_spec_id` / investigation-spec lineage, or are consistently non-claimable (and, where required, non-reachable) so beta cannot assert false traceability. |
| **obligations closed** | OBL-ARCH-002; OBL-ARCH-004 (for launch-critical cohort). Inventory refresh for touched cohorts may close OBL-ARCH-013 for those rows. |
| **why it cannot safely be absorbed into another package** | Requires research-asset extraction/attach and provenance governance; different risk class from compiler identity (PKG-1) and from WHY compile content (PKG-3). Combining would force mixed CONTENT/BEHAVIOUR HIGH work without separable STOP gates. |
| **medical-review dependency** | Yes, if extraction creates or selects medical frames from batch JSON. Attach-only of already-approved `inv_` specs may be CONTENT with lower medical novelty — still STOP if meaning changes. |
| **runtime boundary** | Knowledge Bus packages/research/governance + provenance scanners/gates. Runtime load policy changes only if required to align reachability with blocked claims. |
| **STOP gates** | STOP if asked to invent `source_spec_id` values without source artefacts. STOP if estate-wide regen of all 191 packages is forced into this package. STOP if PSI wiring is smuggled in. |
| **acceptance condition** | Launch-critical inventory shows explicit lineage **or** enforced non-eligibility; zero launch-critical rows that are both beta-claimed and `BLOCKED`/inferred-only; scanners and gate docs agree with live counts. |

---

### PKG-3 — Launch-critical WHY / root-cause authority completion

| Field | Content |
|---|---|
| **product outcome** | For the launch-critical signal cohort, WHY authority is either compiled-promoted (preferred target architecture) **or** explicitly classified legacy-active with no overstated completion claim — ending the unsafe middle state of “compiled architecture done” while 40 YAML targets remain silent dual authority. |
| **obligations closed** | OBL-ARCH-003 for launch-critical cohort. Does **not** automatically close whole-estate YAML retirement. |
| **why it cannot safely be absorbed into another package** | Touches medical hypothesis artefacts and root-cause compiler behaviour; medical-review gated; must not be mixed with provenance extraction or unrelated consumer refactors. |
| **medical-review dependency** | **Yes** for any new or changed compiled hypothesis content. Classification-only (label legacy-active without content change) may proceed without new medical prose, but cannot claim medical upgrade. |
| **runtime boundary** | Compiled hypothesis artefacts + root-cause compiler/registry paths + tests. No Gemini. No frontend inference. |
| **STOP gates** | STOP if package attempts whole-estate 41-target compile in one pass without cohort boundary. STOP if YAML deletion is proposed without promotion/parity evidence. STOP if clinician quarantine regressions appear. |
| **acceptance condition** | Launch-critical targets have a single declared authority class each; dual-path remains only where explicitly classified; baseline/docs no longer imply compiled WHY completion beyond evidence. |

---

## 4. What remains after PKG-1…3 (explicitly out of minimum sequence)

| Obligation | Why deferred from minimum sequence |
|---|---|
| OBL-ARCH-006 estate-wide activation compile | Original whole-estate target; not required for launch-critical honesty once PKG-2 holds |
| OBL-ARCH-007 PSI wiring | Already deferred-with-authority; no new launch-critical claim |
| OBL-ARCH-008 cards beyond Wave 1 | Wave 1 card authority already closed |
| OBL-ARCH-010 medical prose depth | Medical-content programme; no prose package authored here |
| OBL-ARCH-011 visibility-tier enforcement | Product trust; needs medical tier sign-off; separate small package |
| OBL-ARCH-012 secrets hygiene | Operational re-verification |
| OBL-ARCH-005 context activation prerequisites | Remains STOP-gated until clinical sign-off; not architecture identity work |
| OBL-ARCH-009 controlled beta authorisation | Programme gate after architecture **and** medical-content |

---

## 5. Dependency graph

```text
                    ┌─────────────────────────┐
                    │ OBL-ARCH-012 secrets    │ (parallel, ops)
                    └─────────────────────────┘

PKG-1 identity ──► PKG-2 provenance ──► PKG-3 WHY cohort
     │                    │                  │
     └──────────► OBL-ARCH-009 beta gate ◄───┴── OBL-ARCH-010 prose (separate programme)
                        ▲
                        └── OBL-ARCH-011 visibility (optional small package)
```

---

## 6. Explicit non-deliverables of this sequence document

- No Cursor/Automation Bus implementation prompts.
- No prose-generation or content-promotion package.
- No PSI wiring package.
- No architecture-completion or beta-readiness declaration.
- No runtime or medical-content file changes in ARCH-PROG-RECON-1.
