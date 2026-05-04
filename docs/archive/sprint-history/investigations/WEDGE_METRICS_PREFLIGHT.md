# Wedge metrics / launch instrumentation — preflight (read-only)

**work_id:** WEDGE-METRICS-PREFLIGHT  
**mode:** READ_ONLY investigation  
**date:** 2026-04-11  
**Authority:** `docs/HealthIQ_Phase1_Launch_Posture.md`, `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md`, repo evidence below  

---

## 1. Executive summary

| Question | Finding |
|----------|---------|
| **What measurement capability already exists?** | **No** dedicated product analytics SDK or event pipeline in `frontend/app` (no PostHog/Mixpanel/GA4/plausible-style integration found). Funnel behaviour is **only** indirectly inferable via existing APIs and persistence (e.g. analyses per user in DB) if someone runs **adhoc SQL or log queries** — not first-class product metrics. `analysisStore` uses `console.log` / `console.debug` for dev-style tracing, not structured telemetry. `ReportsService` (`frontend/app/services/reports.ts`) exists with download/history helpers but is **not** wired into the main results UX path audited here; results export is **client-side JSON** + optional **Web Share / clipboard** (`frontend/app/(app)/results/page.tsx`). |
| **What is missing?** | Named **bridge metrics** from the launch posture (paid conversion, repeat upload, retention, clinician report download/carry-through, segment splits, trust signals) have **no** consistent event schema, **no** collector, **no** dashboard. **Paid** conversion is **unmeasurable in-product** today: **no** Stripe/billing/subscription references in `frontend/app`. **Segment** (standard retail vs technical/biohacker) is **not** captured as a dedicated user attribute in code reviewed; questionnaire data exists in analysis flow but **no** explicit segment enum for analytics. |
| **Is wedge-metrics work justified now?** | **Yes.** The first-market addendum explicitly sequences **“Sprint 3 — Wedge metrics / launch instrumentation”** after OPS-S1A/S1B. OPS-S1 preflight §3.5 and `docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md` already state instrumentation is deferred and recommend **event contract + privacy alignment** before implementation. Strategy requires the B2C wedge to be **measured**, not assumed. |

---

## 2. Strategy interpretation (sources: posture + first-market addendum)

### 2.1 What the B2C wedge must prove

From `docs/HealthIQ_Phase1_Launch_Posture.md` §318–331, Phase 1 must show the wedge creates:

- real user demand and willingness to pay  
- repeat usage  
- trust in outputs  
- **clinician exposure** via report carry-through  
- **credible** signals for later B2B / enterprise conversations  

B2C is explicitly a **data, proof, product-learning, and messaging engine**, not a holding pattern (§59–74).

### 2.2 Bridge metrics that matter most

From §335–372, **early** tracking should include at minimum:

- paid conversion, repeat upload/panel rate, retention  
- clinician report **download** rate, **carry-through** rate  
- self-reported: discussed with clinician; improved conversation  
- user-rated usefulness / trust  
- **Product proof:** narrative engagement, clinician report usage **by segment**, longitudinal usage, signal density, **segment-level** differences  

### 2.3 Two B2C segments and measurement

Posture §110–149 and addendum §31–43: **standard retail** vs **technical / biohacker** need **separate** comparison where possible (§360–371): conversion, repeat upload, retention, report usage, trust by segment.

**Repo implication:** There is **no** evidence of a persisted `user_segment` (or equivalent) on `Profile` / auth for analytics; segment discrimination for **measurement** is **not** implemented.

### 2.4 Clinician report in the measurement model

Strategy (addendum §52–65): downloadable clinician report is a **secondary distribution channel** — indirect clinician exposure and proof for later B2B.

**Repo:** Clinician narrative is rendered in-app via `ClinicianReportRenderer` on `frontend/app/(app)/results/page.tsx`. “Export” in the same file is **JSON export** (`handleExportResults`) and **share URL** (`handleShareResults`), not necessarily a distinct “PDF clinician pack” download event. **Server-side** `ReportsService.downloadReport` may not reflect live user journeys until confirmed wired.

Measurement should treat **view**, **export/share**, and any **future PDF/server download** as **distinct** events if product defines them.

### 2.5 What this sprint unlocks

**Sprint 3** in the addendum (§163+) is meant to make the launch **measurable** as a deliberate wedge. Without instrumentation, bridge metrics in the posture remain **aspirational**.

---

## 3. Current instrumentation audit

### 3.1 Present

