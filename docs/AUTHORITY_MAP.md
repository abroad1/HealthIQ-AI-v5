# HealthIQ AI — Document Authority Map

**Last updated:** 2026-06-20  
**Status:** LIVE — update when document status changes  
**Purpose:** Stop people reading the wrong documents. One page, fast answer.

---

## How to Use This Map

Find the domain you care about. Look at the Status column.

- **AUTHORITATIVE** — current truth, safe to act on
- **SUPPORTING** — accurate within its scope, not the full picture; use as reference
- **STALE** — the facts it contains may be outdated; do not use for current decisions
- **SUPERSEDED** — replaced by a newer document
- **ARCHIVE** — historical record; useful for understanding history but not current truth
- **UNCLEAR** — status could not be verified from the repo; exercise caution

---

## Strategy

| Document | Status | Notes |
|---|---|---|
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | AUTHORITATIVE | Master strategic record. |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` | AUTHORITATIVE | Read with parent. |
| `docs/strategy/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` | AUTHORITATIVE | April 2026 full review. |
| `docs/strategy/RESET_SPRINT_PLAN_2026-04.md` | AUTHORITATIVE | 8-sprint reset plan. All complete. |
| `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | AUTHORITATIVE | Eight-block beta-readiness programme baseline. First authority for P1-1 and build programme. |
| `docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md` | SUPPORTING | Governance note on doc hierarchy. |
| `docs/strategy/HealthIQ_Executive_GTM_Report_Updated_v2.md` | SUPPORTING | GTM context. |
| `docs/strategy/HealthIQ_Phase1_Launch_Posture.md` | UNCLEAR | Currency uncertain. Verify against April review. |
| `docs/strategy/Phenotype_Terminology_Proposal.md` | SUPPORTING | Phenotype naming proposal. |
| `docs/strategy/healthiq_future_screening_priorities.md` | SUPPORTING | Future screening priorities. |
| `docs/archive/superseded/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` | SUPERSEDED | Superseded by v1.5 FINAL. Moved to archive. |
| `docs/archive/superseded/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` (no version) | SUPERSEDED | Pre-versioning draft. Moved to archive. |
| `docs/archive/working-papers/download-arch/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan*.md` (9 files) | ARCHIVE | All pre-FINAL drafts. |
| `docs/archive/working-papers/download-arch/HealthIQ_Final_Results_Journey_Recommendation_Paper_v*.md` (v1–v5) | ARCHIVE | All superseded. v6 is current (now in docs/frontend/). |

---

## Architecture

