# HealthIQ AI — Architecture Programme Reconciliation

| Field | Value |
|---|---|
| **Work package** | ARCH-PROG-RECON-1 |
| **Status** | RECONCILIATION COMPLETE — read-only; no architecture-completion declaration |
| **Audit date** | 2026-07-25 |
| **Baseline SHA** | `363a644624e54dfdc0ac7012f8133fd5d278b593` |
| **Branch** | `feature/arch-prog-recon-1-historical-architecture-reconciliation` |
| **Nature** | Historical programme reconstruction against current repository reality |

---

## 1. Executive verdict

The original “world-class / launch-condition” architecture target required a single research→compile→runtime pipeline with no parallel medical authorities, activation-frame identity, compiled card and WHY artefacts, honest provenance, Layer B ownership of medical truth, and frontend/Gemini presentation-only behaviour.

**Wave 1 day-one architecture** was later accepted with conditions and non-blocking carry-forwards: compiled Health Systems Card evidence is live; hard-coded card lists are inactive; registry activation-key identity is live; PSI is intentionally unwired; Gemini is deny-default; six Wave 1 domains are wired.

**That acceptance is not whole-estate completion and is not controlled-beta authorisation.** Current repository evidence still shows: dual WHY authority (1 compiled + 40 legacy YAML), zero explicit `source_spec_id` on package manifests, remaining `signal_id`-family collapse on some consumers, batch-JSON provenance blocked cohorts still loaded by the registry, and medical-content depth (prose / medically reviewed assets) incomplete.

No beta-readiness or architecture-completion declaration is made by this package.

---

## 2. Source-document inventory

### 2.1 Primary evidence folders

| Folder | Top-level files | Subdirectories | Notes |
|---|---:|---|---|
| `docs/audit-papers/` | **184** | `assets/`, `launch-core-proving/`, `verification-2026-05-04/` | Complete inventory performed; recursive proving/verification trees inventoried as supporting evidence, not as separate programme authorities |
| `docs/planning-papers/` | **19** | none | Complete inventory performed |

Full alphabetical audit-paper list is recorded in `docs/audit-papers/ARCH-PROG-RECON-1_implementation_and_verification_report.md` § Source inventory.

### 2.2 Authoritative continuity / architecture documents read