| Area | Evidence |
|------|----------|
| **Journey plumbing** | Auth (`authStore`, `AuthService`), upload (`upload/page.tsx`, `upload` store, parsing), analysis (`analysisStore.startAnalysis`), results (`results/page.tsx`), history API (`useHistory`, `AnalysisService.getAnalysisHistory`), reopen route `frontend/app/(app)/analysis/[id]/page.tsx` → redirect to `/results?analysis_id=`. |
| **Persistence** | Backend models store analyses, results, profiles (enables **batch** metrics if queried). |
| **Compliance-oriented audit table** | `audit_logs` migration / `AuditLog` model — **security/compliance** audit trail, **not** product funnel analytics unless explicitly written for product events. |
| **Governance docs** | `docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md`, OPS-S1 preflight §3.5 acknowledge gap. |

### 3.2 Partial

| Area | Evidence |
|------|----------|
| **“Download” behaviour** | Results page triggers **client JSON download** and **share**; meaning of “clinician report download rate” vs **JSON export** must be defined. |
| **Repeat behaviour** | Repeat uploads **can** be derived **server-side** from analysis counts per `user_id` **if** queries exist; **not** exposed as metrics product. |
| **Reopen** | `/results?analysis_id=` + analysis redirect — measurable once events exist. |

### 3.3 Missing

| Area | Evidence |
|------|----------|
| **Product analytics SDK / pipeline** | No matches for common vendors in `frontend/app` application code; OPS-S1 preflight §3.5 confirms. |
| **Payment / subscription** | `grep` over `frontend/app` for stripe/billing/subscription/payment/checkout: **no matches** — **paid conversion** not instrumentable in-app until commerce exists or proxy defined (e.g. manual cohort). |
| **Segment dimension** | No standard-vs-biohacker field for analytics identified in auth/profile flows reviewed. |
| **Structured product events** | No shared `track()` / event envelope; only ad-hoc `console` in store. |
| **Trust / NPS / in-app surveys** | No dedicated trust/usefulness capture UI found in this audit. |
| **Clinician carry-through** | Posture asks % who **discussed** report with clinician — requires **survey** or external study; not in repo. |

---

## 4. Metric-by-metric readiness

Legend: **Now** = measurable today with minimal work (e.g. server logs/DB only); **Bounded** = needs small, defined implementation; **Blocked** = depends on missing product/business pieces.

| Metric | Current status | Implementation complexity | Next-sprint fit? |
|--------|----------------|----------------------------|------------------|
| Registration completion | **Missing** client/server events | **Bounded** (event on success/fail) | Yes |
| Login success / failure | **Missing** product events | **Bounded** | Yes |
| Upload start | **Missing** explicit event | **Bounded** (upload page + store) | Yes |
| Upload complete / parse success | **Partial** (state transitions); no metric | **Bounded** | Yes |
| Analysis start | **Partial** (`startAnalysis` called); no metric | **Bounded** | Yes |
| Analysis success / fail | **Partial** (store + API outcome); no metric | **Bounded** | Yes |
| Results viewed | **Partial** (page load with analysis); no event | **Bounded** | Yes |
| Clinician report **viewed** (tab/render) | **Partial** (UI exists); no distinct event | **Bounded** (tab open / render) | Yes |
| Clinician report **downloaded** | **Ambiguous** — JSON export vs future PDF | **Bounded** after definition | Yes, once defined |
| Historical result reopened | **Partial** — route + fetch; no event | **Bounded** | Yes |
| Repeat upload / repeat panel | **Now** *in principle* via DB aggregation per user | **Bounded** to automate reporting | Yes (prefer server-side aggregate + optional client beacon) |
| Retention / return usage | **Now** *in principle* via session/login timestamps if stored | **Bounded** | Yes |
| Segment split (retail vs biohacker) | **Missing** dimension | **Bounded** to **high** — needs product definition + capture | Yes, but **depends on segment definition** |
| Trust / usefulness signals | **Missing** | **Bounded** (in-app micro-survey or link-out) | Optional phase |
| Enterprise-relevant proof (B2C-derived) | **Indirect** — needs narrative + metrics package | **Not** a single event; **out of scope** for pure instrumentation | Defer to GTM/analyst |

---

## 5. Data / privacy boundary (UK B2C)

