# HealthIQ AI — Eight-Block Beta Readiness Comparison and Programme Recommendation

**Date:** 2026-06-18  
**Work package:** EIGHT-BLOCK-PROGRAMME-1  
**Mode:** Documentation-only programme recommendation  
**Governing layer model:** `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`

---

## 1. Executive summary

HealthIQ AI has **substantial deterministic medical intelligence** (Layer B), a large Knowledge Bus, Wave 1 health-system cards, governance gates, and a broad test harness. The estate is **not externally beta-ready** and should continue under **controlled internal product validation** until explicit CEO approval for any external cohort.

**Current maturity (programme view):** **MEDIUM** for internal deterministic analysis on Wave 1 panels; **LOW–MEDIUM** for controlled external beta.

**Strongest assets:** Day-one architecture closure; `User Health to Systems Map_FINAL.md` as systems taxonomy authority; Wave 1 domain assembler + compiled subsystem evidence; triple Layer B DTO surface (`clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1`); `NarrativePayloadV1` handoff; **186–187** KB packages and **153** Pass 3 specs; AB/VR/golden panels; Sentinel guards; `ReplayManifestV1` and result versioning (LAUNCH-CORE-3); recent **layer-boundary ADR** and **UAT R2** trust hardening.

**Biggest risks:** Only **3 of 6** launch-core consumer domains on the results page; subsystem depth deliberately collapsed (MED-REV-1); **Gemini narrative inactive**; retail explainer registry covers **~17 of ~79** biomarkers; Pass 3 hypothesis richness not fully promoted to runtime cards; **no consolidated beta-readiness gate artefact**; security hygiene blockers noted in prior beta rechecks.

**What has now been clarified:** Strategic Vision v1.5 §2.3 + **ADR-LAYER-BOUNDARY-RECONCILIATION-1** lock Layer B as medical intelligence/WHY/surfacing authority and Layer C as presentation/translation only; late-document addendum incorporated v1.5 without overturning estate verdict; **INTERNAL-UAT-RESULTS-TRUST-HARDENING-1** resolved six HIGH UAT defects (R2: HIGH **6 → 0**).

**Why the estate must not be rebuilt from memory:** Domain taxonomy, Wave 1 assembler patterns, KB packages, Pass 3 corpus, Layer B compilers, IDL, replay/versioning policy, and audit series already exist. Reinventing systems, subsystems, or B→C contracts would discard governed assets and repeat closed decisions.

**Beta-ready?** **No** for external users. **Partial yes** for continued internal validation on known panels with documented reservations.

**Next programme must achieve:** Complete launch-core domain/subsystem coverage from existing materials; expand Layer B boilerplate/prose substrate; harden safety/provenance/auditability; only then activate constrained Layer C/Gemini; redesign UX on stable architecture; prove behaviour across phenotype/panel matrix — without assigning Layer B work to Layer C, Gemini, or frontend.

---

## 2. Evidence base

