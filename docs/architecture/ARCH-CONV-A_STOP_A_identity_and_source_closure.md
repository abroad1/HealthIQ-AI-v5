# ARCH-CONV-A — STOP A Identity and Source Closure Report

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Author role:** Cursor (`healthiq-core-engine`) — implementation / evidence only  
**Authority:** Automation Bus SOP v1.3.1 § STOP A; prompt §12 / §25 / §26  
**Runtime change:** NONE for WHY emit. Phase 0 governance inventory corrections only.

This report does **not** self-certify correctness. It requests GPT architectural review and Anthony ratification.

---

## WORK PACKAGE

| Field | Value |
|---|---|
| work_id | ARCH-CONV-A |
| branch | feature/arch-conv-a-estate-why-authority-migration |
| baseline main commit | `942de1ffda260bdcab8ab00ded17f4602dba478a` |
| start commit (post bus handoff) | `c5ab903f6c05bb0bc61b0e9472e2587c1ca11e4d` |
| current commit | `6ff17724fc4a7de8c1cca2d7ff2be249a5a218b8` |
| Automation Bus status | IN_PROGRESS (kernel); STOP A internal gate — **finish not called** |
| authority token | `automation_bus/state/work_package_active.json` → `ARCH-CONV-A` / STARTED |
| working-tree note | Only kernel-owned `automation_bus/latest_cursor_status.json` remains dirty (IN_PROGRESS) — expected at internal STOP; finish not authorised |

---

## PHASE 0

| Field | Finding |
|---|---|
| active target count | **41** (re-verified) |
| migrated target count | **5** |
| Package A target count | **36** |
| registry and loader reconciliation | Match Stage 0; sole shared legacy file = `hcy_hypotheses_v1.yaml` |
| current WHY authorities | compiled register (pilot); legacy loaders (non-pilot); provenance register (non-emit) |
| runtime entry points | Single funnel: HTTP analysis/regenerate → orchestrator → insight graph → report compiler → `compile_root_cause_v1` |
| scheduled/background WHY paths | **None** |
| estate-index corrections | Refreshed compiled WHY list 1→9; cards remain 10; source-of-truth note added |
| LLM allow-flag finding | Narrative-only; does not gate WHY emit |
| baseline discrepancies | Pre-existing ARCH-RT-5 test expected 7 cards vs live 10 — corrected with refresh; ferritin_low A4→A3 reclass |

Evidence artefact: `docs/architecture/ARCH-CONV-A_phase0_estate_reconciliation.md`

---

## PHASE 1

| Field | Finding |
|---|---|
| final target count | **41** active registry / **36** Package A |
| complete target-to-frame count | **41/41** rows declared (incl. 0-frame blocked and CONTINGENT) |
| final frame count (Package A non-contingent) | **20** |
| final frame count if D-2 distinct | **21** (provisional) |
| frame plurality findings | Pilot plurality unchanged (3/3/2). Bilirubin survivor provisional **3** Pass3 frames. No other Package A inv_spec plurality found. |
| canonical-source dispositions | See Phase 1 map §3–4 |
| source-readiness counts | DUAL_SERVED 1; CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE 18; LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT 16; Package A COMPILED 0 |
| D-1 | Process-closed (frame counts declared); schema gap accepted |
| D-2 disposition | **Options only — awaiting Anthony/GPT:** DISTINCT / FOLD_SUPPRESS / COEXIST_SELECTOR |
| D-3 disposition | **Proposed MERGE_TO_ONE** → survivor `signal_hyperbilirubinemia`; retire `signal_bilirubin_high` |
| D-4 | 1 confirmed (ferritin_low); 7 rejected → blocked |
| D-5–D-8 | As Phase 1 map §6 |
| D-9 | Closed in Phase 0 register refresh |
| wave allocation | Waves 0–6 retained; Wave 4 target count becomes 6 effective identities after D-3 merge |
| Package B hand-offs | DUAL-01/L-02 selector; shared hcy file retirement; L-04 fallback |
| Package C lineage requirements | Recorded for Phase 3 emit (no schema invention) |

Evidence artefact: `docs/architecture/ARCH-CONV-A_phase1_target_to_frame_map.md`

---

## STOP A

| Field | Value |
|---|---|
| identity closure complete | **YES** (map complete; D-2 medical choice + D-3 merge require human ratification before Phase 2) |
| canonical-source closure complete | **YES for disposition** (every frame/target has a source disposition; 16+ targets lack accepted replacement research) |
| targets blocked from medical review | 18 listed in Phase 1 §5 |
| unresolved evidence gaps | All LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT rows; Pass3→inv promotion for bilirubin survivor; elevation_context research if DISTINCT |
| architecture blockers | None that prevent STOP A review. D-2/D-3 require ratification decisions. |
| medical-research requirements | Commission specs for blocked A5/A4-reject targets; optional elevation_context spec if DISTINCT chosen |
| tests run | `test_arch_rt5_launch_gate.py::test_estate_index_loads`; `test_arch_rt5d_package_provenance.py::test_estate_index_covers_launch_artefacts`; `tests/governance/test_arch_completion_2_output_authority.py` |
| files changed | See commit |
| commits | Phase 0/1 / STOP A bounded commits on sprint branch |
| working-tree status | Reported at commit time |

---

## VERDICT

```text
READY FOR STOP A REVIEW
```

**Next authorised action:** GPT architectural review + Anthony ratification of:

1. Complete target-to-frame map  
2. D-2 elevation-context disposition choice  
3. D-3 bilirubin MERGE_TO_ONE (survivor confirmation)  
4. Wave allocation (including Wave 4 count after merge)  
5. Explicit authorisation to continue to Phase 2 for the 17 spec-ready targets only  

**Not authorised until continuation instruction:** medical review execution, compilation, runtime activation, legacy disconnection, Automation Bus `finish`.
