# HealthIQ — As-Is to Day-One Architecture Transition Plan v2
## Second-Pass Review — Claude Code

**Reviewer:** Claude Code  
**Date:** 2026-05-28  
**Reviewed document:** `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v2.md`  
**Review scope:** Accuracy against actual codebase, readiness to convert to Automation Bus work packages  
**Status:** Not yet ready. Specific blockers identified below.

---

## 1. Overall verdict

v2 is substantially more accurate than v1 and the revised framing (use PSI, don't build a duplicate signal-intelligence layer, keep ADR-008) is correct. However, v2 understates two critical facts that must be corrected before work packages are authored:

1. PSI is not "not fully consumed" — it is consumed by **zero runtime paths**. The loader exists. The YAML files exist for 20 packages. Nothing in the analytics pipeline reads them.
2. The multi-frame signal collapse is not a latent risk — it is **active and documented policy** in `signal_evaluator.py`. Three of the four ALT-high research frames are silently discarded at runtime today.

Until these two facts are accurately named in the plan, work packages authored from it will scope their remediation incorrectly.

---

## 2. Question-by-question findings

### Q1. Does v2 correctly reflect the existing PSI / ADR-008 architecture?

**Mostly yes, one significant understatement.**

v2 correctly identifies: PSI schema, loader, translator, and schema constraints. It correctly notes PSI is not fully consumed. It correctly preserves ADR-008 (no hypothesis content in PSI).

The understatement: v2 says PSI "is not fully opted into or consumed across the runtime estate." The actual position is:

```text
load_promoted_signal_intelligence_for_package()
  → called only from: backend/tests/unit/test_promoted_signal_intelligence_kb_s47d.py
  → called from analytics pipeline: NOWHERE
```

PSI is dead at runtime. The 20 kb47 PSI artefacts on disk have no runtime consumer. This changes the scope of WP2 (PSI gap closure) from "add missing PSI opt-ins and check runtime consumption" to "wire PSI into the pipeline for the first time, then establish opt-in."

**Second understatement:** v2 mentions "there appear to be at least two generations of package maturity." The actual generations are:

| Generation | Count | PSI on disk | PSI in manifest | Signal lib source |
|---|---|---|---|---|
| legacy (pkg_*) | ~12 | No | No | Hand-authored |
| s24 | ~15 | No | No | Investigation spec (yaml) |
| kb45 | 10 | No | No | Batch JSON |
| kb47 | 20 | Yes | Yes | Investigation spec (yaml) |
| kb52c | 67 | No | No | Batch JSON (`Batch_5_Pass_3.json`) |

Total: 187 packages across five generations. Only one generation (kb47, 20 packages) has PSI. The largest generation (kb52c, 67 packages) has none.

**v2 correction needed:** Replace "at least two generations" with the actual generation inventory above.

---

### Q2. Is accepting ADR-008 the right decision?

**Yes. Accept ADR-008.**

ADR-008 (PSI excludes hypotheses, hypothesis_ranking, narrative) is architecturally correct. The PSI schema explicitly forbids those keys at root level. Reversing it would:

- Require stuffing ranked hypothesis graphs into PSI, bloating the signal-layer artefact with WHY reasoning that belongs in the hypothesis layer
- Eliminate the clean separation between "what the signal means" and "why it is occurring"
- Require the PSI schema to version twice as fast as it does now

The compiled hypothesis artefact is the right place for hypotheses. ADR-008 gives that boundary its reason to exist. Keep it.

---

### Q3. Is the proposed artefact split correct?

**Yes, the split is correct. One gap in the PSI framing.**

- **packages = signal activation:** Correct. The signal_library.yaml files are activation definitions — threshold conditions, trigger direction, supporting marker relationships. This is the right scope.

- **PSI = signal-layer semantics:** Correct as a target definition, but the current PSI is not actually part of the architecture — it is an off-pipeline artefact. The plan must name this explicitly rather than treating PSI as a live layer that needs extending.

- **compiled hypothesis artefact = WHY/root-cause:** Correct. The hand-authored root-cause YAML files under `knowledge_bus/root_cause/hypotheses/` are the current WHY layer (40 signals registered in `root_cause_registry_v1.py`). The plan correctly proposes replacing these with research-derived compiled artefacts.

- **Health Systems Card evidence artefact = UX projection:** Correct. `wave1_subsystem_evidence.py` is the current hard-coded authority. Its Python `_Wave1SubsystemDef` structs carry only: subsystem_id, subsystem_label, expected_marker_ids, source_trace. No marker_role, no relationship_kind, no rationale_short, no mechanism_line, no missing_policy_line, no visibility_tier. `SubsystemEvidenceV1` (the DTO) also lacks all of these fields. The plan correctly identifies the gap but does not name it at the DTO level.

**Gap:** v2 section 4.7 (DTOs) says SubsystemEvidenceV1 "may need versioned extension." This is confirmed: the fields marker_role, relationship_kind, rationale_short, missing_policy_line, mechanism_line, and visibility_tier **do not exist** in the current DTO. This is not a maybe — it is a required addition. Name it as such.

---

### Q4. Is activation_key required, or can signal_id + spec_id safely resolve multi-frame identity?

**signal_id + spec_id can work, but spec_id is not currently in signal_library entries.**

The `signal_evaluator.py` collapse policy at lines 54–63:

```python
# Deterministic duplicate policy: when the same signal_id appears in
# multiple package files, keep the definition from the lexicographically
# later path and overwrite the earlier one.
if str(path) <= existing_source:
    continue
```

This policy is intentional and documented. It is also the root of the multi-frame collapse problem. For ALT high, four packages share `signal_id: signal_alt_high`:

```text
knowledge_bus/packages/pkg_s24_alt_high_hepatocellular_injury/signal_library.yaml
knowledge_bus/packages/pkg_kb52c_alt_high_hepatocellular_injury_pattern/signal_library.yaml
knowledge_bus/packages/pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern/signal_library.yaml
knowledge_bus/packages/pkg_kb52c_alt_high_muscle_source_or_exertional_pattern/signal_library.yaml
```

Three frames are silently dropped. Only the lexicographically last path wins.

**On activation_key vs signal_id + spec_id:**

`activation_key` requires a new field in every signal_library entry — large blast radius, requires schema version bump, affects all 187 packages.

`signal_id + spec_id` is cheaper if `spec_id` (or `source_spec_id`) is already available in the signal library. It is not currently. The `source_document` is in `package_manifest.yaml`, not in the signal_library itself.

**Recommendation:** Before choosing, answer one question first: does the runtime need to fire **one** signal per direction or **multiple** frames per direction?

- If **one per direction** (e.g., the most evidenced frame wins based on patient data): keep `signal_id` as the key, but replace the lexicographic fallback with a governed arbitration policy. This is the smaller change.
- If **multiple frames per direction** (all valid frames fire and the assembler resolves): change to `(signal_id, package_id)` keying. Larger downstream change to evaluator, InsightGraph, compiler chain.

The plan correctly defers this to an ADR. But the ADR must answer the one-vs-many question first, because the registry change follows from that answer, not the reverse.

---

### Q5. What exactly must change in SignalRegistry to stop silent duplicate collapse?

The minimum required change, regardless of the one-vs-many decision:

1. **Remove the silent lexicographic overwrite policy.** Replace with one of:
   - Hard error on duplicate `signal_id` (forces explicit resolution before ship)
   - Explicit `priority` or `frame_discriminator` field in signal_library entries
   - Keyed by `(signal_id, package_id)` tuple

2. **If keeping one-per-direction:** Add a governed arbitration rule that selects the active frame based on a declared priority field or package-generation seniority, with a warning log when multiple frames exist. The arbitration rule must be deterministic and documented.

3. **If allowing multi-frame:** The `_signals_by_id` dict must become `_signals_by_key: Dict[Tuple[str, str], dict]` where the key is `(signal_id, package_id)`. `get_all_signals()` returns all frames. The evaluator returns per-frame results. Downstream compilers must handle multiple results for the same `signal_id`.

The plan's Phase 1 and Phase 5 cover this, but WP1 needs to explicitly output the one-vs-many decision, and WP4 needs to be scoped to a specific implementation of the chosen option, not left open-ended.

---

### Q6. What is the correct transition path for root_cause_registry_v1.py?

Current state:
- 40 signal registrations, all `registration_source: "manual_v1"`
- Each entry: `(signal_id, loader_callable, asset_filename)`
- No `source_spec_id` or research provenance
- Loader validates: duplicate signal_id, callable loader, non-empty asset, asset loads, hypotheses non-empty
- Fingerprinting exists (`_hypothesis_asset_fingerprint`) but is not enforced in any automated gate

Transition path (recommended):

**Phase A (no schema work yet):** Add `source_spec_id` to `RootCauseTargetSpec` as an optional field. Populate it where the spec is known. This establishes provenance without changing the compiler interface. Can be a CONTENT work package.

**Phase B (after compiled hypothesis schema is locked):** Create the compiled hypothesis artefact for a pilot signal. The artefact must carry hypothesis_id, physiological_claim, hypothesis_rank, evidence_strength, confirmatory_test_refs, evidence_for/against rule representation. Add a new loader function that reads compiled artefacts rather than the hand-authored YAML. Register the new loader alongside the existing one in the registry (shadow mode).

**Phase C (after divergence adjudication):** Replace manual YAML authority with compiled artefact authority for adjudicated signals. Remove manual loaders from the tuple list. The compiler interface (`get_root_cause_targets()` → `List[Tuple[str, HypothesesLoader]]`) may remain unchanged if the compiled loader returns the same payload shape.

**What must NOT happen:** Do not change the compiler before the compiled artefact format is locked and validated. The registry should gain compiled sources without losing the existing manual sources until divergence is confirmed.

---

### Q7. What is the safest first pilot candidate?

v2 says Phase 0 inventory must decide. That is correct. From what is visible now:

**Best current candidate: `signal_ldl_cholesterol_high`**

Evidence:
- One investigation spec: `inv_ldl_high_dyslipidaemia_v1.yaml`
- One s24 package: `pkg_s24_ldl_high_dyslipidaemia`
- One root-cause YAML: `ldl_cholesterol_high_hypotheses_v1.yaml` (registered in registry)
- No kb52c multi-frame packages visible for LDL high
- Single-frame signal — no collision in SignalRegistry

This gives: spec → package → root-cause YAML all present. PSI is absent (no LDL kb47 package visible), so the PSI pilot compile step can be tested without a pre-existing PSI to invalidate.

**Warning:** ALT should NOT be the first pilot. v2 correctly suggests it for the multi-frame identity pilot (Phase 5). Using it earlier collapses the identity problem and the compile pilot into the same work package.

**CRP should NOT be the first pilot** either. CRP has a legacy `pkg_inflammation_crp_context`, a governed `pkg_s24_crp_high_inflammation`, and the root-cause YAML `systemic_inflammation_hypotheses_v1.yaml` maps to `signal_systemic_inflammation`, not `signal_crp_high`. This cross-naming between signal_id in the package and signal_id in the root-cause registry will add noise to a first pilot.

---

### Q8. Which runtime loaders, DTOs, schemas, validators, manifests, or Sentinel guards are still missing?

**Missing schemas (none of these files exist):**

```text
knowledge_bus/schema/compile_manifest_schema_v1.yaml          — MISSING
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml       — MISSING
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml — MISSING
```

The only schema that exists (and is relevant) is `promoted_signal_intelligence_schema_v1.yaml`.

**Missing from SubsystemEvidenceV1 DTO (`backend/core/models/results.py:176`):**

```text
marker_role         — MISSING (not a field on the DTO today)
relationship_kind   — MISSING
rationale_short     — MISSING
mechanism_line      — MISSING
missing_policy_line — MISSING
visibility_tier     — MISSING
```

Any work package that adds card evidence intelligence must version this DTO before frontend consumption is possible.

**Missing runtime wiring:**

```text
PSI loader in analytics pipeline           — MISSING (loader exists, not wired)
Card evidence YAML loader                  — MISSING (no YAML authority exists yet)
Compiled hypothesis artefact loader        — MISSING (no artefact schema exists yet)
```

**Missing Sentinel guards:**

```text
raw_research_runtime_read_forbidden        — MISSING
psi_present_but_not_consumed               — MISSING
manual_card_evidence_authority_forbidden   — MISSING
duplicate_signal_id_collapse_guard         — MISSING
package_without_source_spec_id_guard       — MISSING
root_cause_yaml_as_permanent_authority     — MISSING
compiled_artifact_missing_manifest_guard   — MISSING
```

The Sentinel pack at `sentinel/packs/escaped_defects_v1.json` should be checked before WP1 is authored to confirm none of these are already registered under different names.

**Missing validators:**

```text
backend/scripts/validate_compile_manifest.py          — MISSING
backend/scripts/validate_compiled_hypothesis.py       — MISSING
backend/scripts/validate_health_system_card_evidence.py — MISSING
```

(`validate_promoted_signal_intelligence.py` exists and is the pattern to follow.)

---

### Q9. Which phases are too broad for single Automation Bus work packages?

**WP2 — PSI gap closure and manifest foundation** is too broad.

It combines: PSI runtime wiring audit, manifest schema design, provenance validator additions. These are different risk levels. The manifest schema design is CONTENT. PSI runtime wiring is BEHAVIOUR (it changes what the analytics pipeline reads). They must be separate work packages.

Split into:
- WP2a: PSI gap analysis — CONTENT/STANDARD — confirm coverage, opt-in status, runtime consumption gap
- WP2b: Compile manifest schema — CONTENT/STANDARD — schema only, no code
- WP2c: PSI runtime wiring — BEHAVIOUR/HIGH — first WP that actually routes PSI into a pipeline

**WP5 — Health Systems Card evidence pilot** is too broad.

It includes: schema definition, visibility-tier policy, pilot compile, YAML loader, DTO versioning, assembler change, frontend render update. That is at minimum four work packages across CONTENT and BEHAVIOUR tiers.

Split into:
- WP5a: Card evidence schema and role translation policy — CONTENT/STANDARD
- WP5b: Compile one subsystem artefact and validate — CONTENT/STANDARD
- WP5c: Backend loader + assembler change + DTO versioning — BEHAVIOUR/HIGH
- WP5d: Frontend render update (after DTO is locked) — BEHAVIOUR/HIGH

**WP6 — Compiled hypothesis / root-cause pilot** is too broad.

It includes: compiled hypothesis schema, investigation spec → hypothesis compile, root_cause_registry transition design, confirmatory test mapping, compiler input swap. Each of these is a separable deliverable.

Split into:
- WP6a: Compiled hypothesis schema — CONTENT/STANDARD
- WP6b: Pilot compile + divergence report — CONTENT/STANDARD
- WP6c: Registry transition — BEHAVIOUR/HIGH

All other work packages (WP0, WP1, WP3, WP4, WP7, WP8, WP9) are appropriately scoped.

---

### Q10. What would still block launch if unresolved?

**Hard blockers — ship is not possible:**

1. **Signal collapse for multi-frame markers is live.** ALT has 4 packages; 3 frames are silently dropped. If ALT's metabolic-steatotic and muscle-source frames are clinically meaningful, those signals are not firing. This is not a future risk — it is a current defect in the runtime.

2. **PSI is dead from the runtime's perspective.** 20 packages have PSI artefacts. Zero runtime paths read them. If PSI is part of the target architecture, it must be wired in before launch. If it is not, the 20 PSI artefacts are waste.

3. **SubsystemEvidenceV1 cannot carry research intelligence without DTO versioning.** The card evidence artefact, when compiled, cannot reach the frontend without DTO fields that do not exist. This is a schema + transport + render chain that must be built before the architecture is functional end-to-end.

4. **root_cause_registry_v1.py has no source_spec_id.** 40 root-cause signals have no traceable link to investigation specs. Any launch-readiness audit that requires "every user-facing claim traces to investigation spec → compiled artefact → DTO" fails immediately here.

5. **No compile manifests exist.** The plan's launch gate (Phase 10, item 8) requires hash-valid compile manifests. None exist. The schema for them does not exist. This is a prerequisite for the entire compiled architecture.

6. **kb52c packages source from batch JSON, not investigation specs.** 67 packages (the largest generation) cite `source_document: knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json`. This is a batch file, not a v3 investigation spec. These packages cannot be regenerated via the `investigation_spec → PSI → compiled hypothesis` pipeline until their source specs are extracted or separately authored. The inventory (Phase 0) must classify these explicitly.

**Near-blockers — launch is unsafe without resolution:**

7. **No Sentinel guard on duplicate signal_id collapse.** The lexicographic overwrite is silent. A future package addition can silently displace an existing signal without any alert.

8. **No Sentinel guard on raw investigation spec runtime reads.** If anything in the pipeline reads a batch JSON or spec YAML at runtime, there is no gate to catch it.

9. **IDL / retail prose safety is not consistently applied to hypothesis text.** The root-cause compiler outputs summaries from `summary_template` fields. Whether these pass through IDL before reaching the frontend is not confirmed.

---

## 3. Corrections required before work packages are authored

The following items must be corrected in v2 before WPs are written:

**Must fix:**

1. Replace "not fully consumed" with "consumed by zero runtime paths" when describing PSI.

2. Add the five-generation package table (legacy / s24 / kb45 / kb47 / kb52c) with counts and PSI status. The 67 kb52c packages and their batch JSON source_document must be explicitly classified.

3. Name the ALT four-package collision explicitly as a current live defect, not a latent risk.

4. Confirm that `SubsystemEvidenceV1` is missing the required intelligence fields. This is not a "may need extension" — it is a required schema version.

5. Phase 2 (PSI gap closure) must distinguish: audit of opt-in status (CONTENT), and runtime wiring (BEHAVIOUR). These are different risk levels and cannot be in the same WP.

**Should fix before authoring:**

6. WP5 and WP6 need decomposition as described in Q9 above.

7. The ADR in Phase 1 must explicitly answer: one-frame-per-direction or multi-frame? The registry change and the evaluator change are downstream consequences of that answer.

8. The kb52c batch-JSON source problem needs a decision: treat all kb52c packages as "legacy-retained" (no compiled pipeline path) or extract individual investigation specs for them. This changes the Phase 9 full regeneration scope significantly.

---

## 4. What is solid in v2 (do not revert)

- ADR-008 acceptance: correct.
- Artefact split (packages / PSI / compiled hypothesis / card evidence): correct.
- Rejecting activation_key as a default assumption: correct.
- Retaining legacy root-cause YAML for parity and divergence, not as permanent authority: correct.
- STOP condition: no full regeneration until duplicate signal_id behaviour is resolved: correct and essential.
- Phase 0 inventory-first approach: correct. The five-generation reality makes this mandatory.
- Non-goals section (§9): well-scoped. Keep it.
- Prohibited shortcuts (§10): complete and enforceable. Keep it.

---

## 5. Summary

v2 is directionally correct and architecturally sound. It is not yet accurate enough to convert into Automation Bus work packages because it understates two live defects (PSI runtime gap, signal collapse), underestimates the package estate complexity (five generations, not two), and conflates CONTENT and BEHAVIOUR work in WP2, WP5, and WP6.

Correct the five items above, decompose the three broad WPs, and the plan will be ready for formal work package authoring.

The inventory phase (WP0/Phase 0) must produce explicit answers to: how many packages per generation, which have source_spec_id, which have PSI, and which kb52c packages can be traced to formal investigation specs. Without that inventory, every downstream WP scope will be wrong.
