# HealthIQ AI — Architecture Closure Sequence (Claude Code Independent Verification)

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1-CC |
| **Companion** | `HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION_CC.md`; `HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS_CC.md` |
| **Rule** | Minimum safe outcome-based packages for the *launch-critical* cohort only. No implementation prompts. No estate-wide or medical-content packages authored here. |
| **Date** | 2026-07-25 |

---

## 1. Anti-micro-sprint gate

Same discipline as the historical day-one plan (ADR-RT sequence) and Cursor's own closure sequence — independently re-derived here rather than copied, because it follows directly from the sprint plan's own stated philosophy (§2 of `healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`): "Do not reduce further by combining decision work, runtime behaviour changes, schema/validator changes, card DTO and frontend changes, root-cause compiler changes, full estate regeneration."

**Do not split further into:** a separate sprint per collapse-surface file (all 5 belong in one behaviour package); a separate sprint per package-generation prefix; a docs-only inventory-refresh sprint decoupled from any package that touches the same evidence.

**Do not combine:** frame-identity consumer completion (runtime behaviour, analytics compilers) with provenance/lineage work (knowledge-asset governance, medical-extraction dependency) with WHY-authority completion (medical-hypothesis compile, compiler behaviour, medical-review gated). Each is a different risk class under the Automation Bus SOP and mixing them recreates the exact governance failure ADR-RT-001 was written to correct.