| Document | Path | Authority | Why it matters | Blocks |
|----------|------|-----------|----------------|--------|
| Cursor eight-block audit | `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md` | Discovery audit | Independent block maturity; 186 packages; reuse priorities | All 8 |
| Claude eight-block audit | `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md` | Discovery audit | Companion assessment; 187 packages; sprint sketch S-A* series | All 8 |
| Late-document addendum | `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` | Programme evidence | v1.5 strengthens Layer B/C framing; no full re-audit needed | 3–5 |
| Layer authority index r2 | `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Discovery index | Ranked authority stack for layer boundaries | 3–4 |
| Layer-boundary ADR | `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | **AUTHORITATIVE** | Governing A/B/C vocabulary for all future sprints | 3–5 |
| Strategic Vision v1.5 | `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | **AUTHORITATIVE** | §2.3 strategic north star | All |
| User Health to Systems Map | `docs/architecture/User Health to Systems Map_FINAL.md` | **AUTHORITATIVE** | 8-domain consumer taxonomy | 1–2 |
| ADR_WP2 | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | **AUTHORITATIVE** | `NarrativePayloadV1` handoff | 3–4 |
| NarrativePayloadV1 | `backend/core/contracts/narrative_payload_v1.py` | Runtime contract | LLM prohibitions; brief structure | 3–4 |
| LAUNCH-CORE-3 | `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` | Policy | Replay/versioning | 7 |
| UAT R1 | `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` | Test evidence | Pre-trust-hardening baseline | 5 |
| UAT R2 | `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-17_r2.md` | Test evidence | Post-trust-hardening; HIGH cleared | 5 |
| Trust hardening closure | `docs/audit-papers/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence.md` | Audit | Six HIGH fixes merged | 5 |
| Layer reconciliation closure | `docs/audit-papers/LAYER-BOUNDARY-RECONCILIATION-1_layer_boundary_reconciliation.md` | Audit | ADR acceptance record | 3–4 |
| Results Journey v6 | `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | Supporting | UX journey target | 5 |
| DOMAIN_NARRATIVE_CONTRACT_WAVE1 | `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Contract | Wave 1 domain copy rules | 1, 3 |
| PRIMARY_CONCERN policy | `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Intelligence policy | Layer B ranking | 3 |
| RETAIL_EXPLAINER boundaries | `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Supporting | Explainer render rules | 3, 6 |
| Day-one launch estate gate | `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` | Governance | Render-only conditions | 6–8 |
| AUTHORITY_MAP | `docs/AUTHORITY_MAP.md` | Registry | Document status | Meta |

---

## 3. Corrected canonical layer model

From **ADR-LAYER-BOUNDARY-RECONCILIATION-1** (summarised):

| Layer | Owns |
|-------|------|
| **A** | Ingestion, parsing, canonicalisation, factual normalisation — **not** medical meaning |
| **B** | All deterministic medical intelligence: signals, WHY/root-cause, hierarchy, surfacing/suppression, clinician report, IDL, boilerplate/prose **selection**, safety, provenance |
| **C** | Presentation and translation of governed Layer B output only |

**Explicit locks for programme planning:**

- **Layer B owns WHY/root-cause**, surfacing and suppression, **clinician report**, deterministic **boilerplate/prose asset selection**, evidence/counter-evidence, and traceability.
- **Layer C is presentation/translation only** — deterministic compilers and frontend scrubbers assemble or polish; they do not decide medical meaning.
- **Gemini is optional and constrained**, not the analytical engine — inactive for narrative today; activation only after Layer B brief/prose/test substrate and CEO approval.
- **Frontend remains render-only** — consumes DTO; no medical inference.

The product “wow” should come primarily from **governed Layer B boilerplate modules** (biomarker, system, pathway, lifestyle, missing-marker, counter-evidence, clinician sections) that Layer C presents — not from Gemini improvising long reports.

---

## 4. Cursor vs Claude comparison

| Block | Cursor assessment | Claude assessment | Agreement | Disagreement | Programme interpretation | Confidence | Late docs impact |
|-------|-------------------|-------------------|-----------|--------------|--------------------------|------------|------------------|
| **1 — Core health systems** | MEDIUM; 3/6 domains on cards | MEDIUM; same 3/6 gap | **Strong** | None material | Implement remaining launch domains from `User Health to Systems Map` — do not rebuild taxonomy | HIGH | v1.5 reinforces phenotype-aware ambition; no count change |
| **2 — Subsystems** | MEDIUM; 7 compiled, 2 visible scored; MED-REV-1 collapse | MEDIUM; missing blood/iron, thyroid, kidney assembly | **Strong** | Cursor emphasises pilot subsystem count; Claude names specific KB packages | Map then wire subsystems for new domains using `wave1_subsystem_evidence.py` pattern | HIGH | FE proposal tensions with MED-REV-1 — document in UX phase |
| **3 — Layer B / WHY / clinician / prose** | MEDIUM–HIGH; compilers + IDL strong; boilerplate incomplete | HIGH; triple artifact in production | **Strong** | Cursor slightly lower on prose coverage | Priority: prose/boilerplate matrix before Gemini | HIGH | v1.5 §2.3 + ADR strengthen Layer B ownership |
| **4 — Layer C / Gemini** | LOW–MEDIUM runtime; contract MEDIUM–HIGH | LOW runtime / MEDIUM contract | **Strong** | Both note naming drift (compiler labelled Layer C) | ADR reconciles; no Gemini until substrate ready | HIGH | ADR now settled naming drift |
| **5 — Results / UX** | MEDIUM; UAT reservations | MEDIUM–HIGH; **6 HIGH open** (pre-R2) | **Strong** (post-R2) | Claude rated UX higher pre-fix | R2 supersedes Claude HIGH count; MEDIUM backlog remains | HIGH | Trust hardening merged; R2 confirms |
| **6 — Safety / provenance** | MEDIUM–HIGH | MEDIUM | **Strong** | Cursor slightly higher | Pass 3 promotion pipeline + explainer coverage are P1 | HIGH | Unchanged |
| **7 — Auditability / replay** | MEDIUM | MEDIUM | **Strong** | None | Extend replay manifest fields; do not redesign LAUNCH-CORE-3 | HIGH | Unchanged |
| **8 — Phenotype / beta gates** | MEDIUM | MEDIUM | **Strong** | None | Consolidate beta gate checklist; expand panel matrix | HIGH | Unchanged |

---

## 5. Reconciled eight-block maturity assessment

| Block | Maturity | Confidence | Existing assets | Implementation | Documentation | Main gaps | Beta relevance | Layer B | Layer C / UX | Reuse |
|-------|----------|------------|-----------------|----------------|---------------|-----------|----------------|---------|--------------|-------|
| **1 — Core health systems** | MEDIUM | HIGH | User Health Map; scoring_policy; domain assembler | 3/6 Wave 1 domains | Strong | Blood/iron, thyroid, kidney cards | Critical | High | Low | **HIGH** |
| **2 — Subsystems & depth** | MEDIUM | HIGH | wave1_subsystem_evidence; compiled YAML | 7 subsystems; 2 scored visible | Partial | Hidden subsystems; no assembly for 3 domains | High | High | Medium | **HIGH** |
| **3 — Layer B intelligence & prose** | MEDIUM–HIGH | HIGH | report_compiler; narrative compiler; IDL; root cause | Production DTOs | Strong ADRs | Explainer/boilerplate coverage; Pass 3 compile-through | Critical | **Primary** | Output only | **HIGH** |
| **4 — Layer C / Gemini** | LOW (runtime) | HIGH | NarrativePayloadV1; validator_v2; LC-S3 assembly | Gemini inactive | ADR_WP2 + ADR reconciliation | No production Gemini narrative path | High (later) | Brief source | **Primary** | **HIGH** |
| **5 — Results page / UX** | MEDIUM | HIGH | Full journey; 18+ components; UAT R2 | Renders all DTOs | Journey v6; UAT registers | MEDIUM copy; marker display names; length/IA | High | Consumes B | **Primary** | MEDIUM |
| **6 — Safety / provenance** | MEDIUM–HIGH | MEDIUM | 186+ packages; promotion protocol; prose safety | Lab ranges enforced | Strong | 17/79 explainers; automated Pass 3 compile | Critical | High | Scrub only | **HIGH** |
| **7 — Auditability / replay** | MEDIUM | HIGH | ReplayManifestV1; result_versioning | Stale banner works | LAUNCH-CORE-3 | raw_input_hash; lineage table deferred | High | Meta/provenance | Display | MEDIUM |
| **8 — Phenotype / beta gates** | MEDIUM | HIGH | AB/VR; phenotype fixtures; Sentinel | Reachability tests | Operating model | No single beta checklist | Critical | Test harness | UAT | **HIGH** |

---

## 6. Key conclusions that are now settled

1. **`User Health to Systems Map_FINAL.md`** is the systems taxonomy authority — do not author a new domain model from scratch.
2. **Strategic Vision v1.5 §2.3** is the strategic north star for layer responsibilities.
3. **`ADR-LAYER-BOUNDARY-RECONCILIATION-1`** governs future layer vocabulary and sprint scoping.
4. **Layer B** is the medical intelligence, WHY, hierarchy, surfacing, clinician report, and boilerplate-selection layer.
5. **Layer C** is presentation/translation only; frontend is render-only.
6. **Gemini is inactive** for narrative and must not be activated before Layer B brief/prose/test substrate is ready and CEO approves.
7. **Not externally beta-ready** — language: continued internal validation / future controlled beta readiness.
8. **No full estate re-audit required** — compare, reconcile, programme (this paper).
9. **Implementation must start from existing assets** — KB packages, Wave 1 patterns, compilers, contracts, test panels.

---

## 7. Stale or superseded findings

| Finding | Source | Correction |
|---------|--------|------------|
| **6 HIGH UAT defects unresolved** | Claude audit (2026-06-17) | **Stale.** R2 UAT (2026-06-17) + `INTERNAL-UAT-RESULTS-TRUST-HARDENING-1` merged: HIGH **6 → 0**. Residual: IUAT-006 interpretation line partial (MEDIUM). |
| **Package count 186 vs 187** | Cursor vs Claude | **Immaterial drift** — filesystem recount timing; programme uses **~187 KB packages**; both audits agree order-of-magnitude. |
| **UAT date / commit** | R1 used 2026-06-16 | R2 uses 2026-06-17 on `main` post-merge; trust hardening closure at `af6d17d` family. |
| **Reconciling ADR pending** | Late addendum §1 step 3 | **Superseded** — `ADR-LAYER-BOUNDARY-RECONCILIATION-1` merged 2026-06-18. |
| **Layer index r1 ranking** | r1 index | **Superseded for ranking** by r2; r1 retained as historical. |
| **Results page “PASS WITH RESERVATIONS”** | R1 UAT | **Superseded** by R2 **PASS** for internal validation (not external launch). |

**Check before implementation:** Security/secrets gate status from `BETA-READINESS-RECHECK-1`; MED-REV-1 subsystem visibility vs FE “show systems” policy; persisted API `body_overview` raw text vs UI scrub-only (IUAT-004 note in R2).

---

## 8. Reusable asset inventory

### Systems and subsystems

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| User Health to Systems Map | `docs/architecture/User Health to Systems Map_FINAL.md` | 8-domain taxonomy + medical review | Domain expansion sprints | Authoritative |
| Scoring policy | `backend/ssot/scoring_policy.yaml` | 8 engine systems + biomarker rails | Domain assembler | Runtime SSOT |
| Domain assembler | `backend/core/analytics/domain_score_assembler.py` | Wave 1 three-domain pattern | LAUNCH-CORE-DOMAINS-* | Runtime |
| Wave 1 subsystem evidence | `backend/core/analytics/wave1_subsystem_evidence.py` | Subsystem ID registry | Subsystem wiring | Runtime |
| Compiled health system cards | `knowledge_bus/compiled/health_system_cards/` | Card evidence YAML | Domain cards | Compiled |
| Thyroid / iron KB packages | `pkg_thyroid_tsh_context`, `pkg_iron_deficiency_context`, etc. | Raw material for missing domains | Domain map sprint | Research/runtime |

### Layer B / WHY / clinician report / prose

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| ClinicianReportV1 | `backend/core/analytics/report_compiler_v1.py` | CSR assembly | Layer B hardening | Runtime |
| NarrativePayloadV1 | `backend/core/contracts/narrative_payload_v1.py` | B→C brief | Gemini activation (late) | Contract |
| Root cause compiler | `backend/core/analytics/root_cause_compiler_v1.py` | WHY hypotheses | Layer B expansion | Runtime |
| IDL bundle | `interpretation_display_layer_v1` on DTO | Pattern cards authority | UX (render) | Runtime |
| Retail explainer registry | `backend/ssot/retail_explainer_v1/registry.yaml` | Biomarker explainers | Prose substrate sprint | SSOT |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/` | Pathway copy | N-5 expansion | Governed content |
| Domain narrative contract | `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 copy rules | Domain sprints | Contract |
| Primary concern policy | `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Ranking philosophy | Layer B only | Intelligence policy |

