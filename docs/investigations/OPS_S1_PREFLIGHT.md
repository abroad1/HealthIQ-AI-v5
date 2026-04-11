# OPS-S1 Preflight — Phase 1 Operational Readiness for UK B2C Launch

**work_id:** OPS-S1-PREFLIGHT  
**mode:** READ_ONLY investigation  
**date:** 2026-04-10  
**launch authority:** `docs/HealthIQ_Phase1_Launch_Posture.md` (agreed UK-first B2C posture)  
**roadmap:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (Wave 6, OPS-S1)

---

## 1. Executive summary

### What operational-readiness capability already exists

- **Engineering pipeline:** GitHub Actions CI (e.g. `.github/workflows/ci.yml` — tests for backend/frontend), `golden_gate.yml`, `validate.yml` — deployment discipline exists at the **software delivery** layer.
- **Backend data model hooks:** SQLAlchemy models include GDPR-oriented fields and related tables (e.g. `Profile.consent_*`, relationships to `Consent`, `DeletionRequest`, `AuditLog` per `backend/core/models/database.py`) — **schema-level** readiness, not end-user or policy completion.
- **Auth stack (config):** Backend settings reference `DATABASE_URL`, Supabase (`backend/config/settings.py`, `backend/config/database.py`) — persistence and auth **can** be wired; region is **not** encoded in repo.
- **Product truth on results:** In-app copy in places distinguishes interpretation from diagnosis (e.g. results overall score card, `ClinicianReportRenderer` / `InsightsPanel` framing narrative as companion to structured truth) — aligns with **non-diagnostic** posture when users are inside the app.
- **Launch posture document:** `docs/HealthIQ_Phase1_Launch_Posture.md` is explicit on UK-only, B2C wedge, UK residency **direction**, UK consumer health-data **floor**, and lists minimum legal/security/governance **expectations** and **explicit non-goals** (e.g. HIPAA-led launch, ISO/SOC2 as hard dependencies — out for Phase 1 per that doc §305–314).

### What is still missing (high level)

- **Marketing/trust claims vs UK posture:** Launch-facing UI still uses **US-centric and strong assurance language** (HIPAA, “bank-level”) that the agreed Phase 1 posture explicitly de-emphasises for the UK floor — **claim/control mismatch**.
- **Legal surfaces:** Privacy, Terms, Contact are largely **`href="#"`** placeholders on landing and `(app)` footer — **no published policies** in product.
- **UK residency:** A **business decision** exists in the posture doc; **no repo-enforced or documented** UK-only hosting/subprocessor map ties production config to that decision.
- **Compliance artefacts:** No in-repo **DPIA**, **subprocessor inventory**, or **privacy notice** text aligned to UK GDPR / special-category health data — posture doc **requires** these as part of minimum baseline (§274–303), not yet evidenced as documents in-repo.
- **Wedge metrics:** Posture doc defines bridge metrics (§335–372); **no** product analytics layer (e.g. conversion, segment, report-download funnels) is evident in frontend application code from this audit — **measurement readiness** is largely **undefined in implementation**.

### Whether OPS-S1 is justified now

**Yes.** Roadmap OPS-S1 was blocked until market, residency, operating model, and compliance **floor** were decided; those inputs are now **explicitly recorded** in `docs/HealthIQ_Phase1_Launch_Posture.md` (§440–454). OPS-S1 can be scoped to **close the gap between that posture and observable product/ops reality**, without reopening strategy.

---

## 2. Strategy interpretation — what OPS-S1 is for (UK-first B2C)

**Source — roadmap §764–768:** OPS-S1 delivers **privacy, security, deployment, CI/CD, and operational controls** appropriate to the **intended launch markets**, verifies **controls for geography and product model**, and completes the **operational and governance checklist for first deployment**.

**Interpreted for agreed posture:**

| OPS-S1 intent | UK B2C meaning |
|---------------|----------------|
| Privacy / compliance | Align **user-facing claims**, **policies**, and **data practices** with **UK GDPR / DPA 2018** special-category handling and **non-diagnostic** positioning per posture doc §264–296. |
| Security / operations | Demonstrate **encryption, access control, logging, backup, incident response** as **operational commitments** where the posture requires them (§281–289) — evidenced by process + config, not only code stubs. |
| Deployment / CI/CD | Extend existing CI/CD to **release and environment** practices needed for a **creditable UK consumer launch** (secrets, env separation, production checklist). |
| Governance | **Data-flow documentation**, **vendor/subprocessor inventory**, **DPIA or equivalent** (posture §298–303) — artefact-led, not implied. |

**What OPS-S1 should unlock:** Permission to **market and operate** a UK B2C interpretation product without **obvious** trust/legal/ops contradictions between copy, hosting story, and minimum UK baseline.

**Explicitly not required for Phase 1** (per posture doc §305–314, 395–409): HIPAA-led baseline, ISO 27001 / SOC 2 as **hard** launch gates, medical-device positioning, B2B-primary launch, US-first/multi-market, enterprise-maximal compliance build-out.

