# HealthIQ AI v5 — State of Truth Review
**Date:** 2026-05-04  
**Produced by:** Claude Code  
**Basis:** Full repo inspection — all findings cite observed file paths. No assumptions made.  
**Status:** Leadership reference document — not a sprint prompt.

---

## 1. Executive Summary

Leadership does **not** currently have a clear, consistent view of product truth. The judgement is **partly** — not no, not yes.

There are several excellent, honest documents in this repo that together tell the real story. The problem is that they sit alongside ~200 other files, many of which contradict them, predate them, or duplicate them. A person trying to understand the product by reading the documentation will reach the wrong state of confidence — either too confident in the engine's completeness, or confused about which version of the strategy is operative.

**The core documentation problem is threefold:**

1. **Two high-quality, honest audits** (`PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md`, `PRODUCT_REALITY_AND_DIRECTION_AUDIT.md`) and a concrete reset plan (`RESET_SPRINT_PLAN_2026-04.md`) were produced in April 2026. These are the most accurate product-state documents in the repo. They are not anchored at the top of any navigation path. A reader following `DOCUMENTATION_HIERARCHY.md` or `README_V5.2_BASELINE.md` would never find them first.

2. **The documentation hierarchy itself is stale.** `DOCUMENTATION_HIERARCHY.md` declares `ARCHITECTURE_REVIEW_REPORT.md` as "Level 1 PRIMARY SSOT" — that document is from Sprint 14, October 2025. It does not reflect the product as it exists today. Following it for sprint planning would produce bad decisions.

3. **The `docs/Download-Arch/` directory** contains ~90 working papers, draft strategy versions, feedback documents, and superseded designs — unorganised, unlabelled, and indistinguishable from authoritative documents to a reader who doesn't already know the history.

**The good news:** The components needed for a clear documentation picture exist. The reset in April 2026 already produced the right documents. What is missing is anchoring, archival, and a single entry-point that points to current truth.

---

## 2. Important Document Inventory

### 2A. Strategy