### Layer C / presentation

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| Layer boundary ADR | `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Vocabulary lock | All sprints | Authoritative |
| Narrative compiler | `backend/core/analytics/narrative_report_compiler_v1.py` | Deterministic Layer C output | Presentation phase | Runtime |
| LC-S3 assembly | `narrative_compiler_lc_s3_assembly_v1.py` | Payload-driven prose | Layer C | Runtime |
| Gemini validator | `backend/core/llm/validator_v2.py` | Anti-hallucination | Gemini sprint | Runtime |
| Results page | `frontend/app/(app)/results/page.tsx` | Journey shell | UX phase | Frontend |

### Safety / provenance

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| Promotion protocol | `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Research→runtime rules | KB util sprints | Governance |
| Traceability matrix | `docs/architecture/research_to_runtime_traceability_matrix.md` | Provenance map | Safety hardening | Supporting |
| Output authority provenance | `output_authority_provenance_builder_v1.py` | Report provenance | Layer B | Runtime |
| Consumer prose safety | `backend/core/analytics/consumer_prose_safety_v1.py` | Wording guards | Layer B | Runtime |
| Lab range tests | `backend/tests/enforcement/` | Range authority | Ongoing | Test |

### Auditability

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| ReplayManifestV1 | `backend/core/contracts/replay_manifest_v1.py` | Component hashes | Replay hardening | Contract |
| Result versioning | `result_versioning_policy_v1.py` + LAUNCH-CORE-3 | Stale/incompatible | Completed; extend | Policy/runtime |
| Golden runner | `backend/tests/golden/` | Deterministic replay | Beta validation | Test |

