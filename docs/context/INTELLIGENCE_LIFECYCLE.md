# 🧠 HealthIQ-AI Intelligence Lifecycle

> **Note:** This document describes the full end-to-end intelligence lifecycle across both frontend and backend layers. For backend execution stages only, refer to `STACK_BACKEND.md`.

> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

> This document defines the **full end-to-end intelligence lifecycle** of the HealthIQ-AI platform. It includes both backend and frontend responsibilities and serves as the central reference for all 10 lifecycle stages.

> This document describes the end-to-end journey of biomarker data through the HealthIQ-AI v5 architecture. It defines how raw inputs are transformed into personalised, clinically informed insights, and how each component contributes to data integrity, extensibility, and intelligent UX.


---

## 🚀 Overview: Core Stages

| Stage | Description |
|-------|-------------|
| **1. User Input** | User uploads a lab report and completes lifestyle questionnaire |
| **2. Parsing** | Extract biomarkers, units, ranges via Gemini-powered parsing |
| **3. Canonical Normalisation** | Map aliases to canonical IDs, apply reference ranges, units |
| **3.5. Data Completeness Gate** | Assess sufficiency for analysis, flag gaps, assign confidence |
| **4. Orchestration & Engine Dispatch** | Determine which engines to run based on user tier and biomarker set |
| **5. Engine Execution** | Score biomarkers, clusters, systems (e.g. metabolic, inflammation) |
| **6. Insight Synthesis** | Generate natural language narratives and summaries via Gemini |
| **7. Visualisation** | Render dials, clusters, timelines, risk zones, summaries |
| **8. Recommendations** | Provide behavioural, dietary, or supplement advice (Gemini-driven) |
| **9. Delivery & Feedback** | Return results, export options, track outcomes, trigger retests |
| **10. Integrations & APIs** | Future EHR, wearables, telehealth, and 3rd-party services |

---

## 🔍 Detailed Stage Descriptions

### 1. **User Input**
- **Lab Upload**: PDF, HTML, text
- **Questionnaire**: Age, sex, lifestyle, symptoms
- **Entry Point**: `/upload` page + API

### 2. **Parsing**
- **Gemini Extractor**: This stage is powered by Google Gemini
- **Output**: `RawBiomarkerExtraction[]`
- **Edge Handling**: OCR fuzziness, multi-marker lines

### 3. **Canonical Normalisation**
- **Maps**: Aliases → Canonical IDs (e.g., "ALT" → `alanine_transaminase`)
- **Adds**: Units, population-specific ranges, biomarker metadata
- **Enforced by**: `normalize.py`, `ssot/*.yaml`

### 3.5. **Data Completeness Assessment** ✅
- **Checks for**:
  - Missing key biomarkers
  - Red flags (e.g. low WBC + missing CRP)
  - Compatibility with engine thresholds
- **Confidence Score Assigned**
- **Gating logic**: Partial analysis fallback

### 4. **Pipeline Orchestration**
- **Engine Selector**: Chooses which engines to run
- **Based on**:
  - Biomarkers present
  - Subscription tier (e.g. Premium → 20+ engines)
  - User type (biohacker, lifestyle, clinical)
- **Extensibility**: Plugin registry, version control

### 5. **Engine Execution**
- **Examples**:
  - Metabolic Age Engine
  - Cardiovascular Resilience Engine
  - Fatigue Root Cause Engine
- **Output**:
  - Score (numeric or categorical)
  - Flags (e.g. driver biomarkers)
  - Confidence score

### 6. **Insight Synthesis**
- **Gemini Layer**: This stage is powered by Google Gemini
- **Payload**: All engine + cluster outputs, user profile, questionnaire
- **Prompt Templating**: Ensures safe, scoped, factual summaries
- **Output**:
  - System narratives (e.g., "Your liver markers suggest...")  
  - Individual biomarker synthesis

### 7. **Visualisation**
- **Components**:
  - Holographic Dials
  - Cluster Networks
  - Trendlines
  - Risk Zones + Scorecards
- **User Interactions**:
  - Hover + expand
  - Save to profile
  - Export PDF

### 8. **Behavioural Recommendations**
- **Sources**: This stage is powered by Gemini (Google AI) + Rules + Biomarker states
- **Types**:
  - Food and supplements
  - Sleep, stress, hydration
  - Diagnostic retesting
- **Confidence + Justification** included

### 9. **Delivery & Feedback**
- **User sees**:
  - Summary + engine-level detail
  - Visualisation dashboard
  - Recommendation call-to-action
- **Re-test triggers**
- **Email alerts + exports (planned)**

### 10. **Integrations (Future)**
- EHR via FHIR
- Apple/Google HealthKit
- Wearables (e.g. HRV, glucose monitors)
- Supplements API
- Telehealth partners

---

## 🧬 Structural Guarantees

- All biomarker data converted to **canonical-only format** before scoring
- Every stage emits an **immutable DTO**, validated by `pydantic v2`
- No engine or synthesis logic permitted to use aliases or fuzzy data
- All insight payloads are **versioned and traceable**

---

## 🔁 Built-In Safeguards (Architecture Hooks)

| Area | Safeguard |
|------|-----------|
| **Data Integrity** | Audit trail of all transformations |
| **Error Handling** | Graceful degradation, retry logic, error classification |
| **Confidence Flow** | Propagation of uncertainty from parse → score → insight |
| **Engine Expansion** | Plugin system, feature flags, custom pipelines |
| **Result QA** | Validation, contradiction detection, threshold sanity check |
| **Compliance** | GDPR-ready retention + opt-out framework |

---

## 🧠 Next Steps
- Integrate this file into orchestrator context packs
- Reference this lifecycle in all engine and insight README files
- Use this structure to define engine contract interfaces

---

This document will evolve as we add engine variants, premium tiers, and clinical-grade regulatory scaffolding.

