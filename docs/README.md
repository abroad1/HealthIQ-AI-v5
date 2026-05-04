# HealthIQ AI — Documentation Entry Point

**Last updated:** 2026-05-04  
**Status:** LIVE — this is the authoritative navigation document.

Start here. This file points you to the correct document for each topic.  
If a document is not listed here as current, it is either reference-only or archive.

---

## Current State — Start Here

| What you want to understand | Document |
|---|---|
| What the product really is today — honest ledger | `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` |
| What the three engine bugs were and where they live in code | `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` |
| What analytical signals are covered and what is missing | `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` |
| What the current quality layer covers (Sentinel Phase 1) | `docs/testing/healthiq_sentinel_phase1_implementation_report.md` |
| What sprints have been done and what is active now | `docs/SPRINT_STATUS.md` |

---

## Strategy

| Document | Status | Notes |
|---|---|---|
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | **AUTHORITATIVE** | Master strategic record for Phase 1. Read alongside the April 2026 reset. |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` | **AUTHORITATIVE** | First-market addendum. Read alongside the parent. |
| `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` | **AUTHORITATIVE — current truth** | April 2026 full product review. Most honest state-of-truth document. |
| `docs/RESET_SPRINT_PLAN_2026-04.md` | **AUTHORITATIVE — completed plan** | The 8-sprint reset plan. All sprints now complete. See `docs/SPRINT_STATUS.md`. |
| `docs/strategy/HealthIQ_Strategy_Stack_Document_Authority_Map.md` | **SUPPORTING** | Governance note on how strategy documents relate. |
| `docs/strategy/HealthIQ_Executive_GTM_Report_Updated_v2.md` | **SUPPORTING** | GTM positioning context. |
| `docs/HealthIQ_Phase1_Launch_Posture.md` | **SUPPORTING** | Phase 1 launch posture. Currency uncertain — verify against April review. |
| Earlier strategy versions (v1.4, all v1.5 drafts) | **SUPERSEDED** | See `docs/archive/working-papers/download-arch/` |

---

## Architecture

| Document | Status | Notes |
|---|---|---|
| `architecture/ARCHITECTURE_INDEX.md` | **AUTHORITATIVE** | ADR registry — the constitutional record. Start here for architecture. |
| `architecture/ADR-001-platform-non-negotiables.md` | **AUTHORITATIVE** | Binding governance invariants. Non-negotiable constraints. |
| `architecture/ADR-002-deterministic-analysis-engine.md` | **AUTHORITATIVE** | Three-layer architecture definition. |
| `architecture/ADR-003-knowledge-bus-architecture.md` | **AUTHORITATIVE** | Knowledge Bus evidence architecture. |
| `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | **AUTHORITATIVE** | Active signal evaluation architecture (supersedes ADR-004). |
| `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` | **AUTHORITATIVE** | Promoted signal intelligence contract. |
| `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` | **AUTHORITATIVE** | Root-cause WHY architecture. |
| `architecture/ARCHITECTURE_GUARDRAILS.md` | **AUTHORITATIVE** | Enforceable rules derived from ADRs. |
| `architecture/HEALTHIQ_REASONING_PIPELINE.md` | **AUTHORITATIVE** | Canonical Evidence → Signal → Insight model. |
| `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md` | **SUPPORTING** | Asset inventory at v5.2 baseline. May undercount — KB has grown since. |
| `docs/archive/superseded/ARCHITECTURE_REVIEW_REPORT.md` | **STALE — do not use** | Sprint 14 / October 2025. Moved to archive. |

---

## Intelligence / Analysis Layer

| Document | Status | Notes |
|---|---|---|
| `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | **AUTHORITATIVE — current truth** | April 2026. Code-grounded. Named the engine bugs with file/line citations. |
| `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | **AUTHORITATIVE** | Analytical coverage map. WHY gaps documented here remain partially unresolved (WHY Wave 1 done; Wave 2 not yet started). |
| `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | **AUTHORITATIVE** | Active contract for Wave 1 domain narrative structure. |
| `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | **AUTHORITATIVE** | Policy for primary concern and ranked ambiguity. |
| `docs/Wave1-codebase-analysis_v3.md` | **SUPPORTING** | Wave 1 implementation analysis. v3 is latest. |
| `docs/investigations/2026-04-12_*.md` | **SUPPORTING** | April 2026 investigation notes (4 files). Operational reference. |
| `docs/archive/sprint-history/investigations/` | **ARCHIVE** | ~30 sprint preflight investigations (KB-S*, FE_*, BE_S1, etc.). Historical record only. |

---

## Frontend / UX