**Deferred, not required for launch-critical closure:** estate-wide activation compile (no governed compiler replaces package generations — OBL-CC-005's stale-inventory concern does not by itself justify this); PSI wiring (no new launch-critical claim depends on it); card evidence beyond Wave 1; medical-content/prose depth (a distinct programme, explicitly out of architecture-closure scope); secrets/hygiene re-audit (operational, not Intelligence Core).

---

## 2. Target outcome of this sequence

After PKG-1-CC through PKG-3-CC, the repository should be able to truthfully claim:

1. Every launch-path consumer that ranks, joins, or explains a signal uses `activation_key` (or an explicitly governed frame-selection policy) — including the interaction-builder gap this audit found, which the historical carry-forward register did not name.
2. Launch-critical packages either carry explicit lineage or are consistently non-claimable **and non-reachable** — closing the reachability gap this audit found (§OBL-CC-003), not merely the disclosure gap already closed by ARCH-RT-IDENTITY-PROV-1.
3. Launch-critical WHY is compiled-promoted or honestly classified legacy-active, with no document implying compiled-estate completion.

This sequence does not declare architecture-complete or beta-ready. Controlled beta (OBL-CC-006) remains a separate, later gate.

---

## 3. Package sequence (minimum: 3)

```text
PKG-1-CC  Launch-path activation-frame identity completion (5 surfaces, not 4)
   → PKG-2-CC  Launch-critical provenance lineage AND runtime-reachability honesty
      → PKG-3-CC  Launch-critical WHY/root-cause authority completion
```

This is the same minimum package count Cursor's closure sequence proposed. Independent evidence supports 3 as the floor, not fewer: each package touches a distinct SOP risk class (pure runtime behaviour / knowledge-asset governance + provenance / medical-hypothesis compile) that the sprint plan's own philosophy forbids merging. This audit found no basis to propose either a 4th mandatory package or a reduction below 3 for the launch-critical cohort.

---

### PKG-1-CC — Launch-path activation-frame identity completion

| Field | Content |
|---|---|
| **product outcome** | Every launch-path consumer that ranks, joins, groups, or selects among signals uses `activation_key` as its matching key, not bare `signal_id` — closing all 5 verified surfaces (4 disclosed carry-forward + 1 newly found in `signal_interaction_builder.py`). |
| **obligations closed** | OBL-CC-001 |
| **verified code scope** | `interpretation_display_layer_publish_v1.py` (:75-89, :111-122); `domain_score_assembler.py` (all `signal_id`-only fields); `narrative_report_compiler_v1.py` (:757 lead-frame resolution); `intervention_selector_v1.py` (:149, :203); `signal_interaction_builder.py` (`node_ids` :63-66/145, `confidence_by_signal` :220-224) |
| **why not absorbed elsewhere** | Pure runtime behaviour change on analytics compilers; mixing with knowledge-asset provenance extraction (PKG-2-CC) or hypothesis compile (PKG-3-CC) recombines distinct SOP risk classes |
| **medical-review dependency** | None for identity-preservation mechanics; required only if a frame-*selection* policy (choosing among competing frames rather than preserving all) is introduced |
| **STOP gates** | STOP if scope expands into PSI wiring, prose, or estate regeneration. STOP if any consumer requires a new medical frame-priority policy without an approved ADR. STOP if the pre-work check (below) finds zero live multi-frame exposure on all 5 surfaces — in that case, downgrade to a smaller hardening/test package rather than a full behaviour rewrite, and say so explicitly rather than treating this package as automatically warranted at full size. |
| **pre-work check (recommended, not yet done)** | Before sizing this package, confirm whether any currently-active Wave 1 multi-frame family (of the ~51 claimed multi-frame families — figure not independently re-derived by this audit, see Reconciliation §6) actually reaches all 5 surfaces today. Neither this audit nor Cursor's resolved this; it changes urgency, not correctness of the finding. |
| **acceptance condition** | No remaining bare-`signal_id`-only collapse on any launch-path analysis→DTO consumer for multi-frame families; `signal_interaction_builder.py`'s node/confidence logic is `activation_key`-keyed, not merely output-annotated. |

---

### PKG-2-CC — Launch-critical provenance lineage and runtime-reachability honesty

| Field | Content |
|---|---|
| **product outcome** | Launch-critical packages either carry explicit `source_spec_id` lineage, or are consistently non-claimable **and non-reachable** at runtime — closing both the disclosure gap (already done) and the reachability gap (not done; §OBL-CC-003). |
| **obligations closed** | OBL-CC-002; OBL-CC-003; touches OBL-CC-005 for the specific cohorts extracted/reclassified in this package |
| **verified code scope** | `backend/core/analytics/signal_evaluator.py:33-36` (`_iter_signal_library_paths` — needs a provenance-aware filter or an explicit, documented decision not to filter); `provenance_status_v1.py`; the 20 `pkg_kb47_*` package directories; `knowledge_bus/schema/package_manifest_schema.yaml` |
| **why not absorbed elsewhere** | Requires research-asset extraction/attach plus a runtime-load-policy decision — different risk class from compiler identity (PKG-1-CC) and from WHY compile content (PKG-3-CC) |
| **medical-review dependency** | Yes, if extraction creates or selects among medical frames from batch JSON. Attach-only of already-approved `inv_` specs may be lower-novelty CONTENT. Any runtime-load-policy change (excluding `BLOCKED` packages from firing) is BEHAVIOUR, not CONTENT, and must be classified accordingly. |
| **STOP gates** | STOP if asked to invent `source_spec_id` values without source artefacts. STOP if estate-wide regeneration of all 191 packages is forced into this package. STOP if excluding `BLOCKED` packages from firing would silently remove a currently-relied-upon Wave 1 launch signal — that would require a launch-relevance review, not a quiet behaviour change. |
| **acceptance condition** | Launch-critical cohort (currently 16 `pkg_kb47_*` rows + any others discovered) shows explicit lineage **or** is both non-claimable and non-reachable; `signal_evaluator.py`'s load path and `provenance_status_v1.py`'s classification agree on which packages fire. |

---

### PKG-3-CC — Launch-critical WHY/root-cause authority completion

| Field | Content |
|---|---|
| **product outcome** | For the launch-critical signal cohort, WHY authority is compiled-promoted or explicitly classified legacy-active — no document may imply "compiled WHY complete" while 40 YAML targets remain on family-level content. |
| **obligations closed** | OBL-CC-004, for the launch-critical cohort only — does not close whole-estate YAML retirement |
| **verified code scope** | `compiled_hypothesis.py` (currently a hardcoded 1-element frozenset); `root_cause_compiler_v1.py:539` (branch point); `root_cause_registry_v1.py:28-90` (41 tuples); `knowledge_bus/root_cause/hypotheses/*.yaml` (40 files) |
| **why not absorbed elsewhere** | Touches medical hypothesis content and root-cause compiler behaviour; medical-review gated; must not mix with provenance extraction |
| **medical-review dependency** | Yes, for any new/changed compiled hypothesis content. Classification-only (labelling legacy-active without content change) may proceed without new medical review, but must not claim a medical upgrade. |
| **STOP gates** | STOP if the package attempts a whole-estate 41-target compile in one pass without a cohort boundary. STOP if YAML deletion is proposed without promotion/parity evidence. STOP if the ADR-RT-003 Decision 6 transition stages (provenance columns → `activation_key` keying → manifest-backed registry → generated registry) are skipped rather than advanced in order. |
| **acceptance condition** | Each launch-critical target has one declared authority class; dual-path remains only where explicitly classified; no document (including future audit-paper updates) implies estate-wide compiled-WHY completion. |

---

## 4. What remains after PKG-1-CC…3-CC (explicitly out of minimum sequence)

| Obligation | Why deferred |
|---|---|
| Estate-wide activation compile | Original whole-estate target; not required for launch-critical honesty once PKG-2-CC holds |
| PSI wiring | Already `deferred_non_launch_blocker`; no new launch-critical claim requires it |
| Card evidence beyond Wave 1 | Wave 1 card authority already closed (card-count discrepancy is a documentation question, OBL-CC-005, not a blocker) |
| Medical prose/content depth | Separate programme; no prose package authored here, consistent with the work order's explicit prohibition |
| Stale inventory documents (beyond cohorts touched above) | Documentation hygiene; does not block launch-critical architecture honesty |
| Secrets/hygiene re-audit | Operational/security, not Intelligence Core architecture |
| Controlled beta authorisation | Programme gate after architecture **and** medical-content readiness — not declared here |

## 5. Explicit non-deliverables of this sequence document

No Cursor/Automation Bus implementation prompts. No prose-generation or content-promotion package. No PSI wiring package. No architecture-completion or beta-readiness declaration. No runtime, schema, or medical-content file changes performed by ARCH-PROG-RECON-1-CC itself.
