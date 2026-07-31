# ARCH-CONV-E — Lifecycle exception and closure

**Work ID:** `ARCH-CONV-E`  
**Branch:** `feature/arch-conv-e-alt-why-authority`  
**Date (UTC):** 2026-07-31  
**Claude Code audit:** `automation_bus/latest_audit_summary.md`  
**Audit result:** `gate_status: FAIL` / `failure_type: ARCHITECTURAL`  
**Lifecycle exception:** `RATIFIED` (retrospective governance ratification of the audited scope excursion)  
**Authority:** Anthony — named human project authority/ratifier, following Head of Architecture review and recommendation.

## Purpose

Close the audited lifecycle exception for ARCH-CONV-E. Claude Code independently
verified that the Knowledge Bus package build and the runtime activation-boundary
implementation are technically sound, but failed the package on governance grounds
because the hardened asset-build scope explicitly prohibited executable
analytics/runtime changes. This record ratifies that excursion retrospectively. It
does not invent missing pre-execution approval, and it does not create precedent for
silently expanding a hardened scope.

---

## 1. Original hardened authority

The hardened ARCH-CONV-E asset-build prompt
(`automation_bus/latest_cursor_prompt.md`,
`automation_bus/latest_prompt_hardening.json`, overall verdict `HARDENED`) authorised
Knowledge Bus package creation and regeneration from the canonical Pass 3 research
source. It prohibited modification of executable analytics, runtime, SSOT, or frontend
code. It also required that none of the six packages be promoted or activated.

Hardened authority therefore covered package assets, lineage, validation, and evidence.
It did not cover design or implementation of a production runtime activation boundary.

---

## 2. Triggering defect

Valid package placement under `knowledge_bus/packages/` caused immediate production
reachability because:

1. non-launch-critical packages were classified `ELIGIBILITY_OUT_OF_COHORT`;
2. `is_production_reachable()` incorrectly treated that classification as reachable;
3. `SignalRegistry` therefore loaded every on-disk `signal_library.yaml`, including the
   six ARCH-CONV-E packages.

Consequently, faithful package creation could not satisfy the simultaneous hardened
requirement that the six packages remain unactivated. The defect was pre-existing; the
asset build exposed it.

---

## 3. Required STOP that was missed

Implementation should have stopped and returned for renewed governance approval before
designing or implementing the runtime activation boundary.

That STOP was required by the hardened prohibition on executable analytics/runtime
change and by the Automation Bus rule that a hardened requirement which cannot be met
without touching prohibited files must re-enter hardening, not be resolved by unilateral
scope expansion. The STOP was missed. The runtime boundary was designed and shipped
inside the same work package without a separate hardening pass or pre-execution approval
record. This process failure is not minimised by the later technical correctness of the
fix.

---

## 4. Scope excursion

Out-of-hardened-scope files introduced or modified under `a260c53`:

| Path | Role |
|---|---|
| `backend/core/analytics/signal_evaluator.py` | Production `SignalRegistry` loader / activation gate |
| `backend/core/knowledge/package_runtime_eligibility_v1.py` | Eligibility classifier; `OUT_OF_COHORT` removed from production-reachable set |
| `backend/core/knowledge/package_activation_register_v1.py` | New fail-closed activation-register loader |
| `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` | New governed activation register (173 activated frames; six ARCH-CONV-E frames withheld) |
| Directly associated runtime-boundary tests and reconciliations | Including `backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py`, updates to `test_signal_evaluator.py` / `test_arch_conv_pkg2_provenance_reachability.py`, and package-count reconciliations required by the three new package directories |

In-hardened-scope package assets, Pass 1/2/3 provenance files, estate inventory rows for
the six packages, and the asset-build evidence report remain separately accepted as
within the original CONTENT / package-build authority.

---

## 5. Technical disposition

Retrospective review accepts the implementation rather than requiring reversion because:

- it fixes a genuine pre-existing accidental-activation defect;
- package placement no longer implies activation;
- `ELIGIBILITY_OUT_OF_COHORT` is fail-closed for production loading;
- production-reachable and test-only opt-in semantics remain preserved;
- all six ARCH-CONV-E packages remain valid and unactivated;
- the complete runtime delta is limited to removal of the three accidentally loaded ALT
  Batch 5 frames;
- no non-ALT runtime delta was found;
- reverting would restore known incorrect behaviour.

No further code change is required to close this exception.

---

## 6. ALT lineage disposition

The three former clean-HEAD Batch 5 ALT activation keys were:

- `signal_alt_high::inv_alt_high_hepatocellular_injury_pattern`
- `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern`
- `signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern`

Disposition for each:

> Superseded by canonical regeneration and removed from accidental runtime reachability; replacement frames remain unactivated pending explicit promotion.

This record does not claim that an independent medical-retirement process was completed.
No retirement register entry or medical-retirement evidence was produced under
ARCH-CONV-E. `pkg_s24_alt_high_hepatocellular_injury` remains loaded.

---

## 7. Evidence

| Artefact | Reference |
|---|---|
| Implementation commit | `a260c53` — `feat(knowledge-bus): ARCH-CONV-E ALT assets with activation boundary` |
| Disposition wording commit | `ca2f0f2` — `docs(arch-conv-e): record former Batch 5 ALT key disposition` |
| Kernel COMPLETE status commit | `843f60c` — `chore(bus): ARCH-CONV-E kernel COMPLETE status` |
| Asset-build / boundary evidence report | `docs/sprints/beta_readiness/ARCH-CONV-E_alt_package_asset_build_report.md` |
| Claude Code audit | `automation_bus/latest_audit_summary.md` (`gate_status: FAIL`, `failure_type: ARCHITECTURAL`) |
| Kernel gate evidence | `automation_bus/latest_gate_evidence.json` (`overall.status: PASS`, `exit_code: 0`) |
| Kernel status | `automation_bus/latest_cursor_status.json` (`work_id: ARCH-CONV-E`, `status: COMPLETE`) |
| Package validators | `validate_knowledge_package.py` PASS for all six packages (re-confirmed in Claude audit) |
| Registry before / after | Clean `HEAD` `4d09048`: 182 frames / 176 packages / 4 ALT; post-`a260c53`: 179 / 173 / 1 ALT |
| Targeted tests | Boundary module, package content-contract, inventory/estate reconciliations, launch-critical and ARCH-CONV-CORRECT-1 gates, baseline harness (`38 passed`) |
| Canonical Pass 3 source | `knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json` |
| Pass 3 SHA-256 | `7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267` |

---

## 8. Retrospective authority decision

| Decision | Record |
|---|---|
| Lifecycle exception | `RATIFIED` |
| Implementation | Accepted without reversion |
| Further code change | Not required |
| Future packages | Must STOP and re-harden when prohibited runtime or contract files become necessary |
| Precedent | This exception does **not** create precedent for silently expanding hardened scope |

The ratification closes the audited governance finding for the already-shipped runtime
boundary. It does not rewrite the hardened prompt after the fact, and it does not
reclassify the missed STOP as optional.

---

## 9. Closure status

ARCH-CONV-E remains **unmerged** until independent Claude Code re-audit confirms that
this lifecycle-exception record accurately closes the governance finding.

Merge remains human-only. This document does not itself execute merge.