| Topic | Assessment |
|-------|------------|
| **Existing constraints** | OPS-S1B adds subprocessor inventory and data-flow docs; Privacy/Terms exist (OPS-S1A). Any **new** analytics vendor is a **new subprocessor** — must update `docs/ops/VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md` and Privacy notice. |
| **Special-category data** | Events must **avoid** sending raw biomarkers/health payloads to third-party analytics where possible; prefer **aggregated IDs**, hashed user id, and **event names** only. |
| **Segment** | Storing “biohacker vs retail” may be sensitive; needs **lawful basis** and transparency in Privacy notice. |
| **Consent** | Non-essential analytics may need **consent** gating per UK GDPR/ePrivacy practice — coordinate with legal; **do not** improvise in product without alignment. |
| **Coordination with OPS baseline** | Event contract + vendor choice should be **documented** before wide implementation (per `WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md`). |

**Phase 1 proportionate approach:** Minimum **first-party** or **privacy-reviewed** third-party events; clear retention; no full BI warehouse.

---

## 6. Best implementation shape

**Recommendation:** **SPLIT_INTO_EVENT_CONTRACT_AND_INSTRUMENTATION_PHASES**

| Phase | Deliverable |
|-------|-------------|
| **A — Event contract & governance** | Named event vocabulary (e.g. `auth_login_success`, `upload_started`, `analysis_completed`, `results_viewed`, `clinician_report_viewed`, `export_json_clicked`, `share_clicked`), PII rules, consent placement, vendor choice (or first-party API logging), update subprocessor inventory + Privacy cross-links. |
| **B — Instrumentation implementation** | FE hooks at `authStore`, upload, `analysisStore`, `results/page`, history/reopen; optional BE middleware or audit stream for server-truth duplicates; **no** change to analytical reasoning. |

**Rationale:** Repo has **zero** event schema; OPS-S1B explicitly deferred vendor choice. Implementing SDK before contract risks rework. **Paid conversion** remains **blocked** on payments unless scope explicitly adds **proxy metrics** (e.g. “checkout started” placeholder).

**Alternative (acceptable):** One **bounded** sprint **WEDGE-METRICS** with **two sequential milestones** (contract week 1, code week 2) under a single `work_id` — still **split logically**, single PM surface.

---

## 7. Boundary check — out of scope for wedge-metrics sprint

Keep **out** unless explicitly approved:

- Full **BI/warehouse** programme  
- Broad **experimentation platform** (A/B infra)  
- **Enterprise** analytics tooling  
- Major **pricing/billing** implementation (but **define** how paid conversion will be measured when billing lands)  
- **Data-science** reporting layer  
- **Backend reasoning / InsightGraph / pipeline** behaviour changes  
- **Generic logging** not tied to named wedge metrics  
- Reopening **launch posture** strategy  

---

## 8. Likely touched surfaces (for future sprint authoring)

| Surface | Why |
|---------|-----|
| `frontend/app/state/authStore.ts`, `(auth)/login`, `register` | Auth funnel |
| `frontend/app/(app)/upload/page.tsx`, `state/upload.ts`, parsing queries | Upload funnel |
| `frontend/app/state/analysisStore.ts` | Analysis lifecycle |
| `frontend/app/(app)/results/page.tsx` | Results view, export, share, clinician tab |
| `frontend/app/hooks/useHistory.ts`, `(app)/dashboard` or history UI | Repeat visit |
| `frontend/app/(app)/analysis/[id]/page.tsx` | Reopen |
| Backend: optional structured audit or metrics endpoint | Server-side truth |
| `docs/ops/*`, Privacy notice | Subprocessor + consent copy |

---

## 9. Recommendation (mandatory)

**SPLIT_INTO_EVENT_CONTRACT_AND_INSTRUMENTATION_PHASES**

**Named gaps to close in order:**

1. Event **naming** + data minimisation rules + **vendor or first-party** decision.  
2. **Consent** / Privacy notice alignment for analytics.  
3. FE (and optional BE) **instrumentation** for core funnel + results/clinician/export events.  
4. **Segment** model decision — new profile field vs questionnaire-derived vs deferred.  
5. **Paid conversion** — out of scope until billing; document **placeholder** or **manual** tracking.

---

## 10. References (non-exhaustive)

- `docs/HealthIQ_Phase1_Launch_Posture.md` §318–372  
- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` §163+  
- `docs/investigations/OPS_S1_PREFLIGHT.md` §3.5  
- `docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md`  
- `frontend/app/(app)/results/page.tsx` (export/share)  
- `frontend/app/state/analysisStore.ts` (console logging only)  
- `frontend/app/services/reports.ts` (service exists; verify production usage)  
