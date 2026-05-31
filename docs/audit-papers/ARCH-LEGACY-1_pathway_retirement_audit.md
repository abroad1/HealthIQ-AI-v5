# ARCH-LEGACY-1 — Legacy Pathway Retirement Audit

**Work ID:** `ARCH-LEGACY-1_pathway_retirement_audit`  
**Branch:** `work/ARCH-LEGACY-1-pathway-retirement-audit`  
**Change type:** CONTENT (audit-only — no production code changes)  
**Audit status:** Complete (2026-05-31)

## Executive verdict

The Wave 1 launch architecture is **governed and launch-viable**. ARCH-RT-6 guardrails, MED-REV-1/2 visibility, KB-UTIL-1 card enrichment, and LAYER-B-1 narrative brief maturity have **contained** most dual-authority risk on user-facing surfaces.

**No launch blockers** were identified. Remaining legacy paths fall into three buckets:

1. **Dead but present** — safe to delete in a follow-on implementation sprint (`_Wave1SubsystemDef` partition, `cv_contributor`).
2. **Reachable and classified** — intentional dual authority with guards (hidden subsystems, root-cause YAML vs compiled promotion, CRP signal firing with hidden card tier).
3. **Migration required** — root-cause compiled promotion estate (40 YAML targets vs 1 promoted) and CRP Pass 3 / package lineage alignment.

**Recommended next sprint:** `ARCH-LEGACY-2_targeted_retirement_implementation` (delete dead paths, extend validator, execute prioritized migrations).

---

## Preflight baseline

| Check | Result |
|---|---|
| `main` @ `0dfe1ad` == `origin/main` | Yes |
| Stash | None |
| LAYER-B-1 merged | Yes |
| Carry-forward register | Present |
| Production code modified | **No** |

---

## Legacy pathway inventory and classification

| ID | Pathway | Location | Reachable? | Guarded? | Conflicts MED-REV/KB-UTIL/LAYER-B? | Classification | Future sprint |
|---|---|---|---|---|---|---|---|
| L1 | Hard-coded `_Wave1SubsystemDef` fallback partition | `wave1_subsystem_evidence.py` | **No** — all 7 subsystems route compiled-first; hidden → skip | Yes — estate index `wave1_subsystems_legacy_hard_coded: []`, ARCH-RT-3 tests | No | **retained_unreachable_guarded** | ARCH-LEGACY-2 — delete dead defs |
| L2 | `cv_contributor` (greedy IDL loop) | `domain_narrative_wave1.py` | **No** — zero call sites | Partial — not banned by validator | Superseded by D-6 / lipid-only paths | **retirement_candidate** | ARCH-LEGACY-2 (CF-MEDREV2-003) |
| L3 | `cv_contributor_primary` + homocysteine signal fallback | `domain_narrative_wave1.py`, `domain_score_assembler.py` | **Conditional** — when lipid-only authority not applied | Yes — MED-REV-2 / KB-UTIL-1 regression | Can reintroduce hcy copy if lipid authority bypassed | **retained_reachable_classified** | ARCH-LEGACY-2 — tighten invariant |
| L4 | `cv_contributor_for_lipid_visible_card` + lipid-only fallback | `domain_narrative_wave1.py` | **Yes** — default CV card path post MED-REV-2 | Yes — KB-UTIL-1 UAT regression | Aligned | **retained_reachable_classified** | None |
| L5 | `confidence_sentence_cv_coherent` homocysteine bridge | `domain_narrative_wave1.py` | **Conditional** — if contributor mentions homocysteine | Partial | Low risk under lipid-only contributor | **retirement_candidate** | ARCH-LEGACY-2 |
| L6 | Legacy YAML root-cause (40 signals) | `load_root_cause_hypotheses.py`, `root_cause_compiler_v1.py` | **Yes** — default for non-promoted targets | Yes — registry tests, divergence harness; 41 targets registered | Dual authority by design | **migration_required** | ARCH-RT-4+ promotion |
| L7 | Compiled promoted hypothesis (vitamin D) | `compiled_hypothesis.py`, `compiled_hypothesis_registry_v1.py` | **Yes** — `signal_vitamin_d_low` only | Yes — ARCH-RT-4 validator | Aligned | **retained_reachable_classified** | ARCH-RT-4+ expand promotion |
| L8 | CRP `pkg_s24_crp_high_inflammation` / `signal_crp_high` | `knowledge_bus/packages/…`, SignalRegistry | **Yes** — signal evaluation when CRP thresholds met | Partial — MED-REV-1 hides vascular subsystem DTO | Card hidden; signal/IDL may surface elsewhere; root cause uses `signal_systemic_inflammation` (naming split) | **migration_required** | CRP-PASS3-MIGRATION or ARCH-LEGACY-2 |
| L9 | Hidden subsystem suppression (`hidden_v1`) | `health_system_card_evidence.py` | **Yes** — suppression boundary | Yes — `validate_med_rev1_wave1_visibility`, regression | **Authoritative** MED-REV-1 | **retained_reachable_classified** | None unless policy changes |
| L10 | Rail completeness fallback (CV/MET) | `domain_score_assembler.py` `_evidence_completeness_for_rail` | **Conditional** — when subsystem rows empty | Partial — KB-UTIL-1 liver flat override tested | Edge mismatch if compiled rows missing | **retained_reachable_classified** | ARCH-LEGACY-2 optional assert |
| L11 | Flat liver completeness override | `domain_score_assembler.py` | **Yes** — liver card | Yes — KB-UTIL-1 regression | Aligned post KB-UTIL-1 fix | **retained_reachable_classified** | None |
| L12 | CV `active_signal_ids` homocysteine inclusion | `domain_score_assembler._is_wave1_cardiovascular` | **Yes** — homocysteine signals collected | Partial — narrative lipid authority mitigates copy | Does not affect visible subsystem score basis | **retained_reachable_classified** | ARCH-LEGACY-2 optional filter |
| L13 | Frontend render-only flat/subsystem evidence | `Wave1*EvidenceSection.tsx`, `Wave1DomainCards.tsx` | **Yes** | Yes — `validate_frontend_guards`, component tests | Aligned | **retained_reachable_classified** | None |
| L14 | Frontend snapshot staleness (pre-regen analyses) | Results page DTO immutability | **Yes** — old analysis IDs | Documented MED-REV-2 UAT | UX not logic drift | **deferred_non_launch_blocker** | REGEN-1 / LAUNCH-UX-2 |
| L15 | Inferred / batch-blocked provenance cohorts | ARCH-RT-5D register | Compile-time / inventory | Yes — manifest scans | Deferred per RT5D | **deferred_non_launch_blocker** | KB-UTIL-2 / compile hardening |
| L16 | `narrative_payload_v1` digest-only persistence | Orchestrator / DTO | **Yes** | LAYER-B-1 tests | By design deferral | **deferred_non_launch_blocker** | LLM-NAR-0 (CF-LAYERB1-001) |