**Separation:**

| Area | Relationship to OPS-S1 |
|------|-------------------------|
| **FE-LAUNCH-INTEGRATION** | **Done** — product shell and journey coherence; OPS-S1 does **not** redo FE integration except where **copy/legal links** require touch-ups. |
| **Backend reasoning / narrative** | **Out of scope** — analytical and Layer C contracts are separate workstreams. |
| **Future B2B / B2B2C** | **Out of scope** for Phase 1 floor; posture allows **parallel BD**, not launch-blocking enterprise controls. |
| **Future US / multi-market** | **Out of scope** — posture is **UK-only** first; OPS-S1 should not optimise for HIPAA-led ops as default. |

---

## 3. Current readiness audit (repo-evidenced)

### 3.1 Trust / claims surfaces

| Location | Evidence | Assessment |
|----------|----------|--------------|
| `frontend/app/page.tsx` | Hero strip: “HIPAA Compliant”, “Bank-Level Security”, “Instant Results” (approx. lines 69–80). Trust section: “Medical-Grade Security” with “HIPAA compliant with end-to-end encryption” (approx. 134–139). “Evidence-Based AI” / “Continuous Monitoring” with alerts copy (142–163). Hero: “clinician-grade report” (51). Footer: Privacy/Terms/Contact `href="#"` (196–198). | **High mismatch risk** for **UK-first** posture: HIPAA is **US** framework; posture doc states HIPAA-led launch is **not** Phase 1 floor. Strong security/medical claims are **not** backed by in-repo UK policy or UK-specific wording. Legal links are **non-functional**. |
| `frontend/app/components/layout/Footer.tsx` (app shell) | Privacy / Terms / Contact `href="#"` | Same — **no** policy routes. |
| `frontend/app/(auth)/login/page.tsx` | CardDescription: “Backend: FastAPI /api/auth.” | **Developer-oriented**; weak for consumer trust. |
| `frontend/app/(app)/results/page.tsx` | Structured interpretation, “not a clinical diagnosis” style lines in advanced tab; clinician tab label | **Generally consistent** with non-diagnostic framing **inside** the analysis experience. |
| `frontend/app/components/results/ClinicianReportRenderer.tsx` | Wording on co-ranked items / clinician discussion | **Supports** “discussion with clinician” without claiming device output — still needs **consistency** with landing claims. |

**Summary:** In-app analysis surfaces are **more careful** than **marketing** surfaces. The **largest operational risk** for UK B2C is **unsupported or jurisdictionally wrong trust claims** on the landing page and **stub legal links**.

### 3.2 Data handling / residency

| Topic | Repo evidence | Honest assessment |
|-------|---------------|-------------------|
| Where data lives | `DATABASE_URL`, Supabase-related env in `backend/config/settings.py`, `backend/config/database.py`; frontend `NEXT_PUBLIC_SUPABASE_*` references in config paths | **Vendor and connection-string driven** — **no** UK region flag or constraint in application code from this review. |
| “UK-hosted by default” | Stated in `docs/HealthIQ_Phase1_Launch_Posture.md` §238–257 | **Strategic** commitment; **not** proven by repo alone. Requires **deployment/docs** evidence (chosen Supabase project region, DB region, object storage region). |
| File upload | Upload flow parses files client-side / API — persistence via analysis pipeline | **Behaviour** exists; **residency** follows hosting choices, not code. |

### 3.3 Privacy / compliance artefacts

| Item | Present in repo? | Notes |
|------|-------------------|--------|
| Privacy notice (user-facing) | **No** — links are `#` | Required by posture §274–276. |
| Terms of use | **No** | Same. |
| Retention / deletion (user-visible) | **Not** as product copy | Schema suggests `deletion_requests` etc. (`Profile` model) — **implementation depth** not audited here; **policy text** absent from UX. |
| DPIA / privacy risk review | **No** dedicated doc found in `docs/` search | Posture §302 expects before launch. |
| Subprocessor / vendor inventory | **No** in `docs/` as standalone artefact | Posture §301. |
| Incident / security process | Sprint note `docs/sprints/SPRINT_11_TEST_ISOLATION_AND_SECURITY_VALIDATION.md` exists — **not** same as live **incident response** runbook for launch. |

### 3.4 Operational readiness

| Area | Evidence | Gap |
|------|----------|-----|
| CI/CD | `.github/workflows/*.yml` | Good **build/test** posture; **production** release/runbook not evidenced in this audit. |
| Support / contact | Footer “Contact” `#` | **No** operational support path. |
| Secrets / env | Backend `settings.py` validation patterns | **Pattern** exists; **production** secret handling is **environment** concern — should be in OPS scope as **checklist**. |
| Monitoring / alerting | Not surfaced in frontend; not deep-audited in infra | **Likely gap** for launch operations. |
| Backup / recovery | Mentioned as posture expectation §287 | **Not** verified as documented procedure in-repo. |

### 3.5 Wedge-metric instrumentation readiness

