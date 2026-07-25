# HealthIQ AI — Open Architecture Obligations

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1 |
| **Companion** | `HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION.md` |
| **Rule** | Contains **only unresolved** obligations. Closed work appears only as dependency references. |
| **Date** | 2026-07-25 |
| **Baseline SHA** | `363a644624e54dfdc0ac7012f8133fd5d278b593` |

Status values used below: `OPEN` | `PARTIALLY_CLOSED` | `DEFERRED_WITH_AUTHORITY` | `UNVERIFIABLE`.

---

## OBL-ARCH-001 — End-to-end activation-frame preservation on launch path

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-001 |
| **original requirement** | Multi-frame research fidelity must survive from registry through interaction maps, root-cause, report assembly, and related consumers — not only at `SignalRegistry` load (`ADR-RT-002`; day-one sprint plan; Transition Plan v3). |
| **source documents** | ADR-RT-002; day-one sprint plan; ARCH-RT-IDENTITY-PROV-1 reports; CURSOR/CLAUDE executable audits 2026-07-25; current-state baseline §7/§10 |
| **planned remediation** | ARCH-RT-2 registry fix → ARCH-RT-IDENTITY-PROV-1 consumer migration → remaining deferred surfaces |
| **delivery evidence** | Registry keyed by `activation_key` (closed); IDENTITY-PROV claimed 5 surfaces fixed and listed further deferred collapses |
| **current repository evidence** | Live multi-frame load (197 keys / 51 families). Remaining family/`signal_id` first-match behaviour still present on some analytics consumers (e.g. interaction confidence keyed by `signal_id`). Baseline lists multi-frame consumer completeness incomplete. |
| **status** | PARTIALLY_CLOSED |
| **risk if left open** | Distinct medical frames silently merge in user-visible intelligence; incorrect WHY/interaction attribution |
| **launch relevance** | Launch-critical for any multi-frame claim; active beta blocker in Jul 2026 audits |
| **dependency** | None for remaining consumer work; depends on registry identity (already delivered) |
| **recommended disposition** | Close remaining launch-path collapse surfaces in one outcome package (see Closure Sequence PKG-1) |

---

## OBL-ARCH-002 — Explicit package provenance / `source_spec_id` for launch claims

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-002 |
| **original requirement** | Activated outputs must carry honest, explicit research lineage; inferred directory/`source_document` derivation must not be presented as explicit `source_spec_id` (`ADR-RT-004`; ARCH-RT-5D; strategy Block 5). |
| **source documents** | ADR-RT-004; ARCH-RT-5D unresolved register; ARCH-RT-IDENTITY-PROV-1 inventory; Jul 2026 executable audits; current-state baseline §10/§13 |
| **planned remediation** | Compile-manifest schema + estate regen/backfill; IDENTITY-PROV status enum + launch-critical gate; batch-JSON extraction before beta eligibility |
| **delivery evidence** | Honest provenance enum and blocked launch-critical rows delivered; **no** estate-wide explicit `source_spec_id` invented |
| **current repository evidence** | **0 / 191** package manifests contain a `source_spec_id` field. Launch-critical kb47 inventory: 16 BLOCKED + 1 COMPILED_MANIFEST. RT5D batch-blocked class includes 147 packages (72 `pkg_kb52c_*`). |
| **status** | OPEN |
| **risk if left open** | Launch/beta claims of research traceability are overstated; unsafe to treat activation keys as explicit-spec identity |
| **launch relevance** | Launch-critical for provenance honesty; beta blocker #2 in Jul audits |
| **dependency** | Investigation-spec extraction / attach for batch-JSON packs; depends on OBL-ARCH-001 for safe multi-frame use of those specs |
| **recommended disposition** | Complete explicit lineage for launch-critical cohort first; keep non-critical cohorts blocked-for-claim (PKG-2) |

---