| Document | Location |
|---|---|
| Strategic Vision & Sprint Plan v1.5 FINAL ADOPTED | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` |
| First Market Addendum (to v1.5 FINAL) | `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` |
| Product Review & Strategic Reset (April 2026) | `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` |
| Reset Sprint Plan (April 2026) | `docs/RESET_SPRINT_PLAN_2026-04.md` |
| Strategy Stack Document Authority Map | `docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md` |
| Executive GTM Report v2 | `docs/strategy/HealthIQ_Executive_GTM_Report_Updated_v2.md` |
| Phase 1 Launch Posture | `docs/HealthIQ_Phase1_Launch_Posture.md` |
| Strategy Plan v1.4 amended | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` |
| Strategy Plan (no version suffix) | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` |
| Master Roadmap v5.2 → v5.3 | `docs/MASTER_ROADMAP_v5.2_to_v5.3.md` |
| Download-Arch: 9 further strategy plan revisions | `docs/Download-Arch/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan*.md` |

### 2B. Product / Launch Scope

| Document | Location |
|---|---|
| Master PRD v5.2 | `docs/Master_PRD_v5.2.md` |
| Delivery Sprint Plan v5.2 | `docs/Delivery_Sprint_Plan_v5.2.md` |
| Phase 1 Launch Posture | `docs/HealthIQ_Phase1_Launch_Posture.md` |
| Phased Customer Domain Score Sprint Plan FINAL | `docs/HealthIQ_phased_customer_domain_score_sprint_plan_FINAL.md` |
| V5.3 Depth Track | `docs/V5.3_DEPTH_TRACK.md` |
| OPEN_ITEMS_AND_PHASE1_BOUNDARIES | `docs/ops/OPEN_ITEMS_AND_PHASE1_BOUNDARIES.md` |

### 2C. Architecture

| Document | Location |
|---|---|
| Architecture Index (ADR registry) | `architecture/ARCHITECTURE_INDEX.md` |
| ADR-001: Platform Non-Negotiables | `architecture/ADR-001-platform-non-negotiables.md` |
| ADR-002: Deterministic Three-Layer Architecture | `architecture/ADR-002-deterministic-analysis-engine.md` |
| ADR-003: Knowledge Bus Architecture | `architecture/ADR-003-knowledge-bus-architecture.md` |
| ADR-005: Signal Evaluation v2 (active; ADR-004 superseded) | `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` |
| Architecture Guardrails | `architecture/ARCHITECTURE_GUARDRAILS.md` |
| HealthIQ Reasoning Pipeline | `architecture/HEALTHIQ_REASONING_PIPELINE.md` |
| Analytical Assets Inventory v5.2 | `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md` |
| Phase 0 As-Is Architecture Audit | `docs/architecture/PHASE_0_AS_IS_ARCHITECTURE_AUDIT.md` |
| Architecture Review Report (STALE — Sprint 14) | `docs/ARCHITECTURE_REVIEW_REPORT.md` |
| Architecture Insight Modularity Review | `docs/ARCHITECTURE_INSIGHT_MODULARITY_REVIEW.md` |

### 2D. Intelligence / Analysis Layer

| Document | Location |
|---|---|
| Product Reality & Direction Audit (April 2026) | `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` |
| Metabolic Pathway Coverage Audit (March 2026) | `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` |
| Intelligence Model Design Second Pass | `docs/architecture/HealthIQ_Intelligence_Model_Design_Second_Pass.md` |
| Signal Architecture Completion v1.0 | `docs/architecture/SIGNAL_ARCHITECTURE_COMPLETION_v1.0.md` |
| Domain Narrative Contract Wave 1 | `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` |
| Primary Concern & Ranked Ambiguity Policy v1 | `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` |
| Wave 1 Codebase Analysis v3 | `docs/Wave1-codebase-analysis_v3.md` |
| Investigation files (KB sprint preflights) | `docs/investigations/KB-S48_* through KB_S58_*.md` |
| Results/WHY narrative investigations (April 2026) | `docs/investigations/2026-04-12_*.md` |
| ADR-008: Promoted Signal Intelligence Contract | `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` |
| ADR-009: Root Cause WHY (KB-S46) | `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` |

### 2E. Frontend / UX

| Document | Location |
|---|---|
| Results Journey Recommendation Paper v6 | `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` |
| Interpretation Display Layer Design Lock | `docs/strategy/Interpretation_Display_Layer_Design_Lock.md` |
| IDL Naming Decision Note (Approved) | `docs/strategy/HealthIQ_IDL_Naming_Decision_Note_Approved.md` |
| Questionnaire UX Redesign Background (Q-1) | `docs/QUESTIONNAIRE_UX_REDESIGN_BACKGROUND.md` |
| Questionnaire Visual Redesign Background (Q-2) | `docs/QUESTIONNAIRE_VISUAL_REDESIGN_Q2_BACKGROUND.md` |
| Results Page UX Design Package | `docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md` |
| FE Visualisation Surface Policy Final v3 (Download-Arch) | `docs/Download-Arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` |
| Claude Translation Spec v1 | `docs/CLAUDE_TRANSLATION_SPEC_v1.md` |
| Strategy: Clinician Language Style Guide | `docs/clinician_language_style_guide_v1.md` |

### 2F. Testing / Quality

| Document | Location |
|---|---|
| Phase 1 Sentinel Implementation Report (2026-05-03) | `docs/testing/healthiq_sentinel_phase1_implementation_report.md` |
| Phase 1 Sentinel Brief | `docs/testing/brief for HealthIQ AI Phase 1 Sentinel.md` |
| Sentinel Repo Audit v1 | `docs/testing/healthiq_sentinel_repo_audit_v1.md` |
| Automated Testing & Sentinel Repo Audit Report | `docs/testing/automated-testing-sentinel-repo-audit-report.md` |
| Agentic Testing Strategy Background | `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md` |
| Background Testing Operating Model v1 | `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` |
| UAT1 Findings | `docs/testing/UAT1/UAT1_findings.md` |
| Legacy Test Infrastructure Analysis | `reports/audit/LEGACY_TEST_INFRASTRUCTURE_ANALYSIS.md` |

### 2G. Governance / Control-Plane

| Document | Location |
|---|---|
| CLAUDE.md (permanent project context) | `.claude/CLAUDE.md` |
| Automation Bus SOP v1.3.1 (ACTIVE) | `docs/AUTOMATION_BUS_SOP_v1.3.1.md` |
| Automation Bus SOP v1.3 (superseded) | `docs/AUTOMATION_BUS_SOP_v1.3.md` |
| Automation Bus SOP v1.2 (superseded) | `docs/AUTOMATION_BUS_SOP_v1.2.md` |
| Knowledge Bus SOP v1.3 (ACTIVE) | `docs/KNOWLEDGE_BUS_SOP_v1.3.md` |
| Knowledge Bus SOP v1.2 (superseded) | `docs/KNOWLEDGE_BUS_SOP_v1.2.md` |
| Cursor Operating Policy | `docs/agents/CURSOR_OPERATING_POLICY.md` |
| Download-Arch: SOP v1.1 + multiple v1.3.1 draft variants | `docs/Download-Arch/AUTOMATION_BUS_SOP_*.md` |

### 2H. Investigations / Audits (operational outputs)

| Document | Location |
|---|---|
| Backend intelligence model audit | `backend/artifacts/intelligence_model_audit.md` |
| Investigation spec audit | `backend/artifacts/investigation_spec_audit.md` |
| Package manifest audit | `backend/artifacts/package_manifest_audit.md` |
| Promoted signal intelligence audit | `backend/artifacts/promoted_signal_intelligence_audit.md` |
| Latest Automation Bus audit summary | `automation_bus/latest_audit_summary.md` |
| Latest cursor prompt | `automation_bus/latest_cursor_prompt.md` |

---

## 3. Authority Assessment

### Strategy

| Document | Status | Reason |
|---|---|---|
| `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` | **Authoritative — current truth** | April 2026. Full codebase read. Named engine bugs, product gap, governance calibration issue, and reset plan. This is the most honest and complete state-of-truth document in the repo. |
| `docs/RESET_SPRINT_PLAN_2026-04.md` | **Authoritative — current operative plan** | April 2026. Concrete sprint sequence, governance tier per sprint, success criteria. References the April review as its source. This is the governing sprint plan as of now. |
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | **Authoritative — strategic spine** | The adopted master strategy document. Governs direction, phase structure, and platform bets. Not superseded by the April reset — the reset operates within it. Both must be read together. |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` | **Authoritative — addendum to above** | Extends the v1.5 FINAL with first-market scope decisions. Should be read alongside the parent. |
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` | **Superseded** | The v1.5 FINAL explicitly supersedes v1.4. |
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` (no version suffix) | **Superseded / unclear** | Pre-versioned draft. No version marker. Superseded by v1.5 FINAL. |
| `docs/MASTER_ROADMAP_v5.2_to_v5.3.md` | **Stale — partially superseded** | Describes v5.2/v5.3 phase framing. Much of the v5.2 "remaining mandatory work" it lists has either been completed or is now reordered by the April 2026 reset. Do not use as a current sprint sequencing guide without cross-referencing the reset plan. |
| `docs/Download-Arch/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan*.md` (9 versions) | **Superseded — archive** | All pre-FINAL drafts. The FINAL ADOPTED version supersedes all of them. |
| `docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md` | **Supporting — governance note** | Correctly describes how strategy documents should relate to each other. The decision register it proposes does not exist yet as a live document. |
| `docs/strategy/HealthIQ_Executive_GTM_Report_Updated_v2.md` | **Supporting — GTM reference** | Market positioning context. Does not reflect April 2026 reset findings. Use with caution for commercial decisions. |
| `docs/HealthIQ_Phase1_Launch_Posture.md` | **Unclear status** | Describes launch posture. Not verified against April 2026 reset gaps. May be aspirational rather than current-state. |

