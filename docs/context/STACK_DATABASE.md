# 🗄️ STACK_DATABASE.md

> This document describes the chosen database technologies and schema strategy for HealthIQ-AI v5. It covers the reasons for selecting each technology, our SSOT philosophy, the separation of analytical vs user state, and how we manage biomarker intelligence at scale.

---

## 🔧 Database Technologies

### 1. **PostgreSQL (via Supabase)**
- **Use Case**: Structured relational data (users, uploads, analyses, subscriptions)
- **Justification**:
  - SQL robustness with JSONB flexibility
  - Tight Supabase integration with auth, storage, row-level security
  - Compatible with serverless functions and edge deployments

### ORM Layer

We use **SQLAlchemy** for interacting with the Supabase PostgreSQL database.  
All models are structured around frozen Pydantic DTOs.  
We do **not** use SQLModel or Supabase's built-in ORM layers (e.g. PostgREST) at this time.

### 2. **YAML (SSOT data files)**
- **Use Case**: Version-controlled biomarker truth definitions
- **Justification**:
  - Git-friendly, fully human-readable
  - Enables clinical audit trail of reference ranges, aliases, units
  - Used by canonical normalisation engine as truth layer

### 3. **Redis (optional, future)**
- **Use Case**: Transient state, task queues, SSE event streaming
- **Justification**:
  - Low-latency caching of parsed panels
  - Temporary payload storage between pipeline steps
  - Scalable pub/sub model for real-time UX updates


---

## 📁 Data Layer Structure

| Layer | Type | Purpose |
|-------|------|---------|
| **Supabase (Postgres)** | Relational DB | User uploads, logs, pipeline runs, feature flags |
| **SSOT YAML Files** | Immutable files | Canonical biomarkers, aliases, units, ranges |
| **Redis (Future)** | In-memory | Orchestration memory + performance layer |


---

## 🧬 SSOT (Single Source of Truth)

- Located in: `ssot/biomarkers.yaml`, `units.yaml`, `ranges.yaml`
- Maintains the **canonical IDs**, aliases, reference values
- Used exclusively in:
  - Normalisation engine
  - Scoring thresholds
  - UI visual range mapping

**No downstream module may override SSOT values.**

---

## 🔄 Key Tables in Supabase

| Table | Description |
|-------|-------------|
| `users` | Auth-managed user profile and tier |
| `uploads` | Raw file or text data from users |
| `lifestyle_answers` | Structured questionnaire results |
| `parsed_panels` | Output of LLM parsing step |
| `canonical_panels` | Normalised biomarkers (Step 3) |
| `engine_results` | Output of all engines run per user |
| `insight_payloads` | LLM narrative outputs |
| `recommendations` | Behavioural, supplement, diet actions |
| `audit_log` | Transformation history (planned) |

---

## 🔐 Security Considerations

- `.env` loaded Supabase service key with row-level security
- No YAML truth data is user-writeable
- Deletion logic respects GDPR-style full deletion
- `insight_payloads` and `engine_results` are versioned

---

## 🧠 Future Enhancements

| Area | Plan |
|------|------|
| **Versioning** | Maintain `ssot_versions/` and link to each analysis |
| **Analytics DB** | Move usage and cohort trends to a time-series warehouse |
| **Clinical Layer** | Add ICD-10 + LOINC + SNOMED CT support for each biomarker |
| **Data Export** | FHIR bundles, PDF report archive |

---

## ✅ Summary

The database stack separates transient orchestration state from long-lived user and analysis records. It enforces a strict canonical biomarker model via SSOT YAMLs, while offering flexible scaling and real-time interaction through Postgres and Redis. This architecture ensures auditability, extensibility, and regulatory readiness from the ground up.