## OBL-ARCH-003 — Dual WHY / root-cause authority retirement for launch cohort

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-003 |
| **original requirement** | Compiled hypothesis artefacts become WHY authority; hand-authored root-cause YAML is temporary and must be retired where it overlaps investigation-spec hypotheses (`ADR-RT-003`; Transition Plan v3; day-one sprint ARCH-RT-4/5C). |
| **source documents** | ADR-RT-003; ARCH-RT-4/5C reports; ARCH-COMPLETION-2; Jul 2026 audits; current-state baseline §4/§13 |
| **planned remediation** | Shadow pilot → promote → estate migration; immediate YAML deletion rejected for day-one |
| **delivery evidence** | `signal_vitamin_d_low` compiled + runtime-promoted; untraceable WHY quarantined on clinician path |
| **current repository evidence** | **1** compiled hypothesis; **40** legacy YAML; **41** registry targets; compiler dual-path still live |
| **status** | OPEN (pilot closed; estate open). Temporary dual estate remains `DEFERRED_WITH_AUTHORITY` as programme posture, but **launch-cohort retirement is still OPEN**. |
| **risk if left open** | Parallel medical truth; drift between YAML and research; overstated “compiled WHY” completion |
| **launch relevance** | Launch-critical for any claim that WHY is compiled-governed estate-wide; beta blocker #3 |
| **dependency** | OBL-ARCH-001 (frame-aware WHY); medical review for new compiled hypotheses where content changes |
| **recommended disposition** | Complete launch-critical WHY authority (compile/promote **or** honestly classify remaining YAML as legacy-active non-claim) in PKG-3 — without pretending whole-estate done |

---

## OBL-ARCH-004 — Batch-JSON / blocked-cohort activation vs provenance honesty

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-004 |
| **original requirement** | Packages sourced from batch JSON without extractable frame IDs must be extracted or classified blocked; must not underpin ungoverned launch claims (`ADR-RT-004`; ARCH-RT-5D). |
| **source documents** | ADR-RT-004; ARCH-RT-5D; package generation inventory (stale counts); IDENTITY-PROV inventory |
| **planned remediation** | `blocked_pending_spec_extraction` class; extraction sprints |
| **delivery evidence** | Classification exists; extraction largely not done |
| **current repository evidence** | 72 `pkg_kb52c_*` and broader batch-blocked class still present; `SignalRegistry` still loads non-example libraries; policy `runtime_loaded: false` flags are **not** equivalent to load prevention |
| **status** | OPEN |
| **risk if left open** | Runtime may evaluate signals whose lineage is blocked for beta claims — authority mismatch |
| **launch relevance** | Launch-critical for honesty of “what is active”; may be acceptable if product claims exclude those packs |
| **dependency** | OBL-ARCH-002 |
| **recommended disposition** | Either extract+attach specs for packs that must remain claimable, or enforce non-claim / non-reachability consistently with provenance gate (fold into PKG-2) |

---

## OBL-ARCH-005 — Context-dependent activation prerequisites (androgen / FT3 conditions)

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-005 |
| **original requirement** | Context-dependent packages remain fail-closed until clinical sign-off and orchestrator context bridge prerequisites are met (Day-One Closure Review C-1…C-3). |
| **source documents** | DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md; BATCH2-CONTEXT registers; BETA-READINESS-RECHECK |
| **planned remediation** | Clinical sign-off artefact; ARCH-ORCH-RESTRUCTURE-1; FT3 metadata resolution before activation |
| **delivery evidence** | Fail-closed gates live; DHEA-S gated activation delivered separately; androgen sign-off still called out historically |
| **current repository evidence** | Context semantics / clearance registers remain governance authorities; Jul baseline treats some gates as maintained constraints |
| **status** | PARTIALLY_CLOSED (safety hold active; activation prerequisites incomplete) |
| **risk if left open** | Premature activation of ambiguous endocrine signals |
| **launch relevance** | Not a Wave 1 blocker while packages stay inactive; blocker for any activation sprint |
| **dependency** | Medical review / clinical sign-off artefacts |
| **recommended disposition** | Keep STOP gates; do not absorb into architecture identity/provenance packages |

---

## OBL-ARCH-006 — Estate-wide activation compile (governed spec→library path)

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-006 |
| **original requirement** | Governed activation compile from `investigation_spec` to `signal_library` / package artefacts, distinct from PSI (ADR-RT-001; ADR-RT-004; sprint ARCH-RT-1/5). |
| **source documents** | ADR-RT-001; ADR-RT-004; activation_compile_gap_report; day-one plan FINAL_updated |
| **planned remediation** | ARCH-RT-1 foundation + ARCH-RT-5 full regen |
| **delivery evidence** | DRAFT contracts + pilots; full regen reclassified / deferred for Wave 1 via classification |
| **current repository evidence** | No estate-wide activation compiler replacing generations; packages remain hand/legacy compiled inputs |
| **status** | DEFERRED_WITH_AUTHORITY |
| **risk if left open** | Long-term drift; regeneration remains ad hoc |
| **launch relevance** | Non-blocking for Wave 1 acceptance-as-classified; blocking for original whole-estate target |
| **dependency** | OBL-ARCH-002 |
| **recommended disposition** | Separate post-launch-critical architecture package; not required to close PKG-1…3 |

