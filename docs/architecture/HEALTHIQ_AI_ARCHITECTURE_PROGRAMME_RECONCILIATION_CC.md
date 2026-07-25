# HealthIQ AI — Architecture Programme Reconciliation (Claude Code Independent Verification)

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1-CC |
| **Role** | Independent second auditor — not a review of Cursor's prose, a separate reconstruction |
| **Status** | RECONCILIATION COMPLETE — read-only; no architecture-completion or beta declaration |
| **Audit date** | 2026-07-25 |
| **Baseline SHA (session start)** | `363a644624e54dfdc0ac7012f8133fd5d278b593` (main) |
| **Branch** | `audit/arch-prog-recon-1-cc-independent-verification` |
| **Independence discipline** | All findings below were drafted (see `independent_first_pass.md` working note) before Cursor's three reconciliation documents were opened. Cursor's own `ARCH-PROG-RECON-1_implementation_and_verification_report.md` was read earlier as evidence-base material (explicitly listed as required reading in the work order), not as a conclusion to inherit. |

---

## 1. Executive verdict

The original target architecture (ADR-RT-001–004, day-one sprint plan) required: a single research→compile→runtime pipeline, no parallel medical authorities, `activation_key` frame identity preserved end-to-end (not only at registry load), compiled card and WHY artefacts, explicit (not inferred) provenance, and Layer B ownership of medical truth with Layer C/Gemini presentation-only.

**Independently reconstructed current state (verified against live code, not inherited audit wording):**

- Registry-level identity is genuinely fixed: `SignalRegistry` keys on `activation_key`, fails closed on duplicates (`signal_evaluator.py:61-65`).
- Five downstream consumers were migrated to `activation_key` by ARCH-RT-IDENTITY-PROV-1/C1. **One of those five (`signal_interaction_builder.py`) is only partially migrated** — it emits `participating_activation_keys` as metadata but its interaction-graph node identity and confidence lookup (`node_ids`, `confidence_by_signal`) still key on bare `signal_id` (lines 63-66, 145, 220-224). This is a finding this audit produced independently, not inherited.
- Four further consumers remain deliberately, honestly un-migrated: `interpretation_display_layer_publish_v1.py`, `domain_score_assembler.py`, `narrative_report_compiler_v1.py`, `intervention_selector_v1.py`.
- Provenance: 0/191 package manifests carry an explicit `source_spec_id` field on disk — confirmed by direct scan, unchanged by ARCH-RT-IDENTITY-PROV-1 (which added an honesty/classification layer, not lineage backfill). **Confirmed by direct code read**: `SignalRegistry._iter_signal_library_paths()` (`signal_evaluator.py:33-36`) loads every `*/signal_library.yaml` under `knowledge_bus/packages/` with no provenance filter, and `provenance_status` is carried into `SignalResult`/`ReportTopFindingV1` as disclosed metadata only — it is never used to suppress or exclude a firing signal. Packages classified `BLOCKED` for beta-claim purposes (16 launch-critical `pkg_kb47_*` rows) are fully reachable and rankable at runtime today.
- WHY authority: dual at the system level (1 compiled hypothesis, 40 legacy YAML, 41 registry targets) but **not overlapping per-signal** — `root_cause_compiler_v1.py:539` branches per-`signal_id` to either the compiled or legacy path, mutually exclusively. Row-level frame collapse is fixed (all fired frames emit a finding); hypothesis *content* for the 39 non-pilot legacy signals remains family-level, not frame-differentiated.
- Signal-library generations: not competing runtime authorities. No code path was found that loads `knowledge_bus/packages/` contents directly as a parallel runtime source outside the compiled `signal_library.yaml` glob; the vast majority of the 192 on-disk package directories are compile-time source material, most classified `legacy_retained`/`requires_review`/`BLOCKED`, not independently "active." `package_generation_inventory.md` (186 packages, `pkg_kb52c_*`=67) is stale — live count is 192 directories / 191 manifests, `pkg_kb52c_*`=72.

**Wave 1 acceptance (`accepted_for_wave1_launch`, ARCH-RT-6) is real and bounded. It is not whole-estate completion, and controlled beta remains explicitly not authorised** (`HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` §10). No completion or beta-readiness declaration is made by this package.

---

## 2. Evidence base

### 2.1 Primary evidence folders