| Document | Status | Notes |
|---|---|---|
| `architecture/ARCHITECTURE_INDEX.md` | AUTHORITATIVE | ADR registry. Constitutional record. |
| `architecture/ADR-001-platform-non-negotiables.md` | AUTHORITATIVE | Binding governance invariants. |
| `architecture/ADR-002-deterministic-analysis-engine.md` | AUTHORITATIVE | Three-layer architecture. |
| `architecture/ADR-003-knowledge-bus-architecture.md` | AUTHORITATIVE | Knowledge Bus evidence architecture. |
| `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | AUTHORITATIVE | Active signal evaluation arch. |
| `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` | AUTHORITATIVE | Signal intelligence contract. |
| `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` | AUTHORITATIVE | Root-cause WHY architecture. |
| `architecture/ADR-007-clinician-summary-report.md` | AUTHORITATIVE | Clinician summary report contract. |
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | AUTHORITATIVE | Canonical Layer A/B/C vocabulary for roadmap and sprint planning. |
| `architecture/ADR-004-disease-specific-signal-evaluation.md` | SUPERSEDED | Superseded by ADR-005. |
| `architecture/ARCHITECTURE_GUARDRAILS.md` | AUTHORITATIVE | Enforceable rules. |
| `architecture/HEALTHIQ_REASONING_PIPELINE.md` | AUTHORITATIVE | Canonical pipeline model. |
| `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md` | SUPPORTING | Asset inventory. May undercount — KB has grown. |
| `docs/architecture/openapi.yaml` | SUPPORTING | API contract. |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | SUPPORTING | Retail explainer content boundary rules. |
| `docs/architecture/SIGNAL_ARCHITECTURE_COMPLETION_v1.0.md` | SUPPORTING | Signal architecture completion note. |
| `docs/architecture/R-2A_backend_sse_removal.md` | SUPPORTING | R-2A sprint note: backend SSE removal. |
| `docs/archive/working-papers/PHASE_0_AS_IS_ARCHITECTURE_AUDIT.md` | ARCHIVE | Pre-project baseline. Moved to archive. |
| `docs/archive/superseded/ARCHITECTURE_REVIEW_REPORT.md` | STALE | Sprint 14 / October 2025. Moved to archive. |
| `docs/archive/superseded/DOCUMENTATION_HIERARCHY.md` | SUPERSEDED | Pointed to stale docs. Moved to archive. Use `docs/README.md`. |

---

## Intelligence / Analysis Layer

| Document | Status | Notes |
|---|---|---|
| `docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | AUTHORITATIVE | April 2026 technical audit. Code-grounded. |
| `docs/intelligence/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | AUTHORITATIVE | Coverage map. Renal and Wave 2 WHY gaps still open. |
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | AUTHORITATIVE | Wave 1 domain narrative contract. |
| `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | AUTHORITATIVE | Primary concern policy. |
| `docs/intelligence/Wave1-codebase-analysis_v3.md` | SUPPORTING | v3 is latest. |
| `docs/intelligence/2026-04-12_full_results_narrative_contract_inventory.md` | SUPPORTING | Narrative contract inventory. |
| `docs/intelligence/2026-04-12_insulin_resistance_and_narrative_visibility_investigation.md` | SUPPORTING | IR narrative investigation. |
| `docs/intelligence/2026-04-12_lab_range_fallback_policy_alignment.md` | SUPPORTING | Lab range fallback policy. |
| `docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md` | SUPPORTING | WHY narrative runtime investigation. |
| `docs/intelligence/2026-04-21_N3_longitudinal_lab_value_contract.md` | SUPPORTING | Longitudinal lab value contract (N-3). |
| `docs/intelligence/2026-04-26_D5_wave1_runtime_diagnosis.md` | SUPPORTING | D-5 runtime diagnosis. |
| `docs/intelligence/R-8_why_coverage_wave1.md` | SUPPORTING | WHY Wave 1 sprint implementation note. |
| `docs/intelligence/R-1B_unscored_marker_trust_gaps.md` | SUPPORTING | Unscored marker trust gaps sprint note. |
| `docs/intelligence/HealthIQ_Intelligence_Model_Design_Second_Pass.md` | SUPPORTING | Intelligence model design workshop output. |
| `docs/intelligence/HealthIQ_Investigation_Layer.md` | SUPPORTING | Investigation layer architecture note. |
| `docs/intelligence/Intervention_Effects_Registry_Discussion_Note.md` | SUPPORTING | Intervention effects registry design. |
| `docs/intelligence/Intervention_Registry_Investigation_Memo.md` | SUPPORTING | Intervention registry investigation. |
| `docs/archive/sprint-history/investigations/` (~30 files) | ARCHIVE | KB sprint preflights (KB-S*, FE_*, BE_S1, etc.). Historical record. |
| `docs/archive/sprint-history/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md` | ARCHIVE | VR primary concern ranking investigation. |
| `backend/artifacts/intelligence_model_audit.md` | SUPPORTING | Intelligence model audit artifact. |
| `backend/artifacts/promoted_signal_intelligence_audit.md` | SUPPORTING | Promoted signal audit. |

---

## Frontend / UX