---

## OBL-ARCH-007 — PSI runtime consumption (optional richness)

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-007 |
| **original requirement** | PSI must be wired where launch-critical **or** explicitly classified non-launch-critical (Transition Plan v3; ARCH-RT-5E). |
| **source documents** | ARCH-RT-5E decision report/audit; ADR-RT-003; Jul 2026 baseline §8 |
| **planned remediation** | ARCH-RT-5E decision sprint |
| **delivery evidence** | Explicit `deferred_non_launch_blocker`; day-one validator forbids launch imports |
| **current repository evidence** | Loader present; 57 PSI files; zero launch-path importers |
| **status** | DEFERRED_WITH_AUTHORITY |
| **risk if left open** | Pass 3 richness remains stranded (product depth), not a silent dual-authority runtime hazard while unwired |
| **launch relevance** | Non-blocking while deferred classification holds |
| **dependency** | OBL-ARCH-002 (safe join on identity/provenance) before any future wiring |
| **recommended disposition** | Leave deferred until a new launch-critical claim requires it; do not treat as open safety defect |

---

## OBL-ARCH-008 — Whole-estate compiled card evidence beyond Wave 1

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-008 |
| **original requirement** | Card evidence compiled estate-wide; hard-coded lists not active authority (ADR-RT-001; ARCH-RT-5B). |
| **source documents** | ARCH-RT-5B; Closure Review; ARCH-COMPLETION-2/3; current-state baseline |
| **planned remediation** | Vertical slice → Wave 1 estate → further domains |
| **delivery evidence** | Wave 1: 10 estate-indexed compiled cards; hard-coded inactive |
| **current repository evidence** | Wave 1 closed; non-Wave-1 card compile not claimed |
| **status** | DEFERRED_WITH_AUTHORITY |
| **risk if left open** | New domains would reintroduce manual evidence risk if built outside compile path |
| **launch relevance** | Non-blocking for Wave 1; blocking for whole-estate target |
| **dependency** | Compile contracts already delivered |
| **recommended disposition** | Domain expansion packages only when those domains are in scope |

---

## OBL-ARCH-009 — Controlled beta not authorised (programme gate)

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-009 |
| **original requirement** | Controlled beta requires infrastructure **and** medical-content readiness against eight-block strategy gates (beta strategy 2026-06-20; Jul baseline). |
| **source documents** | Beta strategy; BUILD register; BETA-READINESS-* audits; WAVE1-LAUNCH-READINESS; Jul baseline §5/§10/§12 |
| **planned remediation** | Eight-block build programme |
| **delivery evidence** | Substantial infrastructure delivery; multiple readiness papers; **no** final beta authorisation |
| **current repository evidence** | Current-state baseline: controlled beta **not authorised**; Jul executable audits: beta unwarranted |
| **status** | OPEN |
| **risk if left open** | Premature public/invite exposure |
| **launch relevance** | Programme gate (binds all remaining obligations) |
| **dependency** | OBL-ARCH-001, 002, 003 at minimum for architecture honesty; medical-content obligations below |
| **recommended disposition** | Keep explicit non-authorisation until Stage 0 re-plans against baseline |

---

## OBL-ARCH-010 — Medical-content readiness (prose / WHY depth) — architecture-adjacent

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-010 |
| **original requirement** | Layer B explanatory substrate and medically approved prose depth sufficient for beta “wow” / trust (strategy Block 3; PROSE-INVENTORY-1; DYNAMIC-PROSE-ARCH-1). |
| **source documents** | Beta strategy; PROSE-INVENTORY-1; DYNAMIC-PROSE-ARCH-1; P3-LAYERB-INTEL-1 report; Jul baseline §7/§9 |
| **planned remediation** | P2/P3 prose depth; frame routing / modifiers; Round 2 medical review pipeline (historical wording) |
| **delivery evidence** | Partial retail/pathway substrate; P3-LAYERB-INTEL infrastructure; MR-BATCH-001B retained as test-only |
| **current repository evidence** | Modifier catalogue historically inert; compiled WHY only vitamin_d; candidate prose not promotable; Round 2 not obtained |
| **status** | OPEN |
| **risk if left open** | Thin explanations; trust failure even if infra gates are green |
| **launch relevance** | **Medical-content** beta blocker (distinct from infrastructure) |
| **dependency** | Medical review authority; must not use MR-BATCH-001B as promotion route |
| **recommended disposition** | Separate medical-content programme after architecture PKG-1…3; **do not** author prose-generation package in this reconciliation |