| Document | Authority class (per `docs/AUTHORITY_MAP.md` / baseline) |
|---|---|
| `docs/AUTHORITY_MAP.md` | AUTHORITATIVE index |
| `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` | AUTHORITATIVE maturity baseline |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` | AUTHORITATIVE day-one carry-forward plan |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` | SUPERSEDED earlier FINAL variant |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | SUPPORTING continuity log only |
| `docs/architecture/ADR-RT-001` … `ADR-RT-004` | ACCEPTED day-one ADRs |
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | AUTHORITATIVE Layer A/B/C vocabulary |
| `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | AUTHORITATIVE strategy baseline; aspirational claims superseded where baseline conflicts |

### 2.3 Authoritative vs historical classification

| Class | Examples |
|---|---|
| **AUTHORITATIVE (current)** | Current-state baseline 2026-07-25; AUTHORITY_MAP; ADR-RT-001–004; ADR-LAYER-BOUNDARY; day-one plan `_FINAL_updated`; Automation Bus / Knowledge Bus SOP v1.3.1 |
| **EVIDENCE (not ongoing authority)** | Four 2026-07-25 independent audits under `docs/audit-papers/`; ARCH-GOV-BASELINE exception record |
| **PROGRAMME HISTORICAL (binding at the time)** | Launch-grade target/gap/ledger (May 2026); Day-One Closure Review; ARCH-COMPLETION-2/3; Transition Plan v3; Pre-Sprint packs; Scaffold plans |
| **SUPERSEDED / HISTORICAL drafts** | Transition Plan v1/v2; DOMAIN-UX non-FINAL; `SPRINT_STATUS.md`; strategy “3 domains missing”; MR-BATCH-001B “review then promote” |
| **REVIEW commentary** | Transition plan reviews; DYNAMIC-PROSE-ARCH-1; ARCH-R1 reviews |

---

## 3. Programme chronology

```text
original independent audits
→ consolidated architecture findings
→ Day-One Architecture plan
→ Day-One work packages
→ Beta Readiness audits and plan
→ Beta Readiness work packages
→ later architecture corrections
→ current repository state
```

| Phase | When | What happened |
|---|---|---|
| Market / launch-core planning | early–mid May 2026 | Market paper; Launch-Core Transformation Plan; Pre-Sprint 1–3 packs define bounded product proof |
| Forensic / launch-grade audits | ~2026-05-04 | LC-S12A forensic; LAUNCH_GRADE target/gap/ledger; TRANSFORMATION programme brief |
| Core scaffold | ~2026-05-20 | LC-S12B–23B scaffold-first programme (not launch) |
| Health Systems Card UX plans | post Wave 1 domain audits | DOMAIN-UX1A–1D scaffold sequence |
| Research utilisation / ARCH-R1 | late May 2026 | PASS3 utilisation investigations; ARCH-R1 architecture reviews |
| As-Is → Day-One transition | 2026-05-28 | Transition Plan v1→v2→v3 + dual reviews; ADR-RT-001–004; sprint plan ARCH-RT-0…6 |
| Day-One delivery | late May–mid Jun 2026 | WAVE1-EQUIV1; ARCH-RT-0…6; ARCH-RT-5B/5C/5D/5E splits; ARCH-COMPLETION-1…3 |
| Day-One closure language | 2026-06-12 | Closure Review `ACCEPTED_WITH_CONDITIONS`; ARCH-COMPLETION-3 “complete with non-blocking CF” |
| Batch 2 / context / Pass3 stream | Jun 2026 | BATCH2-*, CONTEXT-*, CF-AUTHORITY-*, PASS3-BATCH2-*, DHEA-* |
| Beta readiness programme | 2026-06-20 onward | Eight-block strategy; BUILD register P1–P3 streams; WAVE1 launch readiness + public fixes; BETA-READINESS-RECHECK / SPRINT-2 |
| Layer / prose / identity corrections | late Jun–Jul 2026 | LAYER-BOUNDARY; DYNAMIC-PROSE-ARCH-1; PROSE-INVENTORY; ARCH-RT-IDENTITY-PROV-1; P3-LAYERB-INTEL-1 |
| Governance baseline reset | 2026-07-25 | Four independent audits; ARCH-GOV-BASELINE-1; current-state baseline — **controlled beta not authorised** |

### Renamed / absorbed / split / superseded packages

| Original | Disposition |
|---|---|
| Transition Plan WP0–WP9 | Absorbed into ARCH-RT-0…6 (+ later ARCH-COMPLETION / Batch2 streams) |
| ARCH-RT-5 monolithic regeneration | Split into M1–M4 then 5B/5C/5D/5E |
| DOMAIN-UX1A + UX1B separate | Merged in FINAL DOMAIN-UX plan |
| “3 missing launch domains” strategy claim | Superseded: six Wave 1 domains wired |
| MR-BATCH-001B promote-after-review | Superseded: Round 1 benchmark / test-only |
| PSI “must wire for launch” | Superseded by ARCH-RT-5E `deferred_non_launch_blocker` |
| Estate-wide card/hypothesis regen as Wave 1 blocker | Reclassified: Wave 1 pilot + classification; whole-estate deferred |
| `docs/SPRINT_STATUS.md` as LIVE SoT | Superseded by BUILD register + current-state baseline |

---

## 4. Original target architecture (what “world-class / launch-condition” required)

Synthesised from `LAUNCH_GRADE_ANALYTICAL_TARGET_STATE_2026-05.md`, Transition Plan v3, ADR-RT-001–004, and the day-one sprint plan — **not invented here**.

| Pillar | Requirement |
|---|---|
| Canonical research | `investigation_spec` v3 is sole research authority for new compile work |
| Compile pipeline | Spec → governed compile (manifest) → immutable artefacts → thin loaders → DTOs → FE render-only |
| Identity | Multi-frame coexistence; `activation_key` = `signal_id::source_spec_id`; fail closed on collisions |
| Card evidence | Compiled from governed assets; no hard-coded subsystem authority |
| WHY | Compiled hypothesis artefacts; hand YAML temporary then retired |
| Provenance | Explicit lineage / `source_spec_id`; no silent inferred-as-explicit |
| PSI | Either consumed where launch-critical **or** explicitly classified out |
| Layer boundaries | Layer B owns medical truth; Layer C / Gemini presentation-only; no FE medical inference |
| Analytical floor | Coherence, non-silent WHY on lead findings, surface honesty (launch-grade May papers) |

**Two “day-one” meanings coexist historically and must not be collapsed:**

1. **Launch-core day-one** — prove bounded personalised pipeline (May launch-core plan).
2. **Architecture day-one** — research→compile→runtime authority correction (late-May transition / ARCH-RT).

---

## 5. Finding-to-remediation traceability matrix

Status values (exactly one per row): `CLOSED` | `PARTIALLY_CLOSED` | `DEFERRED_WITH_AUTHORITY` | `SUPERSEDED` | `OPEN` | `UNVERIFIABLE`.

### A. Canonical research authority

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| A1 | Packages/YAML/cards are parallel authorities vs research | ADR-RT-001; ARCH-RT-0…5 | ADR ACCEPTED; Wave 1 classified | Specs exist (68 files / 31 `inv_*.yaml`); packages still runtime-loaded; dual WHY remains | PARTIALLY_CLOSED |
| A2 | Raw Pass 3 / specs must not be read at runtime | Validators + launch estate gate | ARCH-RT-6 / ARCH-COMPLETION-3 PASS | Guardrails still present; Jul audits confirm no raw research on default path | CLOSED |
| A3 | Activation compile path missing | ARCH-RT-1 contracts + ARCH-RT-5 regen | DRAFT foundation + pilot manifests | No estate-wide activation compiler; pilots only | DEFERRED_WITH_AUTHORITY |
| A4 | Batch JSON packages lack extractable frame IDs | Extract specs or block | ARCH-RT-5D blocked class | 147 RT5D batch-blocked; 72 `pkg_kb52c_*`; still loaded by registry | OPEN |

### B. Signal and activation estate

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| B1 | `signal_id`-only registry silently discards frames | ADR-RT-002; ARCH-RT-2 | Multi-frame registry by `activation_key` | Live: 197 activation keys / 139 signal_ids / 51 multi-frame families; duplicate keys fail closed | CLOSED |
| B2 | Downstream consumers still collapse frames | ARCH-RT-IDENTITY-PROV-1 + follow-ons | 5 surfaces fixed; 4 deferred | Jul audits still flag remaining family/first-match collapse on launch path consumers | PARTIALLY_CLOSED |
| B3 | Collision / lexicographic overwrite | Fail closed on duplicate `activation_key` | ARCH-RT-2 | Confirmed at registry load | CLOSED |
| B4 | Context-dependent activation without gates | Fail-closed context model | BATCH2-CONTEXT / BETA-READINESS-SPRINT-2 | Context gates active; androgen sign-off still conditional | PARTIALLY_CLOSED |
| B5 | Parallel package generations | Inventory + retirement candidates | ARCH-RT-0 / KB-MAP | 11 generation cohorts / 191 packages still present | PARTIALLY_CLOSED |

### C. WHY / root-cause architecture

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| C1 | Hand-authored YAML duplicate WHY authority | ADR-RT-003; ARCH-RT-4/5C | Vitamin D compiled promotion | 1 compiled hypothesis; 40 legacy YAML; 41 registry targets; dual path live | OPEN |
| C2 | Mixed estate intended temporary | Shadow → promote → retire | Immediate YAML deletion rejected for day-one | Temporary acceptance still operative; retirement not done | DEFERRED_WITH_AUTHORITY |
| C3 | Root-cause multi-frame unaware | Policy + compiler work | Deferred / temporary gap | Still signal-family oriented in places | OPEN |
| C4 | Untraceable WHY on clinician path | ARCH-COMPLETION-2 quarantine | Claimed remediated | Filter/quarantine artefacts present | CLOSED |
| C5 | Batch 2 signals lack RC mapping | Future mapping sprint | CF non-blocking | Still listed as carry-forward | OPEN |

### D. Health Systems Card evidence

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| D1 | Hard-coded card evidence in Python | ARCH-RT-3 then estate 5B | Wave 1 compiled cards | Estate index: **10** cards; hard-coded lists empty; code comment “no hard-coded fallback” | CLOSED |
| D2 | `total_bilirubin` false-missing | WAVE1-EQUIV1 | Delivered | Guarded equivalence | CLOSED |
| D3 | Whole-estate card compilation | ARCH-RT-5B then beyond Wave 1 | Wave 1 only | Wave 1 complete; whole estate not claimed | DEFERRED_WITH_AUTHORITY |
| D4 | Legacy Layer C / insight card paths | ARCH-COMPLETION-2 quarantine | Quarantined | Manifest classifications | CLOSED |

### E. Provenance and auditability

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| E1 | 0/186 manifests with explicit `source_spec_id` | ADR-RT-004; ARCH-RT-5D; IDENTITY-PROV | Honest status model + blocked launch-critical | **0/191** manifests with `source_spec_id` field; identities inferred | OPEN |
| E2 | Inferred lineage treated as good enough for beta claims | Explicit vs inferred enum + gate | IDENTITY-PROV inventory | Launch-critical kb47 cohort: 16 BLOCKED + 1 COMPILED_MANIFEST | PARTIALLY_CLOSED |
| E3 | Replay / result versioning | LAUNCH-CORE-3 | Policy locked | Partial runtime wiring; full depth UNVERIFIABLE in Jul executable audits | PARTIALLY_CLOSED |
| E4 | Output authority provenance | ARCH-COMPLETION-2 | Implemented | Present on governed path | CLOSED |
| E5 | Full day-one traceability + estate gate | ARCH-COMPLETION-3 | Gate PASS with CF | Gate artefacts exist; CF still open | PARTIALLY_CLOSED |

### F. Layer boundaries

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| F1 | FE medical inference | Render-only DTO path | WAVE1 / Closure | Sampled routes render-only; ClusterInsightPanel non-live | CLOSED |
| F2 | Gemini analytical authority risk | Deny-default narrative policy | Narrative runtime policy | `HEALTHIQ_NARRATIVE_LLM` double opt-in; deny-default verified Jul 2026 | CLOSED |
| F3 | Layer A/B/C vocabulary drift | LAYER-BOUNDARY-RECONCILIATION-1 ADR | Merged | AUTHORITY_MAP points to ADR | CLOSED |
| F4 | Orchestrator context bridge before activation | ARCH-ORCH-RESTRUCTURE-1 | Condition C-2 | Required before context-dependent activation | PARTIALLY_CLOSED |

### G. PSI and parallel intelligence assets

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| G1 | PSI built but runtime-dead | Wire or classify out | ARCH-RT-5E deferred non-launch-blocker | Loader exists; 57 PSI artefacts; **not** on launch analysis path; validator forbids launch imports | DEFERRED_WITH_AUTHORITY |
| G2 | Duplicate medical truth via PSI vs packages | Keep streams separate | ADR-RT-003 | Policy locked; PSI unwired so not duplicate runtime truth today | CLOSED |

### H. Beta-readiness architecture obligations

| ID | Original finding | Planned remediation | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| H1 | Six launch-core domains missing (Jun strategy) | P1 domain build stream | Six domains wired | Supersedes strategy claim | SUPERSEDED |
| H2 | Architecture gates must pass | Day-one / launch estate validators | PASS claims | Jul audits re-verified architecture gate PASS | CLOSED |
| H3 | Controlled beta authorisation | Eight-block programme | Multiple readiness papers | Current baseline: **not authorised** | OPEN |
| H4 | Secrets / env hygiene | WAVE1-PUBLIC-LAUNCH-FIXES / RECHECK | Conflicting history then SPRINT-2 clean | Jul audits: UNKNOWN_REQUIRES_REVIEW | UNVERIFIABLE |
| H5 | Public-launch CB-1…CB-4 | WAVE1-PUBLIC-LAUNCH-FIXES-1 | Closed in RECHECK | Treated closed | CLOSED |
| H6 | Infrastructure vs medical-content readiness | Strategy eight blocks | Infra advanced; content partial | Infra materially advanced; medical content still open | PARTIALLY_CLOSED |

### I. Prose / explanatory-text architecture (inventory only — no new pipeline design)

| ID | Prior conclusion | Planned remediation (historical) | Claimed delivery | Current verification | Status |
|---|---|---|---|---|---|
| I1 | Embedded signal explanations / retail explainers incomplete | P2/P3 prose depth | Retail expanded (historically 40/~79) | Substrate partial; depth open | OPEN |
| I2 | Narrative fallbacks / mock honesty | Launch-grade W3 | Mock deny-default / honesty | Policy held; product honesty depth separate | PARTIALLY_CLOSED |
| I3 | Candidate prose (MR-BATCH-001B) | Medical review then promote | Earlier claims | Superseded to benchmark/test-only; not promotable | SUPERSEDED |
| I4 | DYNAMIC-PROSE-ARCH-1: extend existing composition, don’t invent engine | P3/P4 gated | Recommendation only | No new engine authorised | DEFERRED_WITH_AUTHORITY |
| I5 | Clinician prose / style governance | Style guide + quarantine | Partial | Partial enforcement historically | PARTIALLY_CLOSED |

---

## 6. Contradictory claims (do not resolve by preferring the louder summary)

| Claim A | Claim B | Resolution from current evidence |
|---|---|---|
| ARCH-COMPLETION-3: day-one architecture complete with non-blocking CF | Jul 2026 baseline: controlled beta not authorised; provenance/WHY/multi-frame open | Both can be true **if** scopes differ: Wave 1 architecture gate ≠ whole-estate target ≠ beta authorisation |
| ARCH-RT-6 / Closure: accepted for Wave 1 launch | May Gap Map: verification/coherence/surface honesty still launch-blocking | Different checklists; Gap Map items were **not** closed by ARCH-RT acceptance language |
| BUILD register / strategy: progress language | AUTHORITY_MAP: BUILD register is SUPPORTING only | Register is continuity log, not proof |
| WAVE1-LAUNCH-READINESS: secrets safe | BETA-READINESS-RECHECK: committed secrets found | Later SPRINT-2 claimed clean; Jul audits did not re-prove → UNVERIFIABLE |
| Inventory docs: 186 packages / 7 cards / 67 kb52c | Live: 191 / 10 / 72 | Live tree wins; several ARCH-RT inventory docs are STALE |
| `signal_id_collision_inventory.md`: lex overwrite | Live registry: activation_key multi-frame | Inventory doc stale |
| Strategy: 3 domains missing | Baseline: 6 domains wired | Strategy claim SUPERSEDED |
| MR-BATCH promote path | Baseline: test-only / non-promotable | SUPERSEDED |

**Completion claims that exceeded implementation evidence (material):**

1. Treating ARCH-COMPLETION-3 / Closure “accepted” language as **whole-estate** or **beta** completion.
2. Treating inferred package lineage as equivalent to explicit `source_spec_id` for launch-critical provenance claims.
3. Treating dual WHY (1 compiled + 40 YAML) as retired or “compiled authority complete”.
4. Treating registry multi-frame identity as end-to-end multi-frame preservation.
5. Treating BUILD-register domain delivery as medical-content readiness.

---

## 7. Completion assessment by architecture domain

| Domain | Wave 1 / launch-critical cohort | Whole estate | Notes |
|---|---|---|---|
| A Canonical research | Partial — no raw reads; specs canonical for *new* compile | Open — batch/legacy packages remain | |
| B Signal/activation | Registry identity closed; consumer collapse partial | Generations still mixed | |
| C WHY | Pilot only (`vitamin_d`) | Open dual authority | Mixed estate accepted as temporary, not retired |
| D Card evidence | **Closed** (10 compiled; hard-coded inactive) | Deferred beyond Wave 1 | |
| E Provenance | Honest classification partial; explicit lineage open | Open | |
| F Layer boundaries | Closed for sampled path + Gemini deny-default | Residual FE barrel / context-activation conditions | |
| G PSI | Deferred with authority | Unwired | |
| H Beta readiness | Infra advanced | Controlled beta open / not authorised | |
| I Prose | Inventory + partial substrate | Medical depth open; no pipeline designed here | |

---

## 8. Verified quantitative outputs

| Metric | Value | Evidence basis |
|---|---:|---|
| Audit papers reviewed (top-level files inventoried) | **184** | `docs/audit-papers/` |
| Planning papers reviewed | **19** | `docs/planning-papers/` |
| Material findings in matrix (§5) | **40** | Domains A–I rows (A4+B5+C5+D4+E5+F4+G2+H6+I5) |
| Findings CLOSED | **14** | A2,B1,B3,C4,D1,D2,D4,E4,F1,F2,F3,G2,H2,H5 |
| Findings PARTIALLY_CLOSED | **11** | A1,B2,B4,B5,E2,E3,E5,F4,H6,I2,I5 |
| Findings DEFERRED_WITH_AUTHORITY | **5** | A3,C2,D3,G1,I4 |
| Findings SUPERSEDED | **2** | H1,I3 |
| Findings OPEN | **7** | A4,C1,C3,C5,E1,H3,I1 |
| Findings UNVERIFIABLE | **1** | H4 secrets hygiene |
| Status sum check | **40** | 14+11+5+2+7+1 |
| Active signal families (unique `signal_id` loaded) | **139** | SignalRegistry load (excl. example) |
| Activation frames (`activation_key` count) | **197** | SignalRegistry load |
| Multi-frame families | **51** | SignalRegistry load |
| Active package directories (`pkg_*`) | **191** | `knowledge_bus/packages/` |
| Package generation cohorts | **11** | Prefix inventory |
| Estate-indexed compiled cards | **10** | `estate_index_v1.yaml` |
| Compiled hypotheses | **1** | `signal_vitamin_d_low` |
| Legacy root-cause YAML | **40** | `knowledge_bus/root_cause/hypotheses/` |
| Root-cause registry targets | **41** | `root_cause_registry_v1.py` |
| Packages with explicit manifest `source_spec_id` | **0** | Manifest scan |
| Packages with inferred / absent explicit provenance | **191** | Same scan (all inferred or blocked class) |
| `pkg_kb52c_*` blocked class | **72** | Disk + RT5D class |
| Launch-critical kb47 IDENTITY rows BLOCKED | **16** | ARCH-RT-IDENTITY-PROV-1 inventory |
| Investigation-spec files (recursive) | **68** | `knowledge_bus/research/investigation_specs/` |
| PSI artefacts / launch-path importers | **57 / 0** | PSI files; orchestrator/analysis grep |

Where a single “active vs dormant vs blocked” triad was requested: **UNVERIFIABLE as one number** — policy inventories disagree and `SignalRegistry` still loads non-example libraries regardless of review-queue flags.

---

## 9. Mixed legacy / current authorities map

| Authority | Role today | Classification |
|---|---|---|
| `investigation_spec` v3 corpus | Canonical for *new* compile | Current |
| Package `signal_library.yaml` generations | Runtime activation inputs | Mixed legacy/current (loaded) |
| Compiled card evidence (10) | Wave 1 card authority | Current |
| Hard-coded card lists | Inactive / empty | Retired for Wave 1 |
| Compiled hypothesis (`vitamin_d`) | WHY for one signal | Current pilot |
| Legacy root-cause YAML (40) | WHY for remaining targets | Legacy active |
| PSI YAML (57) | Built parallel semantics | Built-not-wired |
| Batch-JSON lineage packages | Activation still loadable; provenance blocked for beta claims | Legacy / blocked-for-claim |
| Gemini narrative | Optional presentation | Deny-default non-authority |
| MR-BATCH-001B candidates | Test/benchmark only | Non-production |

---

## 10. Related open-obligation and closure artefacts

- Unresolved obligations only: `docs/architecture/HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS.md`
- Minimum closure sequence: `docs/architecture/HEALTHIQ_AI_ARCHITECTURE_CLOSURE_SEQUENCE.md`
- Verification report: `docs/audit-papers/ARCH-PROG-RECON-1_implementation_and_verification_report.md`

---

## 11. Explicit non-claims

This reconciliation does **not**:

- declare day-one architecture complete;
- declare controlled beta ready;
- author a prose-generation or content-promotion package;
- invent new architecture requirements without a documented prior source;
- change runtime, schemas, medical assets, or tests.