### Testing / beta validation

| Asset | Path | Gives us | Future sprint | Class |
|-------|------|----------|---------------|-------|
| AB/VR panels | `backend/tests/fixtures/` | Acceptance profiles | Beta validation | Test |
| Phenotype fixtures | phenotype suite | Edge cases | Phase 6 | Test |
| Sentinel packs | `sentinel/packs/` | Defect class guards | Ongoing | Test |
| UAT R1/R2 | `docs/testing/INTERNAL_UAT_*` | Results page evidence | UX polish backlog | Test evidence |
| Trust hardening tests | `test_internal_uat_results_trust_hardening.py` | Regression | Maintain | Test |

---

## 9. Programme principles

1. **No Gemini before Layer B brief/prose/test substrate is ready** — `NarrativePayloadV1`, boilerplate matrix, anti-hallucination tests, CEO approval.
2. **No UX polish before core architecture and hierarchy are stable** — domains, subsystems, Layer B prose gaps first.
3. **No new systems taxonomy from scratch** — extend `User Health to Systems Map` and existing registers.
4. **No frontend medical inference** — render-only; ADR-007 and launch estate gate.
5. **No fallback parser logic** — lab ranges authoritative; no global defaults where lab ranges exist.
6. **Preserve research provenance** — Pass 3 promotion protocol; no raw Pass 3 runtime reads.
7. **Beta framing internal until CEO explicitly approves** external cohort language.
8. **Every implementation sprint traces to existing authority** — cite ADR, map, contract, or register.
9. **Prefer outcome-based sprint packages** — avoid unnecessary micro-sprints; bundle only when dependencies align.
10. **Use Automation Bus `change_type: CONTENT`** for documentation-only work (not `DOCS`).