---

## OBL-ARCH-011 — Subsystem visibility-tier enforcement (soft policy)

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-011 |
| **original requirement** | Only medically supported subsystems scored/visible; enforce `visibility_tier` (MED-REV-1; PROGRAMME-STATUS-1). |
| **source documents** | PROGRAMME-STATUS-1; MED-REV-1 report; PROSE-INVENTORY-1; Jul baseline notes on soft visibility |
| **planned remediation** | MED-REV-1 enforcement sprint |
| **delivery evidence** | Field exists on YAML/DTO; enforcement historically incomplete |
| **current repository evidence** | Jul baseline still describes visibility policy as soft; not re-proven fully enforced in Jul executable audits |
| **status** | PARTIALLY_CLOSED |
| **risk if left open** | High-trust UI may show thin/unsupported subsystems |
| **launch relevance** | Product trust / medical honesty |
| **dependency** | Medical review of tier assignments |
| **recommended disposition** | Small enforcement package after medical sign-off of tiers; not absorbed into PKG-1 identity work |

---

## OBL-ARCH-012 — Secrets / history hygiene re-verification

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-012 |
| **original requirement** | No unresolved high-severity secrets/config blockers before controlled beta (strategy Gate 10; BETA-READINESS-RECHECK BB-1/BB-2). |
| **source documents** | WAVE1-LAUNCH-READINESS; BETA-READINESS-RECHECK-1; BETA-READINESS-SPRINT-2; Jul Cursor audit UNKNOWN note |
| **planned remediation** | Rotate keys; untrack; purge history; re-check |
| **delivery evidence** | Conflicting historical claims; SPRINT-2 validator reported clean at the time |
| **current repository evidence** | Jul 2026 executable audits did **not** re-prove secrets/history hygiene |
| **status** | UNVERIFIABLE |
| **risk if left open** | Credential exposure / operational blocker |
| **launch relevance** | Operational beta blocker until re-verified |
| **dependency** | Ops/security verification (outside Intelligence Core architecture packages) |
| **recommended disposition** | Independent secrets audit before any beta invite; not an ARCH-RT code package |

---

## OBL-ARCH-013 — Stale architecture inventory documents

| Field | Content |
|---|---|
| **obligation_id** | OBL-ARCH-013 |
| **original requirement** | Inventories used for governance must match live estate (implicit in ADR-RT-0 inventories; ARCH-GOV-BASELINE supersession of stale RT-5D expectations). |
| **source documents** | package_generation_inventory.md; signal_id_collision_inventory.md; intelligence_authority_inventory.md; active_intelligence_authority_manifest.md; ARCH-RT-5D register; Jul baseline §11 |
| **planned remediation** | Refresh inventories when estate changes |
| **delivery evidence** | Baseline refreshed some test expectations; many inventory docs still stale on disk |
| **current repository evidence** | Docs still claim 186 pkgs / 7 cards / 67 kb52c / lex overwrite; live is 191 / 10 / 72 / activation_key |
| **status** | OPEN |
| **risk if left open** | Agents and humans plan from false numbers; CI-trust hazard |
| **launch relevance** | Governance integrity (not direct clinical path) |
| **dependency** | None |
| **recommended disposition** | Docs hygiene refresh attached to next architecture package or dedicated hygiene sprint |

---

## Explicitly excluded (closed — dependency references only)

These are **not** open obligations; listed only so they are not re-opened from memory:

- Wave 1 compiled card evidence active / hard-coded inactive (depends: D1 closed).
- Registry `activation_key` identity + duplicate fail-closed (depends: B1/B3 closed).
- No raw research reads on default analysis path (depends: A2 closed).
- Gemini deny-default / non-analytical authority (depends: F2 closed).
- Frontend sampled live routes render-only (depends: F1 closed).
- PSI intentionally unwired with day-one import guard (depends: G1 deferred-with-authority, not an open safety defect).
- Six Wave 1 domains wired (supersedes “3 missing”).
- CB-1…CB-4 public-launch fixes (closed).
- Architecture validation gate PASS as of Jul 2026 independent audits (closed as gate, not as beta).
