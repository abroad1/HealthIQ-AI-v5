# HealthIQ AI — Document Authority Map

**Last updated:** 2026-05-04  
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
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | AUTHORITATIVE | Master strategic record. |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` | AUTHORITATIVE | Read with parent. |
| `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` | AUTHORITATIVE | April 2026 full review. |
| `docs/RESET_SPRINT_PLAN_2026-04.md` | AUTHORITATIVE | 8-sprint reset plan. All complete. |
| `docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md` | SUPPORTING | Governance note on doc hierarchy. |
| `docs/strategy/HealthIQ_Executive_GTM_Report_Updated_v2.md` | SUPPORTING | GTM context. |
| `docs/HealthIQ_Phase1_Launch_Posture.md` | UNCLEAR | Currency uncertain. Verify against April review. |
| `docs/MASTER_ROADMAP_v5.2_to_v5.3.md` | STALE | v5.2/v5.3 framing. Partially superseded by reset. Do not use for sprint sequencing. |
| `docs/Delivery_Sprint_Plan_v5.2.md` | SUPERSEDED | Pre-reset sprint plan. |
| `docs/Master_PRD_v5.2.md` | SUPERSEDED | v5.2 PRD. Reset plan supersedes it for Phase 1 execution. May have useful feature specification detail. |
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` | SUPERSEDED | Superseded by v1.5 FINAL. |
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` (no version) | SUPERSEDED | Pre-versioning draft. |
| `docs/Download-Arch/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan*.md` (9 files) | ARCHIVE | All pre-FINAL drafts. |
| `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | AUTHORITATIVE | Current results experience authority. |
| `docs/Download-Arch/HealthIQ_Final_Results_Journey_Recommendation_Paper_v*.md` (v1–v5) | ARCHIVE | All superseded. v6 is current. |

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
| `architecture/ADR-004-disease-specific-signal-evaluation.md` | SUPERSEDED | Superseded by ADR-005. |
| `architecture/ARCHITECTURE_GUARDRAILS.md` | AUTHORITATIVE | Enforceable rules. |
| `architecture/HEALTHIQ_REASONING_PIPELINE.md` | AUTHORITATIVE | Canonical pipeline model. |
| `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md` | SUPPORTING | Asset inventory. May undercount — KB has grown. |
| `docs/architecture/PHASE_0_AS_IS_ARCHITECTURE_AUDIT.md` | ARCHIVE | Pre-project baseline. |
| `docs/architecture/HealthIQ_Intelligence_Model_Design_Second_Pass.md` | SUPPORTING | Design workshop output. |
| `docs/ARCHITECTURE_INSIGHT_MODULARITY_REVIEW.md` | SUPPORTING | Modularity review. |
| `docs/ARCHITECTURE_REVIEW_REPORT.md` | STALE | Sprint 14 / October 2025. Superseded notice added. |
| `docs/DOCUMENTATION_HIERARCHY.md` | SUPERSEDED | Points to stale docs. Superseded notice added. Use `docs/README.md`. |

---

## Intelligence / Analysis Layer