### Architecture

| Document | Status | Reason |
|---|---|---|
| `architecture/ARCHITECTURE_INDEX.md` + ADR-001/002/003/005 | **Authoritative** | The ADR model is correctly structured. ADR-001 through ADR-003 establish the three-layer governance invariants and are binding constraints. ADR-005 is the active signal evaluation architecture (ADR-004 superseded). |
| `architecture/ARCHITECTURE_GUARDRAILS.md` | **Authoritative** | Enforceable rules derived from the ADR set. |
| `architecture/HEALTHIQ_REASONING_PIPELINE.md` | **Authoritative** | Canonical definition of the Evidence → Signal → Insight model. |
| `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md` | **Supporting — may be stale** | Inventory of analytical assets at v5.2 baseline. Knowledge Bus packages have grown significantly since. Do not treat as a complete current count. |
| `docs/ARCHITECTURE_REVIEW_REPORT.md` | **Stale — unsafe to rely on** | From Sprint 14, October 2025. `DOCUMENTATION_HIERARCHY.md` declares it Level 1 PRIMARY SSOT — this is incorrect. It does not reflect the current product state and should be archived. The April 2026 product review explicitly calls this out. |
| `docs/DOCUMENTATION_HIERARCHY.md` | **Stale — misleading** | Its authority hierarchy is wrong: it elevates a Sprint 14 document and does not reference any of the April 2026 authoritative documents. Following this document for navigation will lead to stale truth. |