---

## 10. Recommended multi-sprint programme

Approx. **16 sprints** in **7 phases** (titles are programme recommendations — not yet authored as bus prompts).

### Phase 0 — Immediate governance and evidence consolidation (2 sprints)

| Sprint | Objective | Blocks | Layer | Risk | Stop gate |
|--------|-----------|--------|-------|------|-----------|
| **P0-1 — Programme lock & carry-forward sync** | Publish this paper; sync carry-forward register with eight-block gaps | All | — | LOW | CEO acknowledges programme |
| **P0-2 — Beta gate checklist draft** | Single consolidated internal beta-readiness checklist artefact | 8 | — | LOW | Checklist reviewed |

### Phase 1 — Systems and subsystem completion (4 sprints)

| Sprint | Objective | Blocks | Layer | Risk | Dependencies |
|--------|-----------|--------|-------|------|--------------|
| **P1-1 — Launch-core domain build-materials map** | Map KB packages/signals/SSOT for blood/iron, thyroid, kidney | 1, 2 | B (plan) | LOW | User Health Map |
| **P1-2 — Blood/iron Wave 1 domain card** | Implement `wave1_blood_iron` consumer domain using existing packages | 1, 2 | B | STANDARD | P1-1 |
| **P1-3 — Thyroid Wave 1 domain card** | Implement thyroid domain + subsystem wiring | 1, 2 | B | STANDARD | P1-1; thyroid gates |
| **P1-4 — Kidney Wave 1 domain card** | Implement kidney/renal domain card | 1, 2 | B | STANDARD | P1-1; egfr authority |

