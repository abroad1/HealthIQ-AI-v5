# HealthIQ AI — Open Architecture Obligations (Claude Code Independent Verification)

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1-CC |
| **Companion** | `HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION_CC.md` |
| **Rule** | Contains only genuinely unresolved obligations, independently verified against live code. Closed work is not repeated here. |
| **Date** | 2026-07-25 |

Status values: `OPEN` | `PARTIALLY_CLOSED` | `DEFERRED_WITH_AUTHORITY` | `UNVERIFIABLE`.

---

## OBL-CC-001 — Launch-path frame-identity collapse (5 verified surfaces, not 4)

| Field | Content |
|---|---|
| **original requirement** | Multi-frame research fidelity must survive from registry through every analytics consumer on the analysis→DTO path (ADR-RT-002; day-one sprint plan). |
| **source documents** | ADR-RT-002; ARCH-RT-IDENTITY-PROV-1/C1 implementation + correction reports |
| **delivered remediation** | ARCH-RT-2 (registry); ARCH-RT-IDENTITY-PROV-1/C1 (5 named downstream consumers) |
| **current evidence** | 4 of the 5 named consumers are genuinely `activation_key`-keyed in their core logic. The 5th, `signal_interaction_builder.py`, surfaces `activation_key` only as an output field (`participating_activation_keys`) — its node-identity (`node_ids`, lines 63-66/145) and confidence-lookup (`confidence_by_signal`, lines 220-224) dicts remain keyed on bare `signal_id`, meaning two frames sharing a `signal_id` still collapse to one interaction-graph node. Additionally, 4 further consumers remain deliberately un-migrated (disclosed carry-forward): `interpretation_display_layer_publish_v1.py` (:75-89, :111-122), `domain_score_assembler.py` (no `activation_key` anywhere in file), `narrative_report_compiler_v1.py` (:757, `activation_key` explicitly blanked), `intervention_selector_v1.py` (:149, :203). |
| **status** | OPEN — 5 verified surfaces, one more than the 4 disclosed by ARCH-RT-IDENTITY-PROV-1/C1's own carry-forward note |
| **confidence** | HIGH (direct file:line code read) |
| **risk** | Distinct medical frames silently merge into one interaction node / phenotype signal / narrative lead / intervention basis whenever a multi-frame family reaches these paths. Not yet confirmed whether any *currently firing* Wave 1 signal has >1 concurrently active frame reaching all five — this sub-question was not resolved by this audit or by Cursor's; scoping PKG-1-equivalent work should confirm it first rather than assume worst case. |
| **launch relevance** | Launch-relevant if any multi-frame family is live on the Wave 1 path; mechanism is defective regardless and will affect the next multi-frame family added even if none currently triggers it |
| **recommended disposition** | Fold the interaction-builder gap into the same closure package as the other 4 deferred surfaces — do not treat it as separately "already closed" |

---

## OBL-CC-002 — Explicit provenance lineage (estate-wide)

| Field | Content |
|---|---|
| **original requirement** | Activated outputs must carry honest, explicit research lineage (`source_spec_id`); inferred lineage must not be presented as explicit (ADR-RT-004). |
| **source documents** | ADR-RT-004; ARCH-RT-5D unresolved register; ARCH-RT-IDENTITY-PROV-1 inventory |
| **delivered remediation** | Honest classification enum (`provenance_status_v1.py`) + launch-critical gate; no estate-wide backfill attempted or claimed |
| **current evidence** | 0/191 manifests carry `source_spec_id` on disk — confirmed by direct scan. This is the correct, expected state given the delivered package's actual (narrower) scope; it is not evidence the provenance programme "must be repeated," per the work order's own caution. |
| **status** | OPEN |
| **confidence** | HIGH |
| **risk** | Any claim of estate-wide explicit traceability would be false; no such claim currently exists in authoritative documents |
| **launch relevance** | Launch-critical only for the specific cohort claiming explicit lineage (currently just the 1 compiled-hypothesis pilot row) |
| **recommended disposition** | Extract/attach specs only for packages that must remain claimable; otherwise enforce consistent non-claim status (folds into OBL-CC-003) |

---

## OBL-CC-003 — Runtime reachability of provenance-`BLOCKED` packages (independently discovered, sharper than prior documentation)

| Field | Content |
|---|---|
| **original requirement** | Q2 of the work order explicitly separates "runtime reachability of blocked assets" as its own sub-question — this had not been code-verified by any prior document as of this audit's start. |
| **source documents** | `signal_evaluator.py`; `report_compiler_v1.py`; `ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md` |
| **delivered remediation** | None claimed — no document asserted this was fixed |
| **current evidence** | `SignalRegistry._iter_signal_library_paths()` (`signal_evaluator.py:33-36`) globs every `*/signal_library.yaml` under `knowledge_bus/packages/` with **no** provenance-status filter. All 20 `pkg_kb47_*` package directories (the launch-critical `BLOCKED`/`beta_eligible_explicit: False` cohort) carry a live `signal_library.yaml` and are therefore fully loaded, scored, and rankable in `ReportTopFindingV1` output. `provenance_status` is threaded through `SignalResult` (`signal_evaluator.py:528`) and into the report (`report_compiler_v1.py:817`) as a **disclosed field only** — grepped both call sites; no conditional suppression exists at either. |
| **status** | OPEN — and materially more concrete than "provenance is undocumented": these signals can appear in a live user-facing result today with only a metadata label distinguishing them from explicit-lineage findings |
| **confidence** | HIGH (direct code read, both load-side and consume-side) |
| **risk** | A user-visible finding may rest on a signal whose research lineage is explicitly not eligible for a beta claim, with no runtime control preventing it from firing or ranking highly |
| **launch relevance** | Launch-critical — this is exactly the cohort the launch-critical provenance inventory tracks, and its own `unresolved_action` column ("Extract... before beta claim") implies this reachability gap is not yet accepted as a permanent posture |
| **recommended disposition** | Either (a) extract/attach explicit specs for this cohort, or (b) add an explicit non-reachability gate consistent with the `BLOCKED` classification — do not leave classification-only with full reachability as the shipped state into controlled beta |