**Posture doc** (`docs/HealthIQ_Phase1_Launch_Posture.md` §335–372) requires defined metrics: paid conversion, repeat upload, retention, clinician report download/carry-through, segment splits, trust signals, etc.

**Repo check:** No dedicated **product analytics** integration (e.g. event SDK, billing events) was found in `frontend/app` via targeted search; **bridge metrics are not instrumented** in application code in a way that satisfies the posture’s measurement intent.

**Conclusion:** **Metric definition + governance** can sit in OPS-S1; **full implementation** may span OPS-S1 (minimum event contract + privacy alignment) and a **later product analytics** sprint — **split recommended** for execution, not for “whether to measure.”

---

## 4. Launch-critical gap ranking (UK B2C)

1. **Trust/marketing vs jurisdiction (HIPAA / bank-level / medical-grade on landing)** — Undermines UK posture and creates **regulatory/reputational** exposure if deployed as-is.  
2. **Absent Privacy / Terms / real Contact** — Minimum **transparency** for UK GDPR special-category processing is **not** met in the product shell.  
3. **No documented UK hosting / subprocessor story in-repo** — “UK-hosted by default” cannot be **demonstrated** to buyers or regulators from code alone.  
4. **Missing governance artefacts (DPIA, inventory, data-flow docs)** — Posture **requires** them as baseline; **not** present as documents in this repo survey.  
5. **Login/help copy** — Technical backend string and **no** help/support story for B2C.  
6. **Wedge metrics not wired** — Strategic success of B2C wedge **cannot** be validated without measurement design + privacy-compliant collection.  
7. **Operational runbooks / on-call / incident** — Implied gap vs posture §288–289.

---

## 5. Recommendation

### **SPLIT_INTO_TRUST_AND_OPERATIONAL_PHASES**

**Grounding:** Repo shows **strong product/engineering** progress and a **clear strategic posture document**, but **clusters of work** differ in nature: (A) **user-facing trust and UK-appropriate claims + legal surfaces + claims/copy alignment**; (B) **hosting/vendor evidence, operational controls, incident/backup, production readiness**; (C) **metrics** (definition + privacy-minimal instrumentation vs full analytics). Splitting keeps **governance auditable** and matches posture doc’s own split between **minimum floor** (§270–303) and **later** ISO/HIPAA/US (§305–314).

**If proceeding — likely shape:**

| Phase | Named gaps (examples) | Likely surfaces |
|-------|------------------------|-----------------|
| **Phase 1 — Trust & UK baseline** | Replace or qualify HIPAA/bank-level/medical-grade claims; add **Privacy** and **Terms** routes + content aligned to UK posture; real **Contact** path; align login copy; review results/marketing consistency for non-diagnostic framing | `frontend/app/page.tsx`, `Footer.tsx`, `(auth)/*`, new or linked `docs/legal/*` consumed by app, routing |
| **Phase 2 — Operations & evidence** | Subprocessor/DPIA/data-flow **artefacts**; document UK hosting choices; env/secrets checklist; incident/backup **runbook** references; extend CI/deploy docs as needed | `docs/ops/*`, deployment config, vendor docs, `backend` config review |
| **Metrics (spanning)** | Event taxonomy for wedge metrics; privacy assessment for analytics; implement vs defer heavy BI | Product + OPS agreement; frontend/backend instrumentation as scoped |

**Alternative:** **PROCEED_AS_ONE_BOUNDED_OPS_READINESS_SPRINT** only if programme insists on a **single audit gate** — acceptable if the **sprint prompt** explicitly lists **all** artefact types above with **STOP** if legal review is not engaged for copy/policy.

**Not recommended:** **DO_NOT_PROCEED_OPS_SCOPE_NOT_YET_GROUNDED** — Launch posture and roadmap inputs are now **sufficient** to scope OPS-S1; remaining work is **execution and documentation**, not unknown strategy.

---

## 6. Boundary check — out of scope for OPS-S1 (default)

Per posture doc and roadmap separation:

- Future **US** or **multi-market** compliance programme as **launch** dependency  
- **B2B procurement** / enterprise readiness as **Phase 1 gate**  
- **SOC 2 / ISO 27001 certification** as **mandatory** before UK B2C launch (posture: may be later)  
- **HIPAA-led** operational baseline as **default** (explicitly excluded for Phase 1 floor)  
- **Medical device** positioning  
- **Backend reasoning** or narrative **generation** changes  
- **Broad marketing-site redesign** beyond **trust/legal alignment and honesty**  
- **Enterprise admin/workspace**  
- **Speculative legal drafting** beyond what is needed to **name and fill** required artefacts (actual legal review is a **human** gate, not repo scope)

---

## 7. Required chat output mapping

| Deliverable | Section |
|-------------|---------|
| Executive summary | §1 |
| Strategy interpretation | §2 |
| Readiness audit | §3 |
| Gap ranking | §4 |
| Recommendation | §5 |
| Boundaries | §6 |

---

**Document status:** Preflight complete — OPS-S1 may be authored with `docs/HealthIQ_Phase1_Launch_Posture.md` as mandatory authority alongside this gap analysis.
