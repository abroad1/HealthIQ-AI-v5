# Final Confirmation Review: Transition Plan v3 (WP0 / WP1 only)

**Document reviewed:** `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md`  
**Reviewer:** Cursor  
**Date:** 2026-05-28  
**Scope:** Confirm whether WP0 and WP1 can be safely authored — no full strategy re-review.

---

## Verdict

| Question | Answer |
|---|---|
| **Author WP0?** | **Yes** |
| **Author WP1?** | **Yes**, with two WP-frontmatter corrections (see §6) |
| **Material baseline wrong?** | **No** — counts in §2.2 are approximate; WP0 must reconcile (expected) |
| **WP0/WP1 deliverables sufficient?** | **Yes**, with three small additions recommended |
| **Launch blockers missing?** | **One minor gap** (activation compile path); otherwise covered in Phase 8–9 |
| **WP0/WP1 mis-scoped?** | **WP1 risk/classification** needs tightening; sequencing is correct |

**v3 is accurate enough to formalise ARCH-RT-0 and ARCH-RT-1.** Do not author WP2+ until WP1 ADRs are approved.

---

## 1. Is v3 accurate enough to author WP0?

**Yes.**

WP0 actions (§7 Phase 0) match the repo:

- Pass 3 / investigation spec v3 corpus as canonical research (9 `*_Pass_3.json` files, ~153 specs).
- Heterogeneous packages (~186 dirs); **not** a simple s24-vs-kb52 story — v3’s five-generation table is directionally right and correctly marked **“must be verified.”**
- PSI: **20** packages with PSI on disk **and** manifest opt-in (grep confirms); **zero** orchestrator/evaluator consumption — accurate.
- Manual `root_cause_registry_v1.py` + hand YAML — accurate.
- Hard-coded `wave1_subsystem_evidence.py` — accurate.
- `signal_id` collision via lexicographic overwrite in `SignalRegistry._load` — accurate (live defect).
- `SubsystemEvidenceV1` lacks card intelligence fields — accurate (`evidence_role` exists but is null by design in DOMAIN-UX1C).

**WP0 deliverable list is complete** for downstream scoping: traceability matrix, collision inventory, PSI report, package generation inventory, root-cause registry inventory, legacy retirement candidates.

**Recommend adding to WP0 acceptance criteria (not blocking authoring):**

1. **`docs/architecture/investigation_spec_corpus_inventory.md`** — file list, spec count, contract version, validation status (`validate_investigation_spec.py` run summary).
2. **Explicit row in collision inventory** for `signal_alt_high` (all `pkg_kb52c_alt_high_*` paths + which wins today).
3. **Note whether `source_document` appears in manifests** vs absence of `source_spec_id` (confirmed: manifests use `source_document`, not `source_spec_id`).

WP0 should remain **`change_type: CONTENT`**, **`risk_level: STANDARD`**. Read-only inventory scripts are fine if outputs land in `docs/architecture/` only.

---

## 2. Is v3 accurate enough to author WP1?

**Yes.**

WP1 correctly forces decisions that block all implementation:

- ADR-008 acceptance (already stated in v3 §2.4).
- **One-frame vs multi-frame** (§5) — the right gating question; must be decided in ADR-RT-002, not deferred again.
- Registry keying / `activation_key` options listed without assuming implementation.
- `SignalResult` provenance fields (currently **only** `signal_id` in `backend/core/models/signal.py`).
- Interaction map / phenotype map / root-cause registry family-vs-frame semantics.
- Package provenance policy (`source_spec_id` vs `legacy_retained`).
- Root-cause registry transition principles (manual tuple → generated registry).

Deliverables **ADR-RT-001 through ADR-RT-004** are sufficient for WP1.

**WP1 must not implement** registry/evaluator changes — docs/ADRs only. v3 STOP conditions (§7 Phase 1) enforce that.

---

## 3. Is any material as-is baseline still wrong?

**No material errors.** Only inventory-level imprecision v3 already defers to WP0:

| v3 statement | Quick check | Note |
|---|---|---|
| kb52c ~67 packages | `pkg_kb52*` ≈ **71** | Prefix split; include kb58/kb59/kb60/kb61 in inventory |
| s24 ~15 | `pkg_s24*` ≈ **31** | WP0 will correct |
| PSI “largest generation may be batch JSON” | kb52* mostly cites `Batch_*_Pass_3.json` in manifests | Correct implication |
| “PSI consumed by zero runtime analytics paths” | No `load_promoted_signal` in `orchestrator.py` / `signal_evaluator.py` | Correct |

Strategy, artefact split, PSI/ADR-008, live collision defect, and DTO versioning need — **all correct**. No need to re-open v1/v2 strategy.

---

## 4. Are WP0 and WP1 deliverables sufficient to prevent mis-scoped downstream work?

**Yes**, if WP1 ADRs are written to be **decisive** (not “options still open”).

WP0 prevents:

