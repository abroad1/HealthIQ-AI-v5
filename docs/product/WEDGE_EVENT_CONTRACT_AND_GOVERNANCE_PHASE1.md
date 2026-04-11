# Wedge event contract & governance — Phase 1 (WEDGE-METRICS-A)

**Status:** Launch-bounded measurement contract — internal governance  
**Sprint:** WEDGE-METRICS-A (definition); WEDGE-METRICS-B (first-party instrumentation live — see §11)  
**Next:** Retention policy for event logs; legal/privacy sign-off before broad prod use (see §6)  

**Authority:** `docs/investigations/WEDGE_METRICS_PREFLIGHT.md`, `docs/HealthIQ_Phase1_Launch_Posture.md` §318–372, `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md` §163+, `docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md`.

---

## 1. Stage 1C — preflight verification (record)

| Assertion | Verified |
|-----------|----------|
| Governing preflight | `docs/investigations/WEDGE_METRICS_PREFLIGHT.md` recommends split contract vs instrumentation; documents missing SDK, no billing, ambiguous clinician “download”. |
| Launch authority | Posture doc defines bridge metrics and B2C wedge proof; addendum sequences Sprint 3 wedge metrics. |
| Repo reality | No product analytics SDK in `frontend/app/`; `analysisStore` uses `console.*` only; `reports.ts` uses `API_BASE_URL = 'about:blank'` — server report download **not** live; results page has JSON export + URL share, not a single “PDF clinician download”. |
| Journeys to cover (initial contract) | Registration → login → upload/parse → questionnaire → analysis → results (incl. clinician report **view**) → export/share → history reopen. |
| This sprint does **not** wire events or add SDKs | **Confirmed** — documentation and manifest only. |

---

## 2. Event vocabulary (Phase 1)

**Naming:** Prefix `wedge_`, `snake_case`, past-tense action where the event fires **after** the action completes (except `*_started`).

| Event name | Fires when | Notes |
|------------|------------|--------|
| `wedge_auth_register_completed` | Account creation succeeds (user can proceed). | No payload health data. |
| `wedge_auth_register_failed` | Registration fails (validation or API error). | Include **error_class** only (e.g. `validation`, `api_4xx`), not message text with PII. |
| `wedge_auth_login_success` | Login succeeds. | |
| `wedge_auth_login_failed` | Login fails. | **error_class** only. |
| `wedge_upload_started` | User initiates file or paste upload path (first byte / parse request). | Distinguish `source`: `file` \| `paste`. |
| `wedge_upload_parse_completed` | Parsed table / biomarkers confirmed available for next step. | |
| `wedge_upload_parse_failed` | Parse fails. | No raw file contents in payload. |
| `wedge_questionnaire_submitted` | Questionnaire step submitted before analysis run. | **No** questionnaire answers in analytics payload (see §4). |
| `wedge_analysis_started` | Client calls `startAnalysis` / pipeline begins for a run. | May include `analysis_id` once created (UUID only). |
| `wedge_analysis_completed` | Analysis succeeds and results available to UI. | |
| `wedge_analysis_failed` | Analysis fails. | **error_class** or coarse code only. |
| `wedge_results_viewed` | Results route shows completed analysis (first paint with data). | Include `entry`: `fresh` \| `from_url` \| `from_history`. |
| `wedge_clinician_report_viewed` | User opens **clinician report** presentation (e.g. tab focus, section expand) where `ClinicianReportRenderer` content is shown. | **Not** fired for JSON export or share. |
| `wedge_results_export_json_clicked` | User triggers **client-side JSON export** of analysis (`handleExportResults` in `frontend/app/(app)/results/page.tsx`). | This is **full analysis JSON**, not a dedicated “clinician PDF”. |
| `wedge_results_share_link_clicked` | User triggers share or copy **URL** to current results (`handleShareResults`). | |
| `wedge_analysis_reopened_from_history` | User opens a **saved** analysis via history list or deep link (`/results?analysis_id=` / analysis redirect). | Distinct from first-time `wedge_results_viewed` if implementation can distinguish. |

**Deferred (not honest to emit until product supports):**

| Deferred name | Why deferred |
|---------------|----------------|
| `wedge_clinician_report_pdf_downloaded` | No live server PDF/download path wired; `ReportsService` backend routes disabled (`about:blank` base). **Do not** map JSON export to this event. |
| `wedge_paid_conversion` | No billing/checkout in app — **blocked** (see §8). |
| `wedge_user_segment_assigned` | No persisted standard-vs-biohacker dimension — **blocked** until product defines capture. |