| Folder | Files inventoried | Method |
|---|---:|---|
| `docs/audit-papers/` | 185 (includes Cursor's own `ARCH-PROG-RECON-1_implementation_and_verification_report.md`, added post-original-inventory) | Full filename/one-line-characterization inventory; ~35 files flagged relevant to the four threads (identity, provenance, WHY, signal-library) were deep-read; remainder triaged NOT RELEVANT by domain (frontend UAT, unit conversion, questionnaire UX, card-visual UX — none bear on the four threads) |
| `docs/planning-papers/` | 19 | Full inventory; not individually deep-read — their content is formally ratified/distilled into ADR-RT-001–004, which were read in full and are the operative record of their decisions |

### 2.2 Authoritative continuity/architecture documents read in full

`docs/AUTHORITY_MAP.md`; `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md`; `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`; `docs/architecture/ADR-RT-001` through `004`; `docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md`; `docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md`; `docs/architecture/P3-LAYERB-INTEL-1_migration_and_coverage_inventory.md`.

### 2.3 Merged package evidence read

- `docs/audit-papers/ARCH-RT-IDENTITY-PROV-1_implementation_and_verification_report.md` (baseline `6d30bbf`, impl commit `ebb1d43`)
- `docs/audit-papers/ARCH-RT-IDENTITY-PROV-1-C1_correction_verification_report.md` (independent re-verification, kernel finish `1ec4484`)
- Merge commit `0c90f95` "ARCH-RT-IDENTITY-PROV-1 + C1 evidence completion"
- `automation_bus/latest_audit_summary.md` covering P3-LAYERB-INTEL-1 (PASS, HIGH risk, independently re-verified — confirmed clean diff on `root_cause_compiler_v1.py` / `signal_activation_identity_v1.py`, i.e. that package did not touch WHY compilation)
- `docs/audit-papers/ARCH-PROG-RECON-1_implementation_and_verification_report.md` (read per work order §Evidence base — methodology and quantitative claims extracted for cross-check, not inherited)

### 2.4 Repository-state note (STOP condition 7)

At session start, four untracked files existed on the working branch: Cursor's three reconciliation outputs (`HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION.md`, `HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS.md`, `HEALTHIQ_AI_ARCHITECTURE_CLOSURE_SEQUENCE.md`) and `docs/audit-papers/ARCH-PROG-RECON-1_implementation_and_verification_report.md`. These are exactly the evidence this audit was instructed to read (§ Evidence base of the work order) — not extraneous work-in-progress. Treated as clean-enough to proceed; documented here rather than treated as a STOP trigger.

---

## 3. Programme chronology (independently reconstructed)

```text
Market/launch-core planning (early-mid May 2026)
→ Forensic/launch-grade audits (~2026-05-04)
→ Core scaffold programme (~2026-05-20)
→ Research utilisation / ARCH-R1 reviews (late May 2026)
→ As-Is→Day-One Transition Plan v1→v2→v3 + dual reviews (2026-05-28)
→ ADR-RT-001–004 ACCEPTED (2026-05-28)
→ Day-one delivery: WAVE1-EQUIV1 → ARCH-RT-0 → ARCH-RT-1 → ARCH-RT-2 → ARCH-RT-3 → ARCH-RT-4 → ARCH-RT-5/5B/5C/5D/5E → ARCH-RT-6 (accepted_for_wave1_launch)
→ Beta-readiness eight-block programme (2026-06-20 onward)
→ Identity/prose corrections: ARCH-RT-IDENTITY-PROV-1 + C1, P3-LAYERB-INTEL-1 (Jul 2026)
→ Governance baseline reset: ARCH-GOV-BASELINE-1, CURRENT_STATE_BASELINE_2026-07-25 (controlled beta NOT authorised)
```

This chronology was reconstructed from ADR dates, sprint-plan delivery-status notes, and git merge commits (`0c90f95`, `d877d0d`, `51b998d`), independently of Cursor's phase table — it agrees with Cursor's chronology in substance, which is expected: both are reading the same small set of dated ADRs and merge history, not each other.

---

## 4. Original target architecture

Reconstructed from ADR-RT-001 (canonical pipeline), ADR-RT-002 (identity/registry), ADR-RT-003 (hypothesis/root-cause transition), ADR-RT-004 (compile manifest/provenance), and the day-one sprint plan's Sprint 0–6 sequence + carry-forward register — **not** invented here.

| Pillar | Requirement | Source |
|---|---|---|
| Canonical research | `investigation_spec` v3 sole authority for new compile work; legacy packages/YAML temporary until governed regeneration | ADR-RT-001 |
| Compile pipeline | spec → governed compile (manifest-emitting) → immutable artefacts → thin loaders → DTOs → FE render-only | ADR-RT-001 |
| Identity | `MULTI_FRAME_PER_DIRECTION`; `activation_key = signal_id::spec_id` required at registry, `SignalResult`, and compile-manifest rows; fail closed on duplicate `activation_key` | ADR-RT-002 |
| WHY | Investigation-spec hypotheses never load directly at runtime; compiled hypothesis artefact is the target authority; hand YAML is temporary, "immediate deletion... rejected for day-one" | ADR-RT-003 |
| Provenance | `source_spec_id` mandatory for spec-provenance claims; `legacy_retained` boolean; batch-JSON packages `BLOCKED_PENDING_SPEC_EXTRACTION` at compile time | ADR-RT-004 |
| PSI | Optional signal-layer semantics only; not a hypothesis authority; runtime wiring scheduled separately, may remain unwired | ADR-RT-001/ADR-008 (via ADR-RT-003 Decision 1) |

**Two distinct "day-one" meanings must not be collapsed** (confirmed independently from the sprint plan's own framing): launch-core day-one (bounded personalised pipeline, May plan) vs. architecture day-one (research→compile→runtime authority correction, ARCH-RT programme). Wave 1 acceptance answers the first; the second remains partially open per §5 below.

---

## 5. Finding-to-remediation matrix (independent)

Status values: `CLOSED` | `PARTIALLY_CLOSED` | `DEFERRED_WITH_AUTHORITY` | `SUPERSEDED` | `OPEN` | `UNVERIFIABLE`.

| ID | Finding | Remediation delivered | Independent current-code verification | Status | Confidence |
|---|---|---|---|---|---|
| F1 | `SignalRegistry` collapsed multi-frame `signal_id` collisions via lexicographic overwrite | ARCH-RT-2: `activation_key` keying, fail-closed duplicates | `signal_evaluator.py:61-65` confirmed | CLOSED | HIGH |
| F2 | Five named downstream consumers still collapsed frames after registry fix | ARCH-RT-IDENTITY-PROV-1/C1 | 4 of 5 fully migrated (`root_cause_compiler_v1.py`, `report_compiler_v1.py`, `output_authority_provenance_builder_v1.py`, plus registry-adjacent index — each carries `activation_key` in core logic, not just output). **1 of 5 (`signal_interaction_builder.py`) is only cosmetically migrated** — `activation_key` surfaces as an output field (`participating_activation_keys`, lines 150/155/245/250) but node identity (`node_ids`, lines 63-66/145) and confidence lookup (`confidence_by_signal`, lines 220-224) remain bare-`signal_id`-keyed | PARTIALLY_CLOSED (not CLOSED — this is a correction of the package's own self-report) | HIGH — direct grep+read of current file |
| F3 | Four further consumers left deliberately un-migrated | Disclosed carry-forward, not fixed | Confirmed still bare-`signal_id`: `interpretation_display_layer_publish_v1.py:75-89,111-122`; `domain_score_assembler.py` (no `activation_key` in file); `narrative_report_compiler_v1.py:757` (`activation_key` explicitly blanked `""`); `intervention_selector_v1.py:149,203` | OPEN | HIGH |
| F4 | 0/186 manifests carried explicit `source_spec_id` (ARCH-RT-0 finding) | ADR-RT-004 honest-classification model; ARCH-RT-IDENTITY-PROV-1 gate | 0/191 manifests carry `source_spec_id` today — unchanged, and correctly so: this package's scope was classification honesty, not lineage backfill | OPEN (lineage) / CLOSED (honesty-of-disclosure, see F5) | HIGH |
| F5 | Inferred lineage risked being presented as explicit for beta claims | `provenance_status_v1.py` honest enum (`EXPLICIT_SPEC\|COMPILED_MANIFEST\|SOURCE_DOCUMENT_DERIVED\|LEGACY_INFERRED\|UNRESOLVED\|BLOCKED`); launch-critical gate (16 `pkg_kb47_*` rows `BLOCKED`/`beta_eligible_explicit: False`, 1 `signal_vitamin_d_low` row `COMPILED_MANIFEST`/`True`) | Confirmed implemented and gate-wired (`ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md`) | CLOSED (as disclosure control) | HIGH |
| F6 | Whether `BLOCKED`/dishonest-lineage packages are excluded from firing at runtime | Not claimed remediated by any package | **Independently confirmed NOT excluded.** `signal_evaluator.py:33-36` globs every `*/signal_library.yaml` under `knowledge_bus/packages/` with no provenance/status filter; `provenance_status` reaches `SignalResult` (`signal_evaluator.py:528`) and `ReportTopFindingV1` (`report_compiler_v1.py:817`) as a carried field only — no suppression logic exists at either site. All 20 `pkg_kb47_*` directories carry a `signal_library.yaml` and are therefore live-loadable. | OPEN | HIGH — this is a new, code-verified finding of this audit, not restated from any prior document |
| F7 | Hand-authored YAML duplicate WHY authority vs. investigation-spec hypotheses | ADR-RT-003 pilot: `signal_vitamin_d_low` compiled + runtime-promoted | Confirmed: `compiled_hypothesis.py:17-18` — `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS = frozenset({"signal_vitamin_d_low"})`, cardinality 1. `root_cause_registry_v1.py:28-90` — 41 tuples, 40 legacy YAML files, all hand-authored, no compiled-artefact consumption in the registry file itself | OPEN (estate); pilot itself CLOSED | HIGH |
| F8 | Dual WHY authority overlapping per signal | Not claimed | `root_cause_compiler_v1.py:539` (`is_runtime_promoted_compiled_signal`) branches mutually exclusively per `signal_id` — **no signal is served by both paths simultaneously**. Row-level frame collapse is fixed (all fired frames get a finding, `authority_scope` labelled `frame_specific`/`family_level`); hypothesis *content* for the 39 legacy signals remains family-level (same YAML content regardless of which frame fired) | DEFERRED_WITH_AUTHORITY — ADR-RT-003 Decision 6 explicitly authorises this transitional state; "immediate deletion... rejected for day-one" | HIGH |
| F9 | Root-cause compiler "signal-family-only, first-match" (sprint-plan carry-forward language) | — | This carry-forward wording is **stale relative to current code**. Row emission is no longer first-match (all frames emit); only hypothesis *content* is still family-level. Superseded by ARCH-RT-4/5C changes not reflected in the original carry-forward note | SUPERSEDED (the *wording*, not the underlying content-depth gap, which remains F7/F8) | MEDIUM-HIGH |
| F10 | Multiple package-generation cohorts = "dual signal libraries" | — | No runtime loader reads `knowledge_bus/packages/` as a parallel authority outside the `signal_library.yaml` glob feeding the single `SignalRegistry`. Package generations are compile-input cohorts of varying trust classification, not competing active authorities. `active_intelligence_authority_manifest.md` confirms only 7 launch-included compiled cards + 1 hypothesis artefact are independently "active"; the rest of the 192 directories are source material, mostly `legacy_retained`/`requires_review`/`BLOCKED` | SUPERSEDED (as a "dual libraries" framing — mischaracterizes coexistence as duplication) | MEDIUM-HIGH — full exhaustive read of `signal_library.yaml` estate-index loader path not independently completed line-by-line in this pass |
| F11 | `package_generation_inventory.md` (186 packages, `pkg_kb52c_*`=67) currency | — | Live: 192 directories / 191 manifests, `pkg_kb52c_*`=72 (grew, not shrank). Document is stale and must not be cited as current without regeneration | SUPERSEDED / STALE | HIGH |
| F12 | Wave 1 launch acceptance | ARCH-RT-6 `accepted_for_wave1_launch`; `validate_day_one_architecture.py` fail-closed validator; Sentinel pack | Confirmed as a bounded, documented acceptance distinct from whole-estate completion | CLOSED (bounded scope only) | HIGH |
| F13 | Controlled beta authorisation | Eight-block beta-readiness programme | `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` §10/§12: explicitly **not authorised** | OPEN | HIGH |
| F14 | PSI runtime wiring | ARCH-RT-5E: `deferred_non_launch_blocker` | Confirmed no launch-path importer of the PSI loader; classification stands, not a silent duplicate-authority risk while unwired | DEFERRED_WITH_AUTHORITY | HIGH |

---

## 6. Quantitative outputs (independently verified, not inherited)

| Metric | Value | Method |
|---|---:|---|
| Audit papers inventoried | 185 | Filename+content triage (fork) |
| Planning papers inventoried | 19 | Filename inventory (fork) |
| Package directories on disk | 192 | Direct `ls`/count (fork) |
| Package manifests (`package_manifest.yaml`) | 191 | Direct count; one directory lacks a manifest |
| Manifests with explicit `source_spec_id` field | 0 / 191 | Direct grep/scan of manifest files |
| Manifests with `activation_key:` field on disk | 0 / 191 | Direct grep/scan |
| Manifests with `legacy_retained:` field on disk | 0 / 191 | Direct grep/scan |
| `pkg_kb52c_*` packages | 72 (was 67 at ARCH-RT-0, 2026-05-28) | Direct count |
| Launch-critical `pkg_kb47_*` rows, `BLOCKED`/`beta_eligible_explicit: False` | 16 | `ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md`, cross-checked: all 20 `pkg_kb47_*` directories confirmed to carry a live `signal_library.yaml` |
| Compiled hypothesis artefacts | 1 (`signal_vitamin_d_low`) | `compiled_hypothesis.py:17-18` frozenset, cardinality confirmed |
| Legacy hypothesis YAML files | 40 | Direct count, `knowledge_bus/root_cause/hypotheses/` |
| Root-cause registry targets | 41 | Direct count, `root_cause_registry_v1.py:28-90` (homocysteine registers 2 signal_ids off 1 shared loader) |
| Downstream consumers fully migrated to `activation_key` (of 5 named) | 4 | Code read: `root_cause_compiler_v1.py`, `report_compiler_v1.py`, `output_authority_provenance_builder_v1.py`, registry-adjacent index |
| Downstream consumers cosmetically migrated (output field only, core logic still `signal_id`) | 1 (`signal_interaction_builder.py`) | Code read — independent finding of this audit |
| Downstream consumers not migrated (disclosed carry-forward) | 4 | Code read: `interpretation_display_layer_publish_v1.py`, `domain_score_assembler.py`, `narrative_report_compiler_v1.py`, `intervention_selector_v1.py` |
| Estate-indexed compiled cards (launch-active) | 7 (per `active_intelligence_authority_manifest.md`) — Cursor's document states 10; not reconciled in this pass, see Variance report | See Variance report §on card counts |
| Active signal families / activation keys / multi-frame families | Not independently re-derived by this audit from a fresh `SignalRegistry` load in this session (Cursor's 139/197/51 figures were not re-run against live code by either fork) | UNVERIFIABLE by this audit — flag for future verification, do not restate Cursor's figures as independently confirmed |

**Where a count could not be independently re-derived**, it is marked UNVERIFIABLE above rather than restated from Cursor's report, per the independence rule.

---

## 7. Scope distinctions (must not be merged)

- **Wave 1 launch-condition acceptance** (`accepted_for_wave1_launch`) ≠ **whole-estate day-one architecture completion**. The former is real and validator-enforced; the latter still has open obligations (§ Open Obligations document).
- **Provenance honesty/disclosure controls** (CLOSED) ≠ **explicit lineage migration** (OPEN) ≠ **runtime non-reachability of dishonest-lineage packages** (this audit found reachability is NOT restricted — a distinct, more concrete gap than "lineage is merely undocumented").
- **WHY dual authority as an accepted transitional posture** (DEFERRED_WITH_AUTHORITY per ADR-RT-003) ≠ **WHY estate migration/retirement** (OPEN, no target date set).
- **Package-generation coexistence** (not itself a defect) ≠ **stale inventory documents describing that coexistence** (a real, separate hygiene defect — §F11).

## 8. Non-claims

This reconciliation does **not**: declare day-one architecture complete; declare controlled beta ready; author a prose-generation or content-promotion package; invent new architecture requirements beyond ADR-RT-001–004 and the day-one sprint plan; change runtime, schema, medical-content, or test files; treat Cursor's counts, file references, or closure sequence as correct without the independent verification recorded above.