| Document | Status | Notes |
|---|---|---|
| `docs/strategy/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | **AUTHORITATIVE** | Results page experience authority. v6 is current. |
| `docs/strategy/Interpretation_Display_Layer_Design_Lock.md` | **AUTHORITATIVE** | IDL design lock. |
| `docs/strategy/HealthIQ_IDL_Naming_Decision_Note_Approved.md` | **AUTHORITATIVE** | IDL naming decision. Approved and locked. |
| `docs/QUESTIONNAIRE_UX_REDESIGN_BACKGROUND.md` | **AUTHORITATIVE** | Q-1 questionnaire redesign background. |
| `docs/QUESTIONNAIRE_VISUAL_REDESIGN_Q2_BACKGROUND.md` | **AUTHORITATIVE** | Q-2 premium visual layer background. |
| `docs/CLAUDE_TRANSLATION_SPEC_v1.md` | **SUPPORTING** | Translation spec for Layer C narrative. |
| `docs/clinician_language_style_guide_v1.md` | **SUPPORTING** | Clinical language style. |
| `docs/archive/sprint-history/context/UX_UI_GUIDE.md` | **ARCHIVE** | Pre-governance era. Superseded by Results Journey Paper v6. Moved to archive. |

---

## Testing / Quality

| Document | Status | Notes |
|---|---|---|
| `docs/testing/healthiq_sentinel_phase1_implementation_report.md` | **AUTHORITATIVE — current quality truth** | 2026-05-03. 32/32 regression tests pass. Clearly states Phase 2+ gaps. |
| `docs/testing/brief for HealthIQ AI Phase 1 Sentinel.md` | **AUTHORITATIVE** | Sentinel Phase 1 scope definition. |
| `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` | **SUPPORTING** | Testing operating model philosophy. |
| `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md` | **SUPPORTING** | Background for agentic testing strategy. |
| `docs/testing/UAT1/UAT1_findings.md` | **SUPPORTING — historical** | UAT1 findings. Date uncertain. |
| `docs/testing/healthiq_sentinel_repo_audit_v1.md` | **SUPPORTING** | Repo audit preceding Sentinel implementation. |

---

## Governance / Control-Plane

| Document | Status | Notes |
|---|---|---|
| `.claude/CLAUDE.md` | **AUTHORITATIVE — always current** | Permanent context. Actively maintained. Read first for agent roles and non-negotiables. |
| `docs/AUTOMATION_BUS_SOP_v1.3.1.md` | **AUTHORITATIVE — ACTIVE SOP** | Operative governance SOP. |
| `docs/KNOWLEDGE_BUS_SOP_v1.3.md` | **AUTHORITATIVE — ACTIVE SOP** | Operative Knowledge Bus SOP. |
| `docs/agents/CURSOR_OPERATING_POLICY.md` | **AUTHORITATIVE** | Cursor operating policy within the bus. |
| `AGENTS.md` | **AUTHORITATIVE** | Agent operating map. |
| `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.3.md` | **SUPERSEDED** | Moved to archive. |
| `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.2.md` | **SUPERSEDED** | Moved to archive. |
| `docs/archive/superseded/KNOWLEDGE_BUS_SOP_v1.2.md` | **SUPERSEDED** | Moved to archive. |

---

## GTM / Launch / Ops

| Document | Status | Notes |
|---|---|---|
| `docs/ops/OPEN_ITEMS_AND_PHASE1_BOUNDARIES.md` | **SUPPORTING** | Phase 1 open items and scope boundaries. |
| `docs/ops/OPERATIONAL_CONTROLS_BASELINE_PHASE1.md` | **SUPPORTING** | Operational controls baseline. |
| `docs/ops/UK_HOSTING_AND_RESIDENCY_PHASE1.md` | **SUPPORTING** | UK hosting posture. |
| `docs/compliance/DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md` | **SUPPORTING** | Phase 1 data flow compliance. |
| `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` | **SUPPORTING** | Privacy risk review. Note: April 2026 review identified a GDPR gap on LLM parsing disclosure — verify whether this document addresses it. |

---

## Navigation Rules

- **For current product truth:** start with `docs/CURRENT_STATE_PACK.md`
- **For sprint status:** `docs/SPRINT_STATUS.md`
- **For architecture constraints:** `architecture/ARCHITECTURE_INDEX.md`
- **For governance/SOPs:** `docs/AUTOMATION_BUS_SOP_v1.3.1.md` and `docs/KNOWLEDGE_BUS_SOP_v1.3.md`
- **For document authority classification:** `docs/AUTHORITY_MAP.md`
- **For settled decisions:** `docs/DECISION_REGISTER.md`
- **For archive material:** `docs/archive/` — see `docs/archive/README.md` for structure

---

## What Not to Use for Navigation

| Document | Why |
|---|---|
| `docs/archive/superseded/DOCUMENTATION_HIERARCHY.md` | SUPERSEDED — pointed to stale Sprint 14 documents. Moved to archive. |
| `docs/archive/superseded/ARCHITECTURE_REVIEW_REPORT.md` | STALE — Sprint 14 / October 2025. Moved to archive. |
| `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.2.md` / `v1.3.md` | SUPERSEDED — use v1.3.1. Moved to archive. |
| `docs/archive/superseded/KNOWLEDGE_BUS_SOP_v1.2.md` | SUPERSEDED — use v1.3. Moved to archive. |
| Anything in `docs/archive/working-papers/download-arch/` | Working papers archive (~90 files) |
| Anything in `docs/archive/` | Historical archive — see `docs/archive/README.md` |