| Document | Status | Notes |
|---|---|---|
| `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | AUTHORITATIVE | Current results experience authority. |
| `docs/frontend/Interpretation_Display_Layer_Design_Lock.md` | AUTHORITATIVE | IDL design lock. |
| `docs/frontend/HealthIQ_IDL_Naming_Decision_Note_Approved.md` | AUTHORITATIVE | IDL naming. Approved and locked. |
| `docs/frontend/QUESTIONNAIRE_UX_REDESIGN_BACKGROUND.md` | AUTHORITATIVE | Q-1 background. |
| `docs/frontend/QUESTIONNAIRE_VISUAL_REDESIGN_Q2_BACKGROUND.md` | AUTHORITATIVE | Q-2 background. |
| `docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md` | SUPPORTING | Layer C translation spec. |
| `docs/frontend/clinician_language_style_guide_v1.md` | SUPPORTING | Clinical language style. |
| `docs/frontend/clinician_report_v1_spec.md` | SUPPORTING | Clinician report spec. |
| `docs/frontend/HealthIQ_Results_Page_UX_Design_Package.md` | SUPPORTING | v5.2 design package. Results Journey Paper v6 is current authority. |
| `docs/frontend/HealthIQ_Results_Wireframe_Package.md` | SUPPORTING | v5.2 wireframes. |
| `docs/archive/sprint-history/context/UX_UI_GUIDE.md` | ARCHIVE | Pre-governance era. Superseded by Results Journey Paper v6. |
| `docs/archive/working-papers/download-arch/HealthIQ_Results_Page_UX_Design_Package_v*.md` (v1–v5) | ARCHIVE | Superseded versions. |
| `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` | SUPPORTING | Historical surface policy. Useful context. |
| `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v*.md` (v1–v2) | ARCHIVE | Superseded. |

---

## Testing / Quality

| Document | Status | Notes |
|---|---|---|
| `docs/testing/healthiq_sentinel_phase1_implementation_report.md` | AUTHORITATIVE | 2026-05-03. Current quality truth. |
| `docs/testing/brief for HealthIQ AI Phase 1 Sentinel.md` | AUTHORITATIVE | Sentinel Phase 1 scope. |
| `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` | SUPPORTING | Testing operating model. |
| `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md` | SUPPORTING | Agentic testing strategy background. |
| `docs/testing/healthiq_sentinel_repo_audit_v1.md` | SUPPORTING | Repo audit preceding Sentinel. |
| `docs/testing/automated-testing-sentinel-repo-audit-report.md` | UNCLEAR | Relationship to `healthiq_sentinel_repo_audit_v1.md` unclear. May be duplicate or earlier version. |
| `docs/testing/UAT1/UAT1_findings.md` | ARCHIVE | UAT1 findings. Date uncertain. |
| `docs/archive/fix-reports/TEST_LEDGER.md` | ARCHIVE | Moved from root. Historical. |
| `docs/archive/fix-reports/TEST_PLAN.md` | ARCHIVE | Moved from root. Historical. |
| `reports/audit/LEGACY_TEST_INFRASTRUCTURE_ANALYSIS.md` | ARCHIVE | Legacy test infrastructure analysis. |

---

## Governance / Control-Plane

| Document | Status | Notes |
|---|---|---|
| `.claude/CLAUDE.md` | AUTHORITATIVE | Permanent context. Always current. |
| `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` | AUTHORITATIVE | Active SOP. |
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md` | AUTHORITATIVE | Active Knowledge Bus SOP. |
| `docs/governance/CURSOR_OPERATING_POLICY.md` | AUTHORITATIVE | Cursor operating policy. |
| `AGENTS.md` | AUTHORITATIVE | Agent operating map. |
| `docs/governance/healthiq-core-engine.md` | SUPPORTING | Core engine agent definition. |
| `docs/governance/healthiq-frontend-shell.md` | SUPPORTING | Frontend shell agent definition. |
| `docs/governance/healthiq-qa-uat.md` | SUPPORTING | QA/UAT agent definition. |
| `docs/governance/healthiq-docs-hygiene.md` | SUPPORTING | Docs hygiene agent definition. |
| `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md` | AUTHORITATIVE | Pre-SOP prompt scoping working convention (Stages 0, A–E). Separate from Automation Bus SOP. |
| `automation_bus/latest_scope_advisory.md` | SUPPORTING | Per-sprint Stage B advisory cache. Advisory only — does not authorise execution. |
| `automation_bus/latest_pipeline_advisory.md` | SUPPORTING | Stage 0 batch pipeline advisory cache. Advisory only — does not authorise execution. |
| `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.3.md` | SUPERSEDED | Moved to archive. |
| `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.2.md` | SUPERSEDED | Moved to archive. |
| `docs/archive/superseded/KNOWLEDGE_BUS_SOP_v1.2.md` | SUPERSEDED | Moved to archive. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.1.md` | ARCHIVE | Old version. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.2 (1).md` | ARCHIVE | Old version. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.3.1_aligned.md` | ARCHIVE | Draft/alignment variant. Not operative. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.3.1_final_merged.md` | ARCHIVE | Draft/merge variant. Not operative. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.3.1_stash_fix_patch.md` | ARCHIVE | Patch draft. Not operative. |
| `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_v1.3.2_draft.md` | ARCHIVE | Draft of a potential future version. Not operative. |
| `automation_bus/latest_audit_summary.md` | SUPPORTING | Most recent gate audit output. Operational record. |
| `automation_bus/latest_cursor_prompt.md` | SUPPORTING | Most recent cursor prompt. Operational artefact. |

---

## Ops / Launch / Compliance

| Document | Status | Notes |
|---|---|---|
| `docs/ops/OPEN_ITEMS_AND_PHASE1_BOUNDARIES.md` | SUPPORTING | Phase 1 open items. |
| `docs/ops/OPERATIONAL_CONTROLS_BASELINE_PHASE1.md` | SUPPORTING | Operational controls. |
| `docs/ops/UK_HOSTING_AND_RESIDENCY_PHASE1.md` | SUPPORTING | UK hosting posture. |
| `docs/ops/VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md` | SUPPORTING | Vendor inventory. |
| `docs/ops/local-development.md` | SUPPORTING | Local development setup. |
| `docs/compliance/DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md` | SUPPORTING | Phase 1 data flow. |
| `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` | UNCLEAR | Privacy review. April 2026 identified a GDPR gap on LLM parsing. Verify whether this document covers it. |
| `docs/product/WEDGE_EVENT_CONTRACT_AND_GOVERNANCE_PHASE1.md` | SUPPORTING | Wedge event contract. |

---

## Archive Directories

See `docs/archive/README.md` for full archive structure.

| Location | What it contains |
|---|---|
| `docs/archive/fix-reports/` | ~40 root-level incident/fix reports (2025). Historical record only. |
| `docs/archive/superseded/` | Superseded SOPs (v1.2, v1.3), old strategy plan versions (v1.4 and earlier), old baseline docs, deprecated navigation docs. |
| `docs/archive/working-papers/` | Working papers, docx design files, early research proposals, PRP tooling, Download-Arch dump of ~90 historical documents. |
| `docs/archive/sprint-history/` | Old sprint notes, preflight investigations, delivery reports, golden-narrative design work, pre-governance context files, stash patches, diagnostics. |
| `backend/artifacts/` | Golden run outputs, arbitration run outputs, audit artifacts. Operational history. |

---

## Documents With Unclear Status (Needs Leadership Review)

| Document | Why Unclear |
|---|---|
| `docs/strategy/HealthIQ_Phase1_Launch_Posture.md` | Not verified against April 2026 review findings. |
| `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` | April review found GDPR gap not covered by disclosure in upload flow. |
| `docs/testing/automated-testing-sentinel-repo-audit-report.md` | Possible duplicate of `healthiq_sentinel_repo_audit_v1.md`. |
| `docs/archive/sprint-history/context/` (all context/ files) | Moved to archive in Pass 2. Pre-governance content, not verified for current accuracy. Do not cite as current truth. |
| `architecture/` — ADR-006 gap | ADR-007 and ADR-008 exist; ADR-006 does not. No explanation in index. |