### Phase 2 — Layer B substrate expansion (4 sprints)

| Sprint | Objective | Blocks | Layer | Risk | Dependencies |
|--------|-----------|--------|-------|------|--------------|
| **P2-1 — Boilerplate/prose coverage matrix** | biomarker × trigger × source asset matrix from existing KB/IDL | 3 | B | LOW | PASS3 utilisation audit |
| **P2-2 — Retail explainer expansion wave 1** | Expand registry toward panel coverage (target ≥40 key markers) | 3, 6 | B (CONTENT) | STANDARD | P2-1 |
| **P2-3 — Pathway & missing-marker explainer pack** | N-5/N-7 entries for new domains + homocysteine/B12 cautions | 3 | B | STANDARD | P1-2–4 |
| **P2-4 — NarrativePayload brief hardening** | Confirm v1.1 section intents sufficient for future Gemini | 3, 4 | B | HIGH | ADR_WP2 |

### Phase 3 — Safety, provenance and auditability (2 sprints)

| Sprint | Objective | Blocks | Layer | Risk |
|--------|-----------|--------|-------|------|
| **P3-1 — Pass 3 promotion pilot expansion** | Governed compile for 1–2 high-value Pass 3 frames | 6 | B/KB | HIGH |
| **P3-2 — Replay manifest & lineage extension** | Compiler/package hashes; document lineage deferrals | 7 | B/meta | MEDIUM |

### Phase 4 — Layer C presentation and constrained Gemini (2 sprints)

| Sprint | Objective | Blocks | Layer | Risk | Stop gate |
|--------|-----------|--------|-------|------|-----------|
| **P4-1 — Gemini activation design + test harness** | Prompt template consuming `NarrativePayloadV1`; validator tests | 4 | C | HIGH | P2-4 complete; no production enable |
| **P4-2 — Controlled Gemini narrative pilot** | Internal-only synthesis path behind feature flag | 4 | C | HIGH | CEO approval; P4-1 tests green |

### Phase 5 — Results page / UX redesign (2 sprints)

| Sprint | Objective | Blocks | Layer | Risk |
|--------|-----------|--------|-------|------|
| **P5-1 — MEDIUM UAT / retail polish backlog** | Marker names, transferrin copy, body_overview producer scrub | 5 | C (render) + B (producer where needed) | MEDIUM |
| **P5-2 — Progressive disclosure & journey IA** | Journey v6 alignment; subsystem visibility policy vs MED-REV-1 | 5 | C | MEDIUM |

### Phase 6 — Beta validation and test estate (2 sprints)

| Sprint | Objective | Blocks | Layer | Risk |
|--------|-----------|--------|-------|------|
| **P6-1 — Phenotype/panel validation matrix** | Run AB/VR + phenotype grid; record gaps | 8 | Test | MEDIUM |
| **P6-2 — Internal beta gate execution** | Execute P0-2 checklist; security/secrets re-check | 8 | — | HIGH |

---

## 11. Recommended first three sprints

### Sprint 1 — P1-1: Launch-core domain build-materials map

| Field | Detail |
|-------|--------|
| **Why first** | Biggest structural gap (3/6 domains) but KB material likely exists — mapping prevents duplicate taxonomy work |
| **Produces** | Authoritative map: domain → scoring rail → subsystem IDs → package IDs → gaps |
| **Must not do** | Implement domain cards; change scoring; touch Layer C/Gemini |
| **Type** | **CONTENT** (+ light read-only discovery) |
| **Review** | GPT architectural review; Claude audit optional |