Machine-readable list: `docs/product/wedge_events_phase1.manifest.json`.

---

## 3. Event semantics — ambiguous actions (resolved)

| Ambiguous phrase | Resolution |
|------------------|------------|
| “Clinician report download” (posture language) | **Split:** (1) **In-app view** → `wedge_clinician_report_viewed`. (2) **Client JSON export** of full analysis → `wedge_results_export_json_clicked` (not relabelled as clinician PDF). (3) **Share URL** → `wedge_results_share_link_clicked`. (4) **Future PDF** → `wedge_clinician_report_pdf_downloaded` **deferred**. |
| “Download” vs “export” | Use **export_json** in the event name for the current behaviour to avoid HIPAA/marketing-style mislabeling. |
| “Results viewed” vs “reopened” | `wedge_results_viewed` for any results screen load with data; optional property `entry` distinguishes first load vs reopen if instrumented. |
| Repeat upload / repeat panel | **Prefer server-side aggregation** (count analyses per `user_id` over time) for “repeat” KPIs; optional client `wedge_analysis_started` with `is_repeat_panel: boolean` **only after** product defines “repeat” (same user, new upload). Not required for minimal contract. |

---

## 4. Payload minimisation rules (Phase 1)

### 4.1 Allowed (coarse)

- `event_name`, ISO `timestamp`, environment (`env`: `development` \| `staging` \| `production`).
- **Identifiers:** hashed `user_id` or opaque `analytics_subject_id` tied to auth; **never** email in third-party payloads.
- **Routing:** `route` path (e.g. `/results`), **no** query strings containing tokens.
- **IDs:** `analysis_id` as UUID string only (no biomarker payloads).
- **Enumerations:** `entry`, `source`, `error_class`, `phase` (coarse pipeline phase).

### 4.2 Prohibited

- Raw biomarker values, lab text, file contents.
- Questionnaire free-text or structured health answers.
- Clinician report narrative body, insight text, cluster detail.
- JWT, refresh tokens, passwords.
- Precise geolocation.

### 4.3 Segmentation

- **Do not** send inferred “retail vs biohacker” until product stores a **consented** segment field. Until then: **defer** segment-split analytics or use **proxy** (e.g. manual cohort study).

---

## 5. Analytics collection posture

**Decision for Phase 1 implementation (WEDGE-METRICS-B):**

| Layer | Posture |
|-------|---------|
| **Preferred** | **First-party** collection: browser → HealthIQ **backend** endpoint → append-only store or DB table with retention policy. Aligns with UK posture and keeps subprocessors minimal. |
| **Third-party** (e.g. product analytics SaaS) | **Permitted only after:** privacy/legal review, vendor DPA, update to `docs/ops/VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md`, Privacy notice disclosure, and (if non-essential) **consent** pattern per ePrivacy/GDPR practice. |
| **Hybrid** | Acceptable if **identical event names** and **minimised payloads** are enforced in a single client library; third-party receives **no** additional health content beyond first-party rules. |

**Explicit:** Vendor choice may still be **open** at end of WEDGE-METRICS-A; WEDGE-METRICS-B must **not** integrate a vendor until the above gates are satisfied.

---

## 6. Privacy / consent / policy prerequisites (before instrumentation)

| Item | Status |
|------|--------|
| Privacy notice mentions analytics / optional cookies or similar | **Must be reviewed** before third-party scripts or non-essential tracking. |
| Essential vs non-essential analytics | **Legal review** — first-party operational metrics may be framed differently from marketing analytics. |
| Subprocessor inventory | **Update required** if new analytics vendor processes personal data. |
| Consent banner / CMP | **Review** if non-essential tracking or cross-site cookies. |
| Data retention for event logs | **Define** (e.g. 90-day rolling) before production logging. |

**Can do now:** Finalise this contract, implement first-party endpoint design in WEDGE-METRICS-B.  
**Must review before prod instrumentation:** Legal/privacy on notice + consent.  
**Deferred:** Full DPO sign-off process (org-dependent).

---

## 7. Metric classification (now / proxy / later)