- Wrong pilot choice (inventory-driven Phase 3).
- Underestimating kb52 batch-JSON traceability (explicit STOP).
- Building duplicate PSI schema (explicit STOP).
- Starting compilers before collision map exists (`signal_id_collision_inventory.md`).

WP1 prevents:

- Full regeneration before one-frame vs multi-frame decision.
- `activation_key` assumed without ADR.
- Hypothesis work inside PSI/packages.
- Registry refactor without interaction-map / phenotype-map blast-radius note.

**Add to WP1 acceptance criteria:**

- ADR-RT-002 contains a **single chosen policy** (not a menu left open for WP4).
- ADR-RT-004 states **`source_spec_id` required on new compiles**; `legacy_retained` enum for grandfathered packages.
- Explicit statement: **`investigation_spec → signal_library` compile is a separate track from PSI** (only PSI translator exists today).

That is enough to scope WP2a–WP3 without drift.

---

## 5. Are any launch blockers still missing from the plan?

**Mostly covered** in §3 principles, §10 prohibitions, and Phase 8–9.

**Add explicitly to launch blocker list (Phase 9 or §10):**

- **No governed activation compile path** from investigation spec to package for estate-wide regeneration (sprint ingest scripts are not a day-one compile authority). Implied but worth one line so WP8 is not scoped as “PSI only.”

**Already adequate in v3:**

- Silent `signal_id` collapse.
- PSI runtime-dead if launch claims need signal-layer semantics.
- Manual card maps / hand root-cause authority.
- Missing `source_spec_id` / `legacy_retained`.
- Duplicate hypothesis authorities.
- Traceability audit (Phase 9).

No need to expand this review into full launch-gate analysis.

---

## 6. Would v3 cause WP0 or WP1 to be mis-classified, scoped, or sequenced?

### Sequencing

**Correct.** WP0 → WP1 → halt until ADRs approved → WP2a+. v3 §10 item 12 and §12 align with prior review.

### WP0 scope

**Correct** as CONTENT / STANDARD. Do not expand WP0 to:

- Write ADRs (that is WP1).
- Run compilers or change `SignalRegistry`.
- Fix collisions.

### WP1 classification — **correct before authoring**

v3 lists WP1 as:

```yaml
risk_level: HIGH
change_type: MIXED
```

**Deliverables are documentation only** (four ADRs). Unless WP1 also updates locked schemas in `knowledge_bus/schema/` (e.g. `package_manifest_schema`), classify WP1 as:

```yaml
risk_level: STANDARD  # or LOW
change_type: CONTENT
```

If manifest schema amendments are **in scope** for WP1 (recommended: **yes**, minimal `source_spec_id` / `legacy_retained` fields only), then:

```yaml
risk_level: HIGH
change_type: MIXED
```

with **explicit file allowlist**: `docs/architecture/ADR-RT-*.md`, `knowledge_bus/schema/package_manifest_schema.yaml` (provenance fields only), no `backend/core/**`.

**Do not** put registry/evaluator code in WP1 — that belongs to WP4 after ADR-RT-002 approval.

### WP0 vs WP2a overlap

WP2a (PSI gap) duplicates part of WP0 PSI inventory. **Acceptable** if WP0 produces the inventory and WP2a produces the **interpreted gap report** and consumption design pointers. Author WP0 first; WP2a references WP0 deliverables as inputs.

---

## 7. Direct answers (v3 §11 checklist)

1. **WP0?** — **Yes.**
2. **WP1?** — **Yes** (fix risk/type if doc-only).
3. **Baseline wrong?** — **No** (approximate counts only).
4. **Deliverables sufficient?** — **Yes** (minor additions in §4).
5. **Launch blockers missing?** — **Minor:** activation compile authority for full estate regen.

---

## 8. Authoring checklist (for Automation Bus)

**ARCH-RT-0**

- [ ] All deliverables under `docs/architecture/`
- [ ] Collision inventory includes `signal_alt_high` and homocysteine dual-`signal_id` cases
- [ ] PSI: 20/20 disk+manifest vs 166 without
- [ ] No code changes to `backend/core` or `knowledge_bus/packages` content

**ARCH-RT-1**

- [ ] Four ADRs merged only after human approval
- [ ] ADR-RT-002 picks one-frame **or** multi-frame — not both “for later”
- [ ] No `SignalRegistry` / `SignalEvaluator` edits in WP1
- [ ] Clarify CONTENT vs MIXED in WP front matter

---

## Bottom line

v3 incorporates the second-pass corrections that matter for WP0/WP1: **runtime-dead PSI**, **live multi-frame collapse**, **heterogeneous package estate**, **mandatory card DTO versioning**, and **split downstream WPs**.

**Proceed to author WP0 and WP1.** Do not author implementation work packages until ADR-RT-002 (identity/registry) is human-approved.

---

*Confirmation review only. No code, work packages, or merges were created or modified.*