**Every identified item is classified.** No **launch_blocker** or **retained_reachable_unguarded** items on Wave 1 visible surfaces.

---

## Reachability assessment (detail)

### 1. Wave 1 hard-coded subsystem fallback

All Wave 1 subsystem IDs are in `PILOT_COMPILED_SUBSYSTEM_IDS`. Assembly always calls `assemble_subsystem_from_compiled_card_evidence` first. Hidden tiers return `None` and the row is skipped — the hard-coded `_partition_subsystem_markers` branch is **unreachable** for current estate.

Stale labels in `_Wave1SubsystemDef` (e.g. "Lipid transport", "Glycaemic control") **cannot** reach the frontend via this path.

### 2. Cardiovascular narrative helpers

| Function | Call sites | User-facing risk |
|---|---|---|
| `cv_contributor` | None | None — dead code |
| `cv_contributor_primary` | `cv_block` when not lipid-visible | Low if lipid authority always applies on Wave 1 CV |
| `cv_contributor_for_lipid_visible_card` | Default CV path | Low — excludes hcy/inflammation copy |
| `confidence_sentence_cv_coherent` | CV card | Conditional hcy bridge |

### 3. Root-cause legacy YAML vs compiled

`root_cause_compiler_v1.compile_root_cause_v1` iterates registry targets. Promoted compiled signals short-circuit to `get_compiled_hypothesis_artefact`; all others load legacy YAML hypotheses. **41 registry targets; 1 runtime-promoted compiled** (`signal_vitamin_d_low`). Boundary is explicit and tested; expansion is a migration programme, not a launch defect.

### 4. CRP / s24 legacy path

- **Signal evaluation:** `signal_crp_high` can fire via legacy package.
- **Card DTO:** `wave1_cv_vascular_strain` is `hidden_v1` — no user-facing subsystem row.
- **CV domain signals:** `_is_wave1_cardiovascular` does **not** include `signal_crp` / CRP primary metric.
- **Root cause:** uses `signal_systemic_inflammation` registry entry — **naming split** from `signal_crp_high`.
- **Pass 3:** dedicated CRP investigation specs exist in Batch 4 but are not wired to runtime package pointers (per KB-UTIL-1 / PASS3 audits).

### 5. Completeness rails

- **CV/MET:** Subsystem union when visible rows present; rail fallback only when subsystem list empty.
- **Liver:** Flat domain evidence overrides rail counts (KB-UTIL-1 fix). Protected by regression tests.