| Metric (posture / strategy) | Classification | Notes |
|-----------------------------|----------------|--------|
| Paid conversion | **Later / blocked** | No payment integration — track **placeholder** or manual spreadsheet until billing exists. |
| Repeat upload / repeat panel | **Proxy → then measurable** | **Proxy:** SQL/dashboard on `Analysis` rows per user. **Event:** optional after repeat definition. |
| Retention / return usage | **Proxy → measurable** | **Proxy:** return logins via sessions/DB. **Event:** `wedge_auth_login_success` with day bucket. |
| Clinician report usage | **Measurable (bounded)** | `wedge_clinician_report_viewed` + export/share events; PDF metric **deferred**. |
| Clinician carry-through / discussed with clinician | **Definitional / later** | Requires **survey** or research — not a single product event. |
| Segment differences | **Later** | No segment field — **do not fabricate**. |
| Trust / usefulness | **Later / definitional** | In-app rating or survey — separate instrument. |
| Enterprise-relevant proof | **Later** | Narrative + usage exports for GTM, not automatic events. |
| Registration / login / funnel | **Measurable (bounded)** | Core event list above. |

---

## 8. Handoff — WEDGE-METRICS-B

### 8.1 Likely surfaces (no code changes in WEDGE-METRICS-A)

- `frontend/app/state/authStore.ts` — register/login success/failure  
- `frontend/app/(auth)/login/page.tsx`, `register/page.tsx`  
- `frontend/app/(app)/upload/page.tsx`, `state/upload.ts`, parsing hooks  
- `frontend/app/state/analysisStore.ts` — analysis lifecycle  
- `frontend/app/(app)/results/page.tsx` — results, export, share, clinician tab  
- `frontend/app/hooks/useHistory.ts`, dashboard/history UI  
- `frontend/app/(app)/analysis/[id]/page.tsx` — reopen redirect  
- **Backend (optional):** first-party `POST /api/.../events` + storage, or structured audit stream (must not mix with Intelligence Core reasoning).  

### 8.2 Wire these event names

Use **`wedge_events_phase1.manifest.json`** + §2 table. **Do not** emit deferred events without product support.

### 8.3 Payload rules

Follow §4; enforce in client helper + server validation.

### 8.4 Excluded

- Raw health content, biomarkers, questionnaire answers in events.  
- Third-party SDK loading without inventory + notice updates.  

### 8.5 Open items

- Choose first-party endpoint schema vs vendor.  
- Legal review of Privacy notice + consent.  
- Define “repeat panel” for optional boolean.  
- Segment field — future schema change.  
- Billing — future sprint.  

---

## 9. Validation

- **WEDGE-METRICS-A:** governance artefacts + bounded contract test (`frontend/tests/integration/wedge-metrics-a-event-contract.test.ts`).  
- **WEDGE-METRICS-B:** instrumentation + `frontend/tests/integration/wedge-metrics-b-instrumentation.test.ts` + `backend/tests/unit/test_wedge_events_api.py`.  
- WEDGE-METRICS-B does **not** change Intelligence Core / scoring / analysis reasoning — only first-party event receipt and client emission.

---

## 10. Implementation status (WEDGE-METRICS-B)

**Collection path:** Browser → `POST /api/wedge-events` → structured log line (`healthiq.wedge_events` logger), optional `user_sub` when a valid Bearer JWT is sent. Client helper: `frontend/app/lib/wedgeAnalytics.ts`. Disable client emission in any environment: `NEXT_PUBLIC_WEDGE_EVENTS_DISABLED=1`.

**Live events:** Matches `event_names` in `docs/product/wedge_events_phase1.manifest.json` (names validated server-side in `backend/app/routes/wedge_events.py`).

**Surfaces (indicative):** `authStore` (login/register), `upload/page.tsx` (upload/parse/questionnaire), `analysisStore` (analysis lifecycle), `results/page.tsx` (view/export/share/clinician tab), `analysis/[id]/page.tsx` (reopen from history).

**Explicitly deferred (not emitted as live):** `deferred_event_names` in the manifest; also `wedge_paid_conversion`, segment split, clinician carry-through, and trust surveys — per §2 and §7 — are not wired.

**Operational note:** Payloads are minimised per §4; no biomarker values, questionnaire answers, or report narrative in events.

---

## 11. Revision

Bump `contract_version` in `wedge_events_phase1.manifest.json` when event names or semantics change.