---

## OBL-CC-004 — Dual WHY authority, estate-wide retirement

| Field | Content |
|---|---|
| **original requirement** | Compiled hypothesis artefacts become WHY authority; hand YAML is temporary (ADR-RT-003). |
| **source documents** | ADR-RT-003; `root_cause_compiler_v1.py`; `compiled_hypothesis.py`; `root_cause_registry_v1.py` |
| **delivered remediation** | 1 pilot compiled + promoted (`signal_vitamin_d_low`); mutual-exclusivity gating per signal_id confirmed in code |
| **current evidence** | 1 compiled / 40 legacy YAML / 41 registry targets, confirmed by direct file count. No signal is served by both paths simultaneously (`root_cause_compiler_v1.py:539` branch is exclusive). Row-level frame collapse is fixed; hypothesis *content* for the 39 legacy signals remains family-level regardless of which frame fired. |
| **status** | OPEN for estate retirement. The dual-authority *posture itself* is `DEFERRED_WITH_AUTHORITY` — ADR-RT-003 Decision 6 explicitly rejects immediate YAML deletion for day-one; this is an authorised transition, not a defect requiring urgent remediation. |
| **confidence** | HIGH |
| **risk** | Overstating "compiled WHY complete" while 40 signals remain on family-level legacy content; drift between legacy YAML and current research if not periodically reconciled |
| **launch relevance** | Launch-critical only for any claim that WHY is compiled-governed estate-wide; not launch-critical for the current, disclosed dual-authority posture |
| **recommended disposition** | For the launch-critical cohort, either promote-and-review or honestly classify remaining YAML as legacy-active — do not force whole-estate 41-target migration in one package |

---

## OBL-CC-005 — Stale architecture inventory documents

| Field | Content |
|---|---|
| **original requirement** | Governance inventories must match live estate. |
| **source documents** | `package_generation_inventory.md`; `active_intelligence_authority_manifest.md` |
| **delivered remediation** | None — not previously flagged as urgent beyond the current-state baseline's general supersession note |
| **current evidence** | `package_generation_inventory.md` (2026-05-28) states 186 packages, `pkg_kb52c_*`=67; live count is 192 directories/191 manifests, `pkg_kb52c_*`=72 — the cohort **grew**, contradicting any assumption that it is a closed, shrinking, or static class. Separately, `active_intelligence_authority_manifest.md` states 7 launch-included compiled cards + 1 hypothesis artefact as "active," while other current documents (current-state baseline, Cursor's reconciliation) state 10 compiled cards — this specific discrepancy was not resolved within this audit's time budget; see Variance report. |
| **status** | OPEN |
| **confidence** | HIGH for the 186→192/67→72 drift (direct count); MEDIUM for the 7-vs-10 card count (not independently re-derived by re-reading the estate index in full) |
| **risk** | Planning or future audits citing stale counts as current; card-count discrepancy specifically could mislead a future closure package's acceptance criteria |
| **launch relevance** | Governance integrity, not directly clinical |
| **recommended disposition** | Refresh `package_generation_inventory.md` against live tree; resolve the 7-vs-10 card-count discrepancy by re-reading `estate_index_v1.yaml` directly before citing either number as current in a future work package |

---

## OBL-CC-006 — Controlled beta authorisation (programme gate, unchanged)

| Field | Content |
|---|---|
| **original requirement** | Controlled beta requires infrastructure and medical-content readiness against the eight-block strategy. |
| **source documents** | `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` §10/§12 |
| **current evidence** | Explicitly "not authorised" as of the baseline; nothing in this audit's evidence changes that |
| **status** | OPEN |
| **confidence** | HIGH |
| **risk** | Premature exposure if bypassed |
| **launch relevance** | Programme gate binding all obligations above |
| **recommended disposition** | No action from this package; remains a downstream gate after OBL-CC-001–004 close for the launch-critical cohort |

---

## Explicitly excluded (closed — not re-opened)

- `SignalRegistry` `activation_key` keying + fail-closed duplicates (registry level) — CLOSED, confirmed by direct code read.
- Provenance honesty/classification enum and launch-critical gate — CLOSED as a disclosure control (does not resolve OBL-CC-002/003).
- Compiled-vs-legacy WHY mutual exclusivity per signal — CLOSED (no double-serving signal found).
- Wave 1 compiled card evidence active / hard-coded evidence inactive — treated as CLOSED per prior audits; card *count* (7 vs 10) is a documentation-accuracy question (OBL-CC-005), not a re-opening of whether hard-coded evidence is inactive.
- PSI unwired with day-one import guard — DEFERRED_WITH_AUTHORITY, not an open safety defect.