### Intelligence / Analysis Layer

| Document | Status | Reason |
|---|---|---|
| `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | **Authoritative — current truth** | April 2026. Repo-grounded. Cites exact file paths and line numbers. Named the three engine bugs (contradictory signal activation, one-sided bounds, WHY coverage gap) with code evidence. The most technically precise product-state document in the repo. |
| `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | **Authoritative — analytical coverage truth** | March 2026. Systematic audit of signal coverage, hypothesis assets, and phenotype fixtures across all metabolic pathways. Confirmed: ~30 of 33 non-hcy signals have no WHY hypothesis asset. Renal pathway has zero interaction-map edges. Not superseded — findings are still unresolved. |
| `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | **Authoritative — Wave 1 contract** | The active contract for domain narrative structure in Wave 1. Confirmed present by Sentinel Phase 1 test run. |
| `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | **Authoritative** | Governing policy for how primary concern and ranked ambiguity are determined. |
| `docs/Wave1-codebase-analysis_v3.md` | **Supporting** | v3 is the latest; v2 also present but superseded. Provides Wave 1 implementation reality check. |
| `docs/investigations/2026-04-12_*.md` (4 files) | **Supporting — operational records** | April 2026 investigation notes on insulin resistance visibility, narrative contract inventory, lab range fallback policy, and WHY narrative runtime. Valuable reference; not standalone authority documents. |
| `docs/investigations/KB-S*_PREFLIGHT.md` (many files) | **Operational records** | Sprint preflight investigations for Knowledge Bus sprints. Historical record of what was checked before each KB sprint. Not current-state documents. |
| ADR-008 + ADR-009 | **Authoritative** | Promoted signal intelligence contract and root-cause WHY architecture. Binding constraints for KB sprint work. Note: ADR-007 (`clinician-summary-report`) is present but no ADR-006 exists — the numbering gap is unexplained. |

### Frontend / UX

