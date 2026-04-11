# Privacy risk review — Phase 1 (DPIA-equivalent)

**Document type:** Internal structured privacy impact assessment aligned with UK GDPR expectations for processing special-category (health) data.  
**Not:** A regulator-submitted statutory DPIA unless legal elevates it.  
**Product model:** UK-first B2C; blood-result upload; structured interpretation; clinician-style downloadable output; non-diagnostic positioning.

---

## 1. Controller and scope

| Field | Phase 1 position |
|-------|------------------|
| **Controller** | The operating company offering HealthIQ (name/entity to be stated in Privacy notice / contracts). |
| **Processing scope** | Accounts, health-related inputs (lab results, questionnaire), derived analysis, insight/narrative outputs, audit/consent/deletion hooks per schema. |
| **Lawful basis (indicative)** | **Special category:** explicit consent / explicit policy + health care management patterns — **must be confirmed** by legal for live terms and Privacy notice. This document does not replace legal sign-off. |

---

## 2. Description of processing

| Stage | What happens | Data involved |
|-------|----------------|---------------|
| Registration / login | Identity via Supabase-auth pattern; JWT session (`SecurityConfig` in settings) | Email, credentials (handled by auth provider), profile linkage |
| Upload / ingestion | User provides lab data (file or paste); parsing and analysis pipeline | Raw biomarker data, optional questionnaire JSON |
| Analysis persistence | SQLAlchemy models store analyses and results (`Analysis`, `AnalysisResult`, etc. in `backend/core/models/database.py`) | Health data, scores, clusters, recommendations text |
| Insight / narrative (optional path) | When configured, Gemini may generate or refine text (`core/insights/synthesis.py` pathway) | Derived health context in prompts/responses — **vendor processing** |
| Export / clinician report | User may generate downloadable material (product-dependent); storage bucket name in config | Health summary content |
| Rights / erasure hooks | Schema includes `DeletionRequest`, `Consent`, `AuditLog` relationships to `Profile` | Metadata supporting GDPR requests — **operational SLAs** still required |

---

## 3. Necessity and proportionality

- **Necessity:** Processing health data is **core** to the product’s stated purpose (interpretation of supplied results), not ancillary surveillance.
- **Proportionality:** Retention, access, and third-party exposure should be **minimised** to what is needed for service delivery; Gemini use should follow **data minimisation** practices in prompts (implementation detail — separate hardening).

---

## 4. Risk assessment (summary)

| Risk area | Description | Existing mitigations (repo / design) | Residual / open items |
|-----------|-------------|----------------------------------------|-------------------------|
| **R1 Confidentiality** | Unauthorized access to health data | TLS patterns expected in deployment; JWT auth; RBAC expectation per posture | Production access reviews, key rotation, penetration test scope — **ops** |
| **R2 Subprocessor exposure** | Gemini / Supabase process data outside direct control | Vendor DPAs and region choices | **Verify** regions and SCCs/IDTAs with legal |
| **R3 Integrity** | Tampering with results | Deterministic pipeline emphasis in product; versioned analysis | Change-management for models/rules |
| **R4 Availability** | Loss of data | Posture expects backup/recovery — **see** `docs/ops/OPERATIONAL_CONTROLS_BASELINE_PHASE1.md` | **Documented backup/restore drills not in repo** |
| **R5 Transparency** | Users unclear on use of data | Privacy / Terms / Contact (OPS-S1A); this OPS-S1B pack | Keep UX copy aligned with actual processing |
| **R6 Automated decision-making** | User assumes medical decision | Product copy: non-diagnostic; clinician discussion framing | Ongoing UX review |

---

## 5. Mitigations (operational)

- Consent and deletion **fields** exist at schema level; **process** for honoring requests within SLA must be owned by ops/legal.
- Incident response and breach notification: **baseline** in ops docs; **playbooks** must be exercised.

---

## 6. Sign-off placeholder

| Role | Name | Date | Notes |
|------|------|------|-------|
| Privacy / Legal | *TBD* | | Required before external claims |
| Security / Ops | *TBD* | | Confirms production controls |
| Product | *TBD* | | Confirms UX alignment |

---

## 7. Review cadence

Revisit when: new subprocessors, new data categories, cross-border changes, or major model/pipeline changes.