### Sprint 2 — P2-1: Boilerplate/prose coverage matrix

| Field | Detail |
|-------|--------|
| **Why second** | Parallel-safe with domain planning; unlocks Layer B substrate before Gemini or heavy UX |
| **Produces** | Coverage matrix + prioritized gap list for explainers/pathway/clinician modules |
| **Must not do** | Gemini activation; frontend inference; new medical claims in Layer C |
| **Type** | **CONTENT** |
| **Review** | GPT review recommended |

### Sprint 3 — P1-2: Blood/iron Wave 1 domain card

| Field | Detail |
|-------|--------|
| **Why third** | First missing launch-core domain with confirmed KB packages (`pkg_iron_deficiency_context`, etc.) |
| **Produces** | `consumer_domain_scores` row + subsystem evidence for blood/iron |
| **Must not do** | Rebuild taxonomy; Layer C copy invention; skip P1-1 map alignment |
| **Type** | **BEHAVIOUR** (Layer B only) |
| **Review** | Full HIGH route: Cursor build → Claude audit → GPT review → human approval |

---

## 12. Beta-readiness decision gates

| Gate | Criterion | Owner |
|------|-----------|-------|
| **Domain coverage** | 6/6 launch-core domains on results page with subsystem minimum depth | Programme + medical review |
| **Layer B evidence/prose** | Boilerplate matrix ≥ agreed coverage; clinician report + IDL stable | Layer B sprint lead |
| **Layer C / Gemini** | NarrativePayload sufficient; validator tests; feature-flagged pilot; CEO approval | Architecture + CEO |
| **Medical safety / provenance** | Lab ranges authoritative; promotion protocol followed; no raw Pass 3 reads | Governance |
| **Auditability / replay** | Replay manifest complete for governed outputs; versioning policy met | LAUNCH-CORE-3 |
| **UX trust** | UAT HIGH = 0; MEDIUM backlog triaged; no stale/incompatible false positives | QA/UAT |
| **Phenotype / edge-case** | AB/VR + phenotype matrix executed with documented gaps | Test estate |
| **Security / secrets** | No committed secrets; beta recheck blockers cleared | Security |
| **CEO / human** | Explicit approval for controlled external beta cohort | CEO |

---

## 13. Risks and dependencies

**Major risks:** Over-activating Gemini before Layer B substrate; UX polish masking missing domains; reinventing taxonomy; frontend medical inference; bulk Pass 3 promotion without frame gates; security hygiene blockers.

**Sequencing dependencies:** P1-1 before P1-2–4; P2-1 before explainer expansion; P2-4 before P4-*; domain cards before domain-specific pathway explainers; trust hardening complete before external UX claims.

**Over-fragmentation hurts:** Splitting each missing domain into separate micro-sprints without shared assembler patterns; one-marker explainer sprints.

**Unsafe bundling:** Gemini + UX redesign + domain implementation in one sprint; Layer C copy changes that alter hierarchy.

**Documentation must precede code:** Domain build-materials map; boilerplate matrix; beta gate checklist.

**Clinical/medical review needed:** Androgen/thyroid activation adjacency; iron/thyroid domain copy; any new surfacing rules.

---

## 14. Final recommendation

**Proceed with the programme** as sequenced above. Do **not** treat the product as externally beta-ready. Do **not** rebuild the estate from memory. Do **not** activate Gemini or assign Layer B work to Layer C/frontend.

**First work package to author:** **P1-1 — Launch-core domain build-materials map** (`change_type: CONTENT`).

**CEO decision required:** Approve programme phasing; confirm internal-only validation posture; approve future Gemini activation gate criteria; authorize first implementation sprint (P1-2) after map completes.

**Must not do next:** External beta launch; Gemini narrative activation; full estate re-audit; new systems taxonomy; Layer C medical reasoning; ignoring ADR-LAYER-BOUNDARY-RECONCILIATION-1.

---

*End of programme recommendation — EIGHT-BLOCK-PROGRAMME-1 — 2026-06-18.*