### 6. Frontend

Components consume persisted DTO fields only. Validator blocks `knowledge_bus` reads and clinical role inference. Residual: `defensiveFallbackLabel` humanizes missing `display_label`; pre-regeneration immutable snapshots show stale copy (MED-REV-2 documented).

---

## Guardrail coverage assessment

`validate_day_one_architecture.py` **PASS** covers:

| Guardrail | Covered |
|---|---|
| 7-subsystem compiled card estate | Yes |
| Compile manifest hashes (KB-UTIL-1) | Yes |
| MED-REV-1 `hidden_v1` / scored tiers | Yes |
| KB-UTIL-1 enrichment + liver flat | Yes |
| Vitamin D compiled hypothesis promotion | Yes |
| PSI isolation / no runtime inv-spec reads | Yes |
| Frontend static guards (no KB reads) | Yes |
| Signal `activation_key` uniqueness | Yes |

**Gaps (recommend ARCH-LEGACY-2, do not implement in this audit):**

- Dead symbol detection (`cv_contributor` unreachable)
- CRP package / Pass 3 migration status assertion
- Root-cause promotion inventory vs YAML target count
- `signal_crp_high` ↔ `signal_systemic_inflammation` policy consistency
- Proof hard-coded subsystem partition unreachable beyond empty estate list

---

## Launch-risk assessment

| Risk | Level | Rationale |
|---|---|---|
| Hidden subsystems reappear as score basis | **Low** | MED-REV-1 + LAYER-B-1 boundaries + KB-UTIL-1 regression |
| Stale hard-coded labels on cards | **Low** | Compiled path exclusive at runtime |
| Homocysteine/CRP copy on CV card | **Low** (post KB-UTIL-1 fix) | Lipid-only narrative authority; monitor non-lipid-visible edge |
| Root-cause dual authority confusion | **Medium** (internal) | 40 YAML / 1 compiled — documented, not user-visible card conflict |
| CRP signal without governed card | **Low** | Hidden tier; signal not in CV `active_signal_ids` |
| Frontend clinical inference | **Low** | Render-only validated |
| Immutable stale snapshots | **Low** | Regeneration UX exists (MED-REV-2) |

**No launch blockers identified.**

---

## Recommended retirement / migration order

1. **ARCH-LEGACY-2 (immediate follow-on):** Delete dead code (`cv_contributor`, `_Wave1SubsystemDef` unreachable partition); extend validator gaps; optional homocysteine bridge removal per CF-MEDREV2-003.
2. **CRP-PASS3-MIGRATION (optional slice):** Align `signal_crp_high` with root-cause registry; re-ingest Pass 3 CRP specs; retire active `pkg_s24_crp_high_inflammation` pointer when governed.
3. **ARCH-RT-4+ (programme):** Expand compiled hypothesis promotion beyond vitamin D.
4. **KB-UTIL-2:** Hypothesis/contradiction/confirmatory surfacing design (CF-KBUTIL1-002) — after medical review.
5. **LLM-NAR-0:** Translation design + NarrativePayload persistence (CF-LAYERB1-001).
6. **REGEN-1 / LAUNCH-UX-2:** Lineage hardening and results hierarchy polish.

---

## Proposed future sprint list

| Sprint | Purpose |
|---|---|
| **ARCH-LEGACY-2** | Targeted retirement implementation (dead paths, validator extensions) |
| **CRP-PASS3-MIGRATION** | CRP package/spec alignment |
| **KB-UTIL-2** | Hypothesis/contradiction/confirmatory surface design |
| **LLM-NAR-0** | LLM translation design audit |
| **LAUNCH-UX-2** | Results hierarchy polish |
| **REGEN-1** | Result lineage hardening (CF-MEDREV2-001/002) |

---

## Carry-forward register updates

See `docs/sprints/launch_core_carry_forward_register.md`:

- **CF-MEDREV2-003** — notes enriched with ARCH-LEGACY-1 classification (`cv_contributor` = retirement_candidate).
- **CF-ARCHLEG1-001** — Root-cause dual authority migration (40 YAML / 1 compiled).
- **CF-ARCHLEG1-002** — CRP legacy s24 / signal naming split / Pass 3 migration.
- **CF-ARCHLEG1-003** — Remove unreachable `_Wave1SubsystemDef` partition code.
- **CF-ARCHLEG1-004** — Extend ARCH-RT-6 validator for legacy retirement gaps.

---

## Tests / validators run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

**Result:** PASS / PASS

---

## Confirmation

- **No production code, schemas, tests, packages, compiled artefacts, or frontend components were modified.**
- Only audit documentation and carry-forward register updates are in scope for this sprint.
