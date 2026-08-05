# HealthIQ AI — Main-System and Subsystem Completion Audit

**Mode:** B2 strategic/programmatic audit, explicitly authorised by Anthony. Repository-grounded; code inspection performed directly and via two parallel read-only sub-agents (Wave 1: Cardiovascular/Blood sugar/Liver; Wave 2: Kidney/Blood-iron-oxygen/Thyroid), each independently citing file:line evidence and running tests directly rather than trusting prior documents.
**Date:** 2026-08-05
**Supersedes for sequencing purposes:** `docs/audit-papers/POST_CLIN_PRIORITY_PROGRAMME_SEQUENCING_AUDIT.md` (that audit's findings on clinical-authority/regeneration stability remain valid and are reused below; it did not inspect the system/subsystem estate and its sequencing conclusion is corrected here).

## 1. Executive verdict

The prompt's premise — "seven main systems, four missing" — does not match documented programme intent or repository state and should not be used as-is. The programme's own documented taxonomy is **6 launch-core domains + 2 explicitly deferred "second-wave" domains = 8 intended systems**, not 7. Separately, and more consequentially: **the current-state baseline's claim that "six Wave 1 domains built and wired" is misleading as written** — backend assembly is genuinely complete for all 6, but the frontend rendering component hardcodes exactly 3, and the "3 systems" limit is baked into consumer-facing copy ("How **three** focus areas look on your panel"), not just a filter. This is a real, evidenced, currently-open gap — just a narrower and more precisely defined one than the prompt assumed.

Additionally, this audit found a **genuine, currently-failing runtime defect** in thyroid signal firing (§5), and confirmed that the "one bounded subsystem per domain" pattern the user described is **not an implementation gap** but a **named, tested, deliberate medical-review policy decision (MED-REV-1)** that deliberately hides 5 of 10 compiled subsystems from consumer view.

**Consumer presentation consolidation should not proceed as a single full-page redesign yet** — not because the clinical-authority layer is unstable (it isn't, see §7), but because a **product-scope decision** (how many main systems the page shows) is still open, and redesigning around 3 systems now risks a second redesign later if that decision expands scope to 6.

## 2. Main-system matrix

All 8 systems the repository's own documents name as intended, in the taxonomy defined by `HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` §8.1 (6 launch-core) and `P1-7_research_to_runtime_readiness_matrix.yaml` (+2 second-wave).

| Consumer name | Canonical ID | Scoring | Compiled evidence | Subsystem routing | Signal coverage | Backend assembly | DTO exposure | Frontend rendering | Regression | Consumer-visible | Blocker / carry-forward | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cardiovascular health | `wave1_cardiovascular` | Active | Yes, 3 subsystems compiled | 1 of 3 visible (MED-REV-1) | Active | `cv_block`, `domain_score_assembler.py` | Yes | Yes (`Wave1DomainCards.tsx:19-23`) | `test_med_rev1_wave1_subsystem_visibility.py` et al. | **Yes** | 2 of 3 subsystems intentionally hidden (governed, not blocked) | **PARTIAL** |
| Blood sugar control | `wave1_blood_sugar` | Active | Yes, 2 subsystems | 1 of 2 visible | Active | `met_block` | Yes | Yes | Same suite | **Yes** | 1 subsystem hidden (governed) | **PARTIAL** |
| Liver health | `wave1_liver` | Active | Yes, 2 subsystems, resolves to flat evidence | 0 of 2 visible — flat fallback only | Active | `liv_block` | Yes (`DomainFlatEvidenceV1`) | Yes | Same suite + KB-UTIL-1 flat-evidence tests | **Yes** | No scored subsystem depth reaches consumers at all, by design (`wave1_subsystem_evidence.py`: `if domain_id != "wave1_liver": return None`) | **PARTIAL** |
| Kidney function | `wave1_kidney` | Active | Yes, 1 subsystem compiled | Visible | Active (eGFR/creatinine only; no urea, no ACR/UACR) | `ren_block`, `domain_score_assembler.py:890-` | Yes | **No** — absent from `Wave1DomainCards.tsx` and from every other frontend file (repo-wide grep, zero matches) | `test_p1_2_*` (13/13 pass) | **No** | Frontend wiring only; backend is genuinely complete | **PARTIAL — backend-complete, consumer-invisible** |
| Blood / iron / oxygen | `wave1_blood_iron_oxygen` | Active | Yes, 1 subsystem | Visible | Active | `bio_block` — no primary IDL selected (`idl = None`) | Yes | **No** | Passing (fork-run) | **No** | Frontend wiring; narrative shallower than kidney (no IDL) | **PARTIAL — backend-complete, consumer-invisible, narrative-shallow** |
| Thyroid / energy regulation | `wave1_thyroid` | Active | Yes, 1 subsystem | Visible | **Partially broken** — see §5 | `thy_block` — no primary IDL selected | Yes | **No** | **1 test currently FAILS** (`test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate`) | **No** | Frontend wiring + a live firing defect | **PARTIAL — backend mostly complete, has an active defect, consumer-invisible, narrative-shallow** |
| Silent inflammation (second-wave) | *(none assigned)* | None | None | None | None | None | None | None | None | **No** | Explicitly deferred by strategic decision (`P1-7_research_to_runtime_adequacy_gate.md:81,181`); research present, uncompiled, unmapped | **NOT_STARTED** (by design) |
| Hormone balance / gonadal axis (second-wave) | *(none assigned)* | None (hormonal scoring rail exists but inert for this domain) | None | None | None | None | None | None | None | **No** | Explicitly deferred; kb47 testosterone/LH/FSH/DHEA packages exist as research only (`P1-9_pass3_research_to_runtime_exploitation_map.md:106,135`) | **NOT_STARTED** (by design) |

**Correction of the baseline claim:** `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md:66,79` states "Six Wave 1 domains built and wired," explicitly superseding the earlier strategy's "three domains missing" framing (line 126). Both statements are partially right and partially misleading: **backend assembly is genuinely complete for all 6** (confirmed directly — `domain_score_assembler.py` produces full `ConsumerDomainScoreV1` rows for all 6, consumed live in `orchestrator.py:49`), but **"wired" does not mean consumer-visible**: `frontend/app/components/results/Wave1DomainCards.tsx:19-23,66` hardcodes a 3-domain `WAVE1_ORDER` list and renders literal copy "How **three** focus areas look on your panel." The 3-system limit is a product/copy decision baked into the frontend, not a technical stub.

## 3. Subsystem matrix

Canonical subsystem taxonomy source: `backend/core/analytics/wave1_subsystem_evidence.py:20-43` (`_WAVE1_DOMAIN_SUBSYSTEM_ORDER`), cross-checked against the compiled-artefact list and the MED-REV-1 visibility partition in `backend/core/knowledge/health_system_card_evidence.py:26-53`.

| Subsystem ID | Parent | Governed evidence | Compiled artefact | Runtime firing | Allowlist | Assembly | DTO | Frontend | Fires on test data | Consumer-ready | Blocker | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `wave1_cv_lipid_transport` | Cardiovascular | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes (confirmed) | Yes | None | **COMPLETE** |
| `wave1_cv_homocysteine_pathway` | Cardiovascular | Yes | Yes | Yes | Yes | Yes | Yes (not surfaced) | No | Not re-verified this pass | No | MED-REV-1 hides it (`visibility_tier: hidden_v1`) | **DEFERRED** |
| `wave1_cv_vascular_strain` | Cardiovascular | Yes | Yes | Yes | Yes | Yes | Yes (not surfaced) | No | Not re-verified | No | MED-REV-1 hidden | **DEFERRED** |
| `wave1_met_glycaemic_control` | Blood sugar | Yes | Yes (original pilot, `PILOT_SUBSYSTEM_ID`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | None | **COMPLETE** |
| `wave1_met_insulin_metabolic` | Blood sugar | Yes | Yes | Yes | Yes | Yes | Yes (not surfaced) | No | Not re-verified | No | MED-REV-1 hidden | **DEFERRED** |
| `wave1_liv_enzyme_pattern` | Liver | Yes | Yes | Yes | Yes | Yes | Yes (not surfaced) | No | Not re-verified | No | MED-REV-1 hidden; liver has zero visible scored subsystems | **DEFERRED** |
| `wave1_liv_processing_context` | Liver | Yes | Yes | Yes | Yes | Yes | Yes (not surfaced) | No | Not re-verified | No | MED-REV-1 hidden | **DEFERRED** |
| `wave1_ren_glomerular_filtration` | Kidney | Yes | Yes | Yes | Yes | Yes | Yes | **No** (domain not on frontend allowlist) | Passing tests | No | Frontend wiring only | **PARTIAL — backend-complete, consumer-invisible** |
| `wave1_bio_oxygen_carrying_capacity` | Blood/iron/oxygen | Yes | Yes | Yes | Yes | Yes | Yes | **No** | Passing | No | Frontend wiring; no primary IDL | **PARTIAL** |
| `wave1_thy_hormonal_axis` | Thyroid | Yes | Yes | **Partially broken** | Yes | Yes | Yes | **No** | **1 test fails** | No | Frontend wiring + live firing defect (§5) | **PARTIAL — has an active defect** |

No subsystem-level rows exist for the two second-wave domains — there is no subsystem taxonomy to classify until domain mapping itself begins, consistent with their `NOT_STARTED` main-system classification.

**Do not treat any hidden or unwired subsystem as a technical gap needing a work item on its own.** The 5 MED-REV-1-hidden subsystems are a deliberate, tested, reversible product/medical decision (`docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md`; enforced at CI by `backend/scripts/validate_day_one_architecture.py:81-114,247,281`) — re-activating them requires a policy decision to change MED-REV-1, not implementation work.

## 4. Active authority map

Authorities currently affecting main-system/subsystem output, and how they relate:

- **Compiled subsystem evidence** (`knowledge_bus/compiled/estate_index_v1.yaml`, consumed via `health_system_card_evidence.py`) — the sole active subsystem evidence authority. Legacy hard-coded subsystem lists are confirmed empty/inactive (per `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md:51-52`, consistent with what both forks found).
- **MED-REV-1 visibility partition** (`health_system_card_evidence.py:41-53`) — a second, deliberate authority layered on top of compiled evidence, gating which of the 10 compiled subsystems reach the DTO. This is not a duplicate/competing authority — it is a governed downstream filter on the single compiled-evidence authority, and it is enforced by a dedicated architecture validator, so it cannot silently drift.
- **Domain score assembler** (`domain_score_assembler.py`) — the single main-system assembly authority for all 6 launch-core domains; confirmed live in the orchestrator (`orchestrator.py:49`), not a parallel/shadow path.
- **Frontend `WAVE1_ORDER`** (`Wave1DomainCards.tsx:19-23`) — a **third, independent authority** that silently drops any domain not in its hardcoded 3-item list, even though the DTO already carries all 6. This is the one clear case of a **frontend authority that has fallen out of sync with backend reality** — not a competing clinical/medical authority, but a stale product-scope decision baked into rendering code.
- **`clinical_concern_set` / concern-set presentation authority** — separately audited this session (`PASS`, see §7); unrelated to and does not depend on the Wave1 domain-card estate described above. These are two different sections of the same results page (lead-finding hero vs. system-score cards) and can be worked on independently.
- **Narrative-report, IDL, cluster/primary-driver, clinician-report authorities** — already mapped in detail by the prior UAT presentation investigation (`docs/audit-papers/UAT_RESULTS_PAGE_PRESENTATION_INVESTIGATION_1ce310e1.md`, §2-3, §12); that mapping is reused here, not repeated. It identified up to 7 competing narrative sources visible on one page for the concern-set/lead-finding surface specifically — a separate, already-documented problem from the domain-card frontend gap found in this audit.
- **Adjacent naming-split flag** (not yet resolved, out of this audit's core scope but relevant to future authority hygiene): `docs/audit-papers/ARCH-LEGACY-1_pathway_retirement_audit.md:45` records a still-open `signal_crp_high` vs `signal_systemic_inflammation` naming split relevant to any future silent-inflammation domain work.

No duplicate or competing **medical/clinical** authority was found for main-system or subsystem output — the one duplication found (frontend `WAVE1_ORDER` vs backend DTO) is a **product-scope/rendering** gap, not a clinical-governance conflict.

## 5. Genuine defect found this audit

`backend/tests/unit/test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate` **fails on current `main`/audited branches** — asserts `signal_free_t3_high` should fire when FT3=7.0 with TSH=0.2 (suppressed), but the evaluator returns zero signals. This was independently run, not inferred from documentation, and is a live runtime-firing defect in the thyroid domain — it should not be conflated with the (separate, intentional) MED-REV-1 visibility decisions above.

## 6. Missing and partial implementation estate — summary

- **Frontend wiring gap (kidney, blood/iron/oxygen, thyroid):** backend-complete, zero frontend consumption. This is the largest single gap and is purely a frontend + product-scope-decision task — no backend work is required to close it once the scope decision is made.
- **Thyroid firing defect (§5):** a genuine bug, independent of the above, fixable without any product decision.
- **Narrative shallowness (blood/iron/oxygen, thyroid):** no primary IDL selected (`idl = None`), unlike kidney. Cosmetic/depth gap, not a correctness defect.
- **MED-REV-1 hidden subsystems (5 of 10):** deliberate, tested, reversible only by a governed policy decision — not implementation debt.
- **Second-wave domains (silent inflammation, hormone balance):** genuinely `NOT_STARTED` at the domain-model level; explicitly and repeatedly deferred by strategic decision across multiple sprint documents; no evidence this was ever meant to be part of near-term scope.
- **Consumer-copy/presentation-authority gap** (from the prior UAT investigation, unrelated surface): still open, independently confirmed stable at the ranking-authority layer (§7).

## 7. Backend/authority work required before presentation consolidation

Reused from the prior sequencing audit (still valid, not re-litigated): clinical finding/prioritisation authority (CLIN-PRIORITY-CORE-1) and analysis regeneration/result-versioning authority (CLIN-PRIORITY-RESULT-REGEN-1) are both independently audited **PASS** and stable foundations. That conclusion stands.

**New from this audit:** before any *full* results-page consolidation (as opposed to the already-scoped bounded concern-set presentation fix), the following must be resolved:
1. **A product-scope decision**: does the consumer page show 3 systems (current), 6 (all launch-core, backend-ready today), or a phased rollout? This is not a technical blocker — the DTO already supports 6 — but consolidating page layout/copy now, before this decision, risks a second redesign.
2. **The thyroid firing defect (§5)** should be fixed regardless of the scope decision — it affects data correctness, not presentation.
3. **No further backend work is required** to add kidney/iron/thyroid to the consumer page if the scope decision says yes — this is a frontend `WAVE1_ORDER` change plus (optionally) closing the IDL gap for bio/thyroid for narrative parity with kidney.

## 8. Corrected programme sequence

1. **Thyroid FT3/TSH firing-defect fix** (bounded, Intelligence Core, HIGH risk by touch-surface but narrow in scope) — independent of every other item below; fix now.
2. **Product-scope decision: consumer-visible main-system count** (decision package, not an SOP) — Anthony/product authority decide whether to expand from 3 to 6 systems, and on what timeline. This gates items 3-4 below but not item 1, 5, or 6.
3. **`FE-WAVE1-SYSTEM-EXPANSION-1`** (only if item 2 authorises expansion) — wire kidney/blood-iron-oxygen/thyroid into `Wave1DomainCards.tsx`, update the "three focus areas" copy, close the IDL gap for bio/thyroid. Frontend-only; no backend change required.
4. **`FE-RESULTS-PRESENTATION-STRUCTURE-1`** (already scoped in the prior sequencing audit) — the bounded concern-set/hero presentation fix (enum/label leakage removal, conflicting-legacy-narrative suppression, deduplication). Independent of items 2-3 (different page section); may proceed in parallel with item 2's decision process.
5. **Consumer-label product/clinical decision + DTO addition + `FE-RESULTS-CONSUMER-COPY-BOUNDARY-1`** (already scoped in the prior sequencing audit, unchanged) — proceeds after item 4.
6. **Full results-page consolidation** — only after items 2-5 are resolved, so the page is designed once against a settled system count and settled consumer-copy authority.
7. **Register/documentation hygiene** (parallel, non-blocking) — see §9.

Second-wave domains (silent inflammation, hormone balance) remain correctly out of this sequence entirely.

## 9. Sprint plan and BDR — do they require updating?

**Yes, in two specific places, both documentation-only:**
- `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md:66,79` ("six Wave 1 domains built and wired") should be qualified to distinguish backend-wired from consumer-visible — as written it can mislead a reader into believing the frontend gap doesn't exist.
- `BUILD_DELIVERABLE_REGISTER.md` has no entries yet for CLIN-PRIORITY-RESULT-REGEN-1 or `fix/uat-alt-prioritisation` (flagged in the prior sequencing audit — still true, still unresolved).

The **day-one architecture rework sprint plan** (`healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`) is a **different, parallel track** (identity/provenance/WHY-authority) from the eight-block beta-readiness strategy that actually governs domain/subsystem completeness — it does not need updating for this audit's findings because it was never the authority for this question. Treating it as "the governing sprint plan" for system/subsystem completeness (as the prior sequencing audit implicitly did) was itself a scope error this audit corrects.

## 10. Recommended next governed package

**Two independent, immediately-startable packages, not one:**
- A bounded bug-fix SOP for the thyroid FT3/TSH firing defect (§5) — no product decision required, standard risk given Intelligence Core touch but narrow surface.
- The product-scope decision on consumer-visible system count (§8 item 2) — a decision/ratification package, not an implementation SOP, and the true long-pole item this audit surfaces.

The already-scoped `FE-RESULTS-PRESENTATION-STRUCTURE-1` from the prior sequencing audit remains valid and may proceed in parallel — it is not blocked by anything found in this audit.

## 11. Evidence paths (primary)

- `frontend/app/components/results/Wave1DomainCards.tsx:19-23,66` — 3-domain hardcode + consumer copy.
- `backend/core/analytics/domain_score_assembler.py:400-451,453-503,505-581,890-1071` — all 6 domain assembly blocks.
- `backend/core/pipeline/orchestrator.py:49` — live use of the assembler.
- `backend/core/analytics/wave1_subsystem_evidence.py:20-43,91-105` — canonical subsystem taxonomy; liver flat-evidence hardcode.
- `backend/core/knowledge/health_system_card_evidence.py:26-53,360-362` — compiled subsystem list and MED-REV-1 visibility partition.
- `backend/core/models/results.py:202-275,278-294` — `SubsystemEvidenceV1` / `DomainFlatEvidenceV1` DTO models.
- `docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md`; `backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py`; `backend/scripts/validate_day_one_architecture.py:81-114,247,281` — MED-REV-1 governance and enforcement.
- `backend/tests/unit/test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate` — failing test, run directly this audit.
- `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md:456-492` — original 6-domain launch-core taxonomy.
- `docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md:81-82,181`; `P1-7_research_to_runtime_readiness_matrix.yaml:177,202,224`; `P1-9_pass3_research_to_runtime_exploitation_map.md:105-106,135,164` — second-wave domain deferral.
- `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md:60-79,111-130` — superseded-claims table and the "six built and wired" statement corrected in §2 above.
- `docs/audit-papers/POST_CLIN_PRIORITY_PROGRAMME_SEQUENCING_AUDIT.md`; `docs/audit-papers/UAT_RESULTS_PAGE_PRESENTATION_INVESTIGATION_1ce310e1.md` — prior audits reused for §4 and §7, not repeated in full here.

## Provisional nature of this audit

This audit is repository-grounded as of 2026-08-05 and is a planning input, not an implementation authorisation. The two sub-agent evidence passes did not re-run every cited regression test (disclosed per-item above where a test was run directly vs. cited by name only) and did not re-verify the 5 MED-REV-1-hidden subsystems' current DTO/test state beyond confirming the visibility partition itself. If sequencing decisions are made from this document, re-check any specifically load-bearing citation against the then-current repository state first.