| Document | Status | Reason |
|---|---|---|
| `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | **Authoritative** | v6 is the latest Results Journey paper. The strategy authority map designates the Results Journey Paper as the authority for results page architecture. v1–v5 all exist in Download-Arch and are superseded. |
| `docs/strategy/Interpretation_Display_Layer_Design_Lock.md` | **Authoritative** | Locked design decision for the Interpretation Display Layer. |
| `docs/QUESTIONNAIRE_UX_REDESIGN_BACKGROUND.md` | **Authoritative — active work** | Background for Q-1 (guided section-by-section questionnaire flow). Listed in CLAUDE.md as in-progress. |
| `docs/QUESTIONNAIRE_VISUAL_REDESIGN_Q2_BACKGROUND.md` | **Authoritative — active work** | Background for Q-2 (premium visual layer). In-progress per CLAUDE.md. |
| `docs/RESET_SPRINT_PLAN_2026-04.md` — Sprint 3 spec | **Authoritative for results page** | Sprint 3 of the reset plan contains the operative results page restructure specification. This supersedes the Download-Arch surface policy documents for immediate sprint work. |
| `docs/Download-Arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` | **Supporting** | Historical surface policy. Useful as design context. The reset sprint plan's Sprint 3 specification is the operative frontend restructure guide. |
| `docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md` | **Supporting — may be stale** | Design package at v5.2. The v6 Results Journey Paper and the Sprint 3 reset spec are more current for implementation work. |
| `docs/context/UX_UI_GUIDE.md` | **Stale** | Pre-governance-era UX guide in the `context/` directory. The Results Journey Paper v6 supersedes it for results page direction. |

### Testing / Quality

| Document | Status | Reason |
|---|---|---|
| `docs/testing/healthiq_sentinel_phase1_implementation_report.md` | **Authoritative — current quality truth** | 2026-05-03. Documents exactly what Sentinel Phase 1 built, what tests pass, and what is deferred to Phase 2+. The most current quality-state document. 32/32 regression tests pass. Clearly states coverage gaps. |
| `docs/testing/brief for HealthIQ AI Phase 1 Sentinel.md` | **Authoritative — Sentinel scope definition** | The governing brief for Sentinel Phase 1. Defines scope, constraints, and what Phase 1 is not. |
| `docs/testing/healthiq_sentinel_repo_audit_v1.md` | **Supporting** | The repo audit that preceded Sentinel Phase 1 implementation. Historical context. |
| `docs/testing/automated-testing-sentinel-repo-audit-report.md` | **Duplicate / overlapping** | Appears to be an earlier or parallel version of the sentinel repo audit. Status relative to `healthiq_sentinel_repo_audit_v1.md` is unclear. |
| `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` | **Supporting — governance** | Describes the testing operating model philosophy. Predates Sentinel implementation. Still relevant for understanding the testing governance intent. |
| `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md` | **Supporting** | Background for the agentic testing strategy that led to Sentinel. Historical context. |
| `docs/testing/UAT1/UAT1_findings.md` | **Supporting — historical** | UAT1 findings document. Date unclear. Not a current-state quality document. |
| `TEST_PLAN.md`, `TEST_LEDGER.md` (root level) | **Stale** | Root-level test documents from early in the project. Superseded by Sentinel. Should be archived. |

### Governance / Control-Plane

| Document | Status | Reason |
|---|---|---|
| `.claude/CLAUDE.md` | **Authoritative — always current** | The permanent context file. Actively maintained. Contains the current phase, active focus, and non-negotiables. The highest-signal short document in the repo. |
| `docs/AUTOMATION_BUS_SOP_v1.3.1.md` | **Authoritative** | Active SOP. MEMORY.md confirms this is the operative governance version. |
| `docs/KNOWLEDGE_BUS_SOP_v1.3.md` | **Authoritative** | Active Knowledge Bus SOP. |
| `docs/AUTOMATION_BUS_SOP_v1.3.md` | **Superseded** | Superseded by v1.3.1. |
| `docs/AUTOMATION_BUS_SOP_v1.2.md` | **Superseded** | Superseded by v1.3. |
| `docs/KNOWLEDGE_BUS_SOP_v1.2.md` | **Superseded** | Superseded by v1.3. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.1.md` + `v1.2 (1).md` | **Superseded** | Old SOP versions. Should not be referenced. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.3.1_aligned.md` etc. | **Superseded draft variants** | Multiple v1.3.1 alignment/merge/stash-fix-patch variants. None are operative. The canonical is in `/docs/`. |
| `docs/agents/CURSOR_OPERATING_POLICY.md` | **Authoritative** | Governs how Cursor operates within the bus. |

### Root-Level Fix Reports (~40 files)

| Group | Status |
|---|---|
| `BIOMARKER_PERSISTENCE_FIX.md`, `ALIAS_NORMALIZATION_INSTRUMENTATION.md`, `COMPLETE_FLOW_FIX_FINAL.md`, `EVENTSOURCE_DUPLICATION_FIX.md`, `DTO_ALIGNMENT_REPORT.md`, and ~35 similar files | **Historical — should be archived** | These are post-hoc firefighting reports from the pre-governance era. They tell the history of the project honestly but have no current operational value. The April 2026 reset plan explicitly calls for moving them to `docs/archived/`. |

---

## 4. Current-State Pack Recommendation

Leadership should read these **seven documents** to understand HealthIQ AI as it exists today. No others are required for a current-state understanding.

| # | Document | Path | Why it belongs here |
|---|---|---|---|
| 1 | **Product Review & Strategic Reset** | `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` | The most complete, honest, repo-grounded state-of-truth document. Covers engine, product shell, governance, repo hygiene, and documentation. Read this first. |
| 2 | **Product Reality & Direction Audit** | `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | The companion technical audit. Names the three engine bugs with code citations. Provides reproducible evidence. Read alongside the April review. |
| 3 | **Reset Sprint Plan** | `docs/RESET_SPRINT_PLAN_2026-04.md` | The operative 8-sprint plan for the current period. Defines what work is ordered how, what governance tier applies to each sprint, and what "done" means for each sprint. |
| 4 | **CLAUDE.md** | `.claude/CLAUDE.md` | The permanent context file. Contains the current active focus, architectural non-negotiables, and standing lessons. Kept current. Short read. |
| 5 | **Metabolic Pathway Coverage Audit** | `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | Authoritative map of what the intelligence layer actually covers and what is missing. Still accurate. The WHY coverage gap it documents is unresolved. |
| 6 | **Strategic Vision v1.5 FINAL ADOPTED** | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | The master strategic record. Provides the phase structure and long-range intent within which the reset plan operates. |
| 7 | **Sentinel Phase 1 Implementation Report** | `docs/testing/healthiq_sentinel_phase1_implementation_report.md` | The current quality layer truth. Documents what regression coverage exists, what tests pass, and what quality gaps are explicitly deferred to Phase 2+. |

---

## 5. Confusion and Duplication Findings

### 5.1 The navigation hierarchy points to stale truth

`docs/DOCUMENTATION_HIERARCHY.md` is the designated navigation document for new contributors. It declares `docs/ARCHITECTURE_REVIEW_REPORT.md` as "Level 1 PRIMARY SSOT" for current sprint status. That document is from Sprint 14, October 2025. A developer starting work from the hierarchy will believe the product is at a different state than it is. This is the most operationally dangerous documentation problem in the repo.

### 5.2 Multiple authoritative versions of the strategy document coexist

In `docs/` alone: an un-versioned copy, v1.4 amended, and v1.5 FINAL ADOPTED. In `docs/Download-Arch/`: nine further versions (v1.5 draft through revision v9, plus feedback files and master variants). The FINAL ADOPTED version is the correct one, but the others are not labelled as superseded. A reader landing in `docs/` or `Download-Arch/` cannot easily identify the current version without already knowing what it is.

### 5.3 `docs/Download-Arch/` is an unsorted working-papers dump

Approximately 90 documents of mixed status: working papers, feedback files, superseded SOPs, old strategy drafts, research briefs, and meeting outputs. The name `Download-Arch` implies archival but provides no labelling or status hierarchy. These documents are indistinguishable from authoritative ones to a cold reader. Several important documents are buried here by proximity to junk (e.g. the surface policy final v3 is in Download-Arch alongside superseded v1/v2 versions of the same document).

### 5.4 The `docs/context/` directory is a pre-governance-era fragment

`docs/context/` contains files such as `PRD.md`, `INTELLIGENCE_LIFECYCLE.md`, `STACK_*.md`, `SPRINT_LOG.md`, and `UX_UI_GUIDE.md`. These were created early in the project and many have been superseded by the more structured governance documents. They remain present and are referenced by `DOCUMENTATION_HIERARCHY.md` as "Level 2 CANONICAL SPECIFICATION." Their actual currency is unknown — they have not been audited against the current codebase.

### 5.5 Good intelligence audits get orphaned

The April 2026 audits (`PRODUCT_REALITY_AND_DIRECTION_AUDIT.md`, `METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`) are the two most honest documents in the repo. The April product review explicitly calls them out as ground truth. Yet they sit in `docs/investigations/` and `docs/` respectively, with no pointer from the navigation hierarchy and no prominent linkage. A new contributor would have to know to look for them.

### 5.6 Multiple SOP versions coexist without clear supersession labelling

Three versions of the Automation Bus SOP are present in `/docs/` (v1.2, v1.3, v1.3.1). Five additional variants are in `docs/Download-Arch/`. None of the superseded versions carry a header declaring their status. A developer who finds v1.3 has no immediate signal that v1.3.1 is the operative version. The SOPs are long documents — a developer who reads the wrong one will work to an incorrect procedure.

### 5.7 Sentinel Phase 1 work is committed but the quality picture is not anchored

The Sentinel implementation report (2026-05-03) is a high-quality, complete document. However, it notes that "all work is uncommitted and not merged to `main`" — this was the state at report time. The current git status shows the main branch is clean, and the recent commits include Sentinel fixes. The implementation report needs to be the primary quality-state reference, but it is not linked from anywhere in the documentation hierarchy.

### 5.8 Root-level markdown proliferation

Approximately 40 fix-report markdown files at the repository root (`BIOMARKER_PERSISTENCE_FIX.md`, `COMPLETE_FLOW_FIX_FINAL.md`, `DTO_ALIGNMENT_REPORT.md`, etc.) create noise for any navigation attempt. These are not current truth — they are historical incident records. Their presence at root implies currency they do not have.

---

## 6. Missing Truth

The following important current-state facts have no single clear documented source of truth.

### 6.1 No sprint execution status register

The reset plan (`RESET_SPRINT_PLAN_2026-04.md`) defines Sprints 1–8. There is no document recording which of those sprints has started, what status they are at, or what has been completed. The April reset plan is the goal; the gap between it and the current codebase state is undocumented. Leadership cannot determine whether Sprint 1 (engine trust bugs) has been done, is in-flight, or has not started. This is the most operationally urgent missing document.

### 6.2 No current launch-grade analytical scope document

The engine has 137 registered signals, 187 Knowledge Bus packages, and 6 WHY-governed signals. The Metabolic Pathway Coverage Audit documents what is covered vs missing, but there is no single document that answers: "For Phase 1 launch, which analytical domains are considered complete, which are partial, and which are explicitly out of scope?" The coverage audit identifies the gaps but does not assign a launch posture to each domain.

### 6.3 No frontend design system truth

There is no current single-source-of-truth document for the frontend design system as implemented: component library, typography, colour system, spacing, and interaction patterns. The Results Journey Paper v6 defines the results page target architecture. The UX Design Package defines wireframes. But the actual implemented design system — what Radix UI components are in use, what Tailwind theme is configured, what component patterns are canonical — is undocumented. This means frontend work proceeds without a clear "what does correct look like" reference.

### 6.4 No decision register

The strategy authority map (`docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md`) proposes a cross-stack decision register with 12 initial decisions. That register does not exist as a live document. Decisions made in audits, chat, or preflight investigations are not consolidated anywhere. The same decisions (e.g. whether biomarkers lead the experience, what the phenotype naming convention is, whether Gemini is optional polish) are re-litigated in different documents.

### 6.5 No release confidence model

There is no document that defines what "release confidence" means for HealthIQ AI: what test coverage is required, what manual QA gates must pass, what clinical review is needed, what the known-acceptable-bug list is, and what blocks vs does not block a release. The Sentinel Phase 1 establishes regression coverage for specific defect classes, but there is no connecting document that ties quality gates to a release readiness verdict.

### 6.6 No commercial/pricing decision record

The pricing model is acknowledged as missing (a Sprint 7 action in the reset plan). But there is also no document recording what pricing decisions have been discussed, what was rejected and why, or what the current commercial hypothesis is. Sprint 7 requires "the model has been chosen before work begins" but there is no document where that choice is recorded or being deliberated.

### 6.7 No honest frontend implementation state

The April 2026 product review contains the most honest frontend state assessment (the 2/10 complete table). But this is embedded in a large review document, not in a current implementation state document that would be maintained over time. As the reset sprints are completed (Sprint 3: results restructure, Sprint 4: PDF export, etc.), there is nowhere to record what the implementation reality has become.

---

## 7. Documentation Reset Recommendation

The April 2026 reset plan already specifies the documentation hygiene work. This section does not repeat those tasks — it states what the output of a documentation reset should be.

### 7.1 A single entry point

Create `docs/README.md` as the true index: one section per domain (Strategy, Architecture, Intelligence, Frontend, Testing, Governance), with each entry being one or two sentences describing the document and its current status (authoritative / superseded / archive). This file is the only navigation document. `DOCUMENTATION_HIERARCHY.md` is retired.

### 7.2 A clean authority tier

The documentation structure should express three tiers:
- **Current truth** — documents that reflect the product as it exists now and are safe to act on
- **Reference** — documents that are accurate within their scope but not the full picture (e.g. ADRs, SOPs, the strategy plan)
- **Archive** — superseded, historical, or firefighting documents that should not be cited for current-state decisions

Currently all three tiers are co-mingled. A reset should make the tier visible in the file structure: `docs/archive/` for tier 3, clear naming or headers for tier 2 documents, and the `docs/README.md` entry point making tier 1 explicit.

### 7.3 A sprint execution status register

A short living document — `docs/SPRINT_STATUS.md` or equivalent — that records for each reset sprint: status (not started / in-flight / complete), branch name, gate outcome, and completion date. Updated by whoever completes each sprint. This is the document that answers "where are we?" without requiring a git log audit.

### 7.4 A decision register

A short document recording the cross-stack decisions that the strategy authority map proposed. These decisions are currently scattered across strategy papers, preflight investigations, and ADRs. Consolidating them into one short register (the 12 decisions plus any that have been made since) would eliminate repeated re-litigation.

### 7.5 An archived fix-report directory

Move the ~40 root-level fix-report markdown files to `docs/archive/fix-reports/`. They have historical value but are not current-state documents. Their presence at root suggests currency they do not have.

### 7.6 A supersession label on old SOP versions

Each superseded SOP (v1.2, v1.3) should carry a one-line header: `> SUPERSEDED — see docs/AUTOMATION_BUS_SOP_v1.3.1.md`. This prevents developers who find the wrong version from following an outdated procedure.

### 7.7 What the reset should NOT produce

- A giant new architecture document consolidating everything that already exists
- A new PRD to replace the existing one
- A new strategy paper
- A new governance framework

The documents that need to be written are: the README index, the sprint status register, and the decision register. Everything else is curation, archival, and labelling — not new writing.

---

## 8. Open Ambiguities

The following could not be confidently determined from the repo alone.

### 8.1 Reset Sprint 1 execution status

The reset plan was produced in April 2026. The three engine trust bugs it names (contradictory signal activation, one-sided bounds, WHY fallback) were identified in the April audit. It is not possible to determine from documentation alone whether Sprint 1 has been completed. The CLAUDE.md active focus section describes Wave 1 domain card work and Questionnaire UX redesign — not engine trust bugs — which suggests Sprint 1 may not yet be complete. This should be verified against the codebase directly.

### 8.2 `docs/context/` currency

The files in `docs/context/` (INTELLIGENCE_LIFECYCLE.md, STACK_*.md, SPRINT_LOG.md, etc.) were not fully audited. It is unclear whether they have been maintained alongside the governance evolution or are pre-governance-era fragments. Their operational status cannot be assessed from file dates alone.

### 8.3 The `docs/investigations/2026-04-21_N3_longitudinal_lab_value_contract.md` scope

This investigation file (April 2026) was not read in full during this review. Its relationship to the reset sprint plan (specifically Sprint 6: Trend View) is unclear — it may be an N-3 sprint preflight or a standalone investigation.

### 8.4 ADR-006 gap

The Architecture Index lists ADR-007 and ADR-008 but no ADR-006. Either ADR-006 was never created, was deleted, or is under a different number. This numbering gap is unexplained.

### 8.5 `docs/compliance/` coverage adequacy

The compliance directory contains `DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md`, `PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md`, and a vendor subprocessor inventory. The April 2026 product review identified a GDPR gap (no privacy disclosure on LLM parsing at upload). Whether the compliance documents address or omit this gap was not verified in this review.

### 8.6 Wave 1 domain card work completion state

CLAUDE.md describes Wave 1 domain cards D-2 through D-7 as complete. The exact state of D-1 and whether D-2 through D-7 completion means merged-to-main or implemented-on-a-branch is not clear from documentation alone.

---

*This review was produced by reading the full documentation landscape and a representative selection of key document content. All file paths cited above were verified to exist. Authority assessments are based on document content and dates — they should be treated as a starting point for leadership judgement, not a final verdict.*
