# HealthIQ AI – Product Requirements Document (PRD)

> **🎯 PURPOSE**: **SUPPORTING CONTEXT (Level 3)** - This document defines product requirements, features, and user experience goals. Use this for understanding the "what" and "why" behind feature development.

> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

## 1. Overview

**HealthIQ AI** is a precision biomarker intelligence platform that redefines the traditional blood report. It empowers individuals to explore, understand, and optimise their biology through clinical-grade analysis, network-level insights, and actionable behavioural recommendations — all delivered in a beautifully structured, shareable interface.

This is not a wellness coach. This is a precision tool for people who want to take control of their internal health landscape — and change it.

---

## 2. Core Value Proposition

- 🧬 **System-Aware Biomarker Intelligence**: Not just marker-by-marker commentary, but deeply interconnected insight based on systems biology and clinical logic.
- 🔍 **Root-Cause Correlation Engines**: Unrivalled analysis of how biomarkers influence each other, uncovering physiological stressors, dysregulation patterns, and compensation loops.
- 🧠 **Biomarker-to-Behaviour Bridge**: We don't stop at insight — we drive transformation. Every out-of-range marker triggers AI-generated lifestyle, supplement, or diet guidance, grounded in physiology and personal context.
- 📈 **Interpretability at a Glance**: Visual dials, grouped clusters, and dynamic UX make complexity accessible without simplification.
- 📤 **Designed for Sharing**: Beautiful, exportable summaries for users, clinicians, or health partners — readable, rational, and real.
- 🤖 **Built for Agents**: Fully modular context engineering structure that powers Cursor, LLM engines, or other AI workflows out-of-the-box.

---

## 3. Key Features

### Blood Panel Upload
Users upload a PDF or plaintext blood panel from any lab. We parse this using our configured LLM engine to extract biomarker values and reference ranges.
> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

### Canonicalisation Engine
All biomarkers are mapped to canonical IDs using our alias registry, and normalised into unified units and per-lab reference ranges. This ensures downstream scorers and clusters never handle aliases.

### Lifestyle Questionnaire
Users complete a structured lifestyle intake form capturing diet, sleep, stress, supplements, medical history, physical activity, and personal goals.

### Scoring Engine
Each biomarker is evaluated individually and in context of user lifestyle, using calibrated, version-controlled thresholds. We calculate out-of-range severity, directionality, and signal weight.

### Cluster-Based Insight Engine
We apply a proprietary set of cluster models that group markers into physiological systems: Metabolic, Cardiovascular, Inflammation, Hormonal, and Nutritional.

Within each cluster:
- Correlation engines analyse cross-marker relationships
- System health is inferred via weighted patterns
- Biological causes of dysfunction are hypothesised

Every insight ends with a "Next Step" — a behavioural intervention tailored to that specific dysfunction pattern.

### Behavioural Guidance Engine (LLM)
We use our configured LLM engine to generate:
- Personalised lifestyle changes
- Dietary suggestions
- Targeted supplement options

These are precise, not generic. Each suggestion is directly linked to the cluster or marker it's meant to address, and includes clinical reasoning.
> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

### Dashboard + Visualisations
We present biomarker dials grouped by cluster, showing:
- Actual value
- Normalised reference range
- Cluster summary
- Marker-specific commentary
- Risk flags, correlation notes, and suggestions

### Shareable Report Export
Users can export a PDF or JSON summary with dial snapshots, narrative interpretations, and action plans — shareable with doctors, health coaches, or friends.

---

## 4. User Personas

### 🧪 Preventive Health Seeker
- Wants early warning signs and lifestyle guidance
- We offer system-level clarity and clear next steps

### 🧠 Biohacker / Optimiser
- Seeks peak performance, longevity, and subtle gains
- We provide granular scoring, trends, and advanced markers

### 🧍‍♂️ Clinical User / Quantified Patient
- Has symptoms or chronic conditions, needs deeper pattern understanding
- We give medically informed insights and structural explanations

---

## 5. Functional Requirements

- ✅ File upload for blood test data (PDF or text)
- ✅ AI-powered parsing (LLM engine)
- ✅ Canonicalisation of biomarker IDs and ranges
- ✅ Lifestyle intake questionnaire (structured form)
- ✅ Scoring engine (versioned thresholds + weights)
- ✅ Cluster engine (correlation + compensation analysis)
- ✅ Behavioural suggestion engine (LLM)
- ✅ SSE streaming results to frontend
- ✅ Frontend dial components and insight cards
- ✅ Export to PDF and JSON

---

## 6. Technical Constraints

- **Backend**: FastAPI, Pydantic v2, SQLAlchemy, Supabase, Redis
- **Frontend**: Next.js 14+, App Router, Tailwind, TypeScript, Zustand, TanStack Query, D3
- **Analysis**: Modular Python insight engine with DTOs
- **ORM**: SQLAlchemy for database interactions with Supabase PostgreSQL
- **Data**: YAML (SSOT) for biomarker alias mapping and canonical reference ranges
- **Agent Support**: Cursor + LLM workflows with structured context files
- **Streaming**: Server-Sent Events (SSE) for streaming responses
- **CI/CD**: GitHub Actions with black + ruff + mypy linters
- **Lovable Integration**: Lovable mock-ups are captured as static HTML drafts in `/frontend/_drafts/lovable/` and converted to production Next.js components by Cursor. Lovable cannot run Next.js directly and produces only Vite/React previews that require manual conversion.

---

## 7. Insight Engine Architecture

The platform is built as a pipeline:
> `Scorer → Cluster Inference → Insight Engine → LLM Narrator → DTO → Frontend`

Each module is stateless, version-controlled, and independently testable. Context is passed as structured DTOs between modules.

---

## 8. Future Scope

- Longitudinal biomarker tracking
- API integrations with testing providers
- User goal tracking and follow-up reminders
- Clinical provider dashboard
- Historical comparison reports
- Comorbidity-aware scoring weights
- Wearable and lifestyle integrations (HRV, sleep, etc.)

---

## 9. Out of Scope

- Live doctor chat
- Medical diagnosis or prescription
- Insurance integration
- Wearable device distribution

---

## 10. Metrics of Success

- 🧠 % of users who understand their bloodwork more clearly (UX survey)
- 🧪 # of biomarkers with recommended actions
- ⬇️ # of red/yellow markers over time (longitudinal success)
- 🔁 Conversion rate from free report → paid insight bundle
- 💬 Time to first actionable recommendation
- 📤 Share/export rate

---

## 11. Why We Win

HealthIQ AI delivers:
- A blood report people **actually understand**
- Root-cause inference that clinicians can trust
- A gorgeous UX for humans — not just for graphs
- An agent-ready file structure for true AI collaboration

In a market flooded with surface-level summaries, we go deeper — and bring clarity with us.

---