| Document | Status | Notes |
|---|---|---|
| `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | AUTHORITATIVE | April 2026 technical audit. Code-grounded. |
| `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | AUTHORITATIVE | Coverage map. Renal and Wave 2 WHY gaps still open. |
| `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | AUTHORITATIVE | Wave 1 domain narrative contract. |
| `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | AUTHORITATIVE | Primary concern policy. |
| `docs/architecture/SIGNAL_ARCHITECTURE_COMPLETION_v1.0.md` | SUPPORTING | Signal architecture completion note. |
| `docs/Wave1-codebase-analysis_v3.md` | SUPPORTING | v3 is latest. |
| `docs/Wave1-codebase-analysis-v2.md` | SUPERSEDED | v3 supersedes. |
| `docs/investigations/2026-04-12_full_results_narrative_contract_inventory.md` | SUPPORTING | Narrative contract inventory. |
| `docs/investigations/2026-04-12_insulin_resistance_and_narrative_visibility_investigation.md` | SUPPORTING | IR narrative investigation. |
| `docs/investigations/2026-04-12_lab_range_fallback_policy_alignment.md` | SUPPORTING | Lab range fallback policy. |
| `docs/investigations/2026-04-12_results_why_narrative_runtime_investigation.md` | SUPPORTING | WHY narrative runtime investigation. |
| `docs/investigations/2026-04-21_N3_longitudinal_lab_value_contract.md` | SUPPORTING | Longitudinal lab value contract (N-3). |
| `docs/investigations/2026-04-26_D5_wave1_runtime_diagnosis.md` | SUPPORTING | D-5 runtime diagnosis. |
| `docs/investigations/KB-S*_PREFLIGHT.md` (many files) | ARCHIVE | KB sprint preflights. Historical record. |
| `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | AUTHORITATIVE | (See above.) |
| `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md` | SUPPORTING | VR primary concern ranking. |
| `backend/artifacts/intelligence_model_audit.md` | SUPPORTING | Intelligence model audit artifact. |
| `backend/artifacts/promoted_signal_intelligence_audit.md` | SUPPORTING | Promoted signal audit. |

---

## Frontend / UX

| Document | Status | Notes |
|---|---|---|
| `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | AUTHORITATIVE | Current results experience authority. |
| `docs/strategy/Interpretation_Display_Layer_Design_Lock.md` | AUTHORITATIVE | IDL design lock. |
| `docs/strategy/HealthIQ_IDL_Naming_Decision_Note_Approved.md` | AUTHORITATIVE | IDL naming. Approved and locked. |
| `docs/QUESTIONNAIRE_UX_REDESIGN_BACKGROUND.md` | AUTHORITATIVE | Q-1 background. |
| `docs/QUESTIONNAIRE_VISUAL_REDESIGN_Q2_BACKGROUND.md` | AUTHORITATIVE | Q-2 background. |
| `docs/CLAUDE_TRANSLATION_SPEC_v1.md` | SUPPORTING | Layer C translation spec. |
| `docs/clinician_language_style_guide_v1.md` | SUPPORTING | Clinical language style. |
| `docs/clinician_report_v1_spec.md` | SUPPORTING | Clinician report spec. |
| `docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md` | SUPPORTING | v5.2 design package. Results Journey Paper v6 is current authority. |
| `docs/architecture/Frontend/HealthIQ_Results_Wireframe_Package.md` | SUPPORTING | v5.2 wireframes. |
| `docs/context/UX_UI_GUIDE.md` | STALE | Pre-governance era. Superseded by Results Journey Paper v6. |
| `docs/Download-Arch/HealthIQ_Results_Page_UX_Design_Package_v*.md` (v1–v5) | ARCHIVE | Superseded versions. |
| `docs/Download-Arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` | SUPPORTING | Historical surface policy. Useful context. |
| `docs/Download-Arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v*.md` (v1–v2) | ARCHIVE | Superseded. |

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
| `docs/AUTOMATION_BUS_SOP_v1.3.1.md` | AUTHORITATIVE | Active SOP. |
| `docs/KNOWLEDGE_BUS_SOP_v1.3.md` | AUTHORITATIVE | Active Knowledge Bus SOP. |
| `docs/agents/CURSOR_OPERATING_POLICY.md` | AUTHORITATIVE | Cursor operating policy. |
| `AGENTS.md` | AUTHORITATIVE | Agent operating map. |
| `docs/AUTOMATION_BUS_SOP_v1.3.md` | SUPERSEDED | Superseded notice added. |
| `docs/AUTOMATION_BUS_SOP_v1.2.md` | SUPERSEDED | Superseded notice added. |
| `docs/KNOWLEDGE_BUS_SOP_v1.2.md` | SUPERSEDED | Superseded notice added. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.1.md` | ARCHIVE | Old version. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.2 (1).md` | ARCHIVE | Old version. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.3.1_aligned.md` | ARCHIVE | Draft/alignment variant. Not operative. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.3.1_final_merged.md` | ARCHIVE | Draft/merge variant. Not operative. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.3.1_stash_fix_patch.md` | ARCHIVE | Patch draft. Not operative. |
| `docs/Download-Arch/AUTOMATION_BUS_SOP_v1.3.2_draft.md` | ARCHIVE | Draft of a potential future version. Not operative. |
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
| `docs/compliance/DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md` | SUPPORTING | Phase 1 data flow. |
| `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` | UNCLEAR | Privacy review. April 2026 identified a GDPR gap on LLM parsing. Verify whether this document covers it. |
| `docs/product/WEDGE_EVENT_CONTRACT_AND_GOVERNANCE_PHASE1.md` | SUPPORTING | Wedge event contract. |

---

## Archive Directories

| Location | What it contains |
|---|---|
| `docs/archive/fix-reports/` | ~40 root-level incident/fix reports (2025). Historical record only. |
| `docs/Download-Arch/` | ~90 working papers, design explorations, superseded SOPs, strategy drafts. See `docs/Download-Arch/README.md`. |
| `docs/context/` | Pre-governance-era context files. Currency not verified. Use with caution. |
| `backend/artifacts/` | Golden run outputs, arbitration run outputs, audit artifacts. Operational history. |

---

## Documents With Unclear Status (Needs Leadership Review)

| Document | Why Unclear |
|---|---|
| `docs/HealthIQ_Phase1_Launch_Posture.md` | Not verified against April 2026 review findings. |
| `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` | April review found GDPR gap not covered by disclosure in upload flow. |
| `docs/testing/automated-testing-sentinel-repo-audit-report.md` | Possible duplicate of `healthiq_sentinel_repo_audit_v1.md`. |
| `docs/context/INTELLIGENCE_LIFECYCLE.md` + other context/ files | Pre-governance. Not verified for current accuracy. |
| `architecture/` — ADR-006 gap | ADR-007 and ADR-008 exist; ADR-006 does not. No explanation in index. |
