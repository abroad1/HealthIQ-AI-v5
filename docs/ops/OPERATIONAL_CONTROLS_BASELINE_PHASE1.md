# Operational controls baseline — Phase 1

**Purpose:** Minimum **documented expectations** for running HealthIQ in production, aligned with `docs/HealthIQ_Phase1_Launch_Posture.md` §281–289.  
**Not:** A certified ISMS or full SOC 2 control matrix.

Each section separates: **implemented in product**, **process expectation**, **open / human dependency**.

---

## 1. Incident response (security & privacy)

| Aspect | Status | Notes |
|--------|--------|--------|
| **Detect** | Partial | CI and tests reduce defect risk; **production** detection needs monitoring/alerting — **not fully specified in repo** |
| **Contain** | Process | Expect runbook: rotate keys, disable accounts, block traffic — **document owner: ops** |
| **Eradicate / recover** | Process | Patch, redeploy, restore from backup per §3 |
| **Notify** | Legal/process | UK ICO breach notification rules if applicable — **legal owns thresholds** |
| **User notification** | Process | Align with Privacy notice commitments |

**Open:** Written **playbook** with roles and escalation paths; tabletop exercise before public launch.

---

## 2. Backup and recovery

| Aspect | Status | Notes |
|--------|--------|--------|
| **Code / branching backup** | Documented elsewhere | e.g. `docs/context/BACKUP_STRATEGY.md` — **source code**, not production DB |
| **Production database backup** | **Ops dependency** | Must follow Supabase / DB provider backup settings; **RPO/RTO targets** to be stated by ops |
| **Restore testing** | **Open** | Periodic restore drill not evidenced in-repo |

**Open:** Single-page **production** backup policy: frequency, retention, restore drill cadence, owner.

---

## 3. Secrets and configuration

| Aspect | Status | Notes |
|--------|--------|--------|
| **Pattern** | In code | Secrets from env (`SECRET_KEY`, `DATABASE_URL`, `SUPABASE_*`, `GEMINI_*`, etc.) |
| **Production practice** | **Ops dependency** | No secrets in git; use vault/CI secrets; rotation policy |

**Open:** Secret **rotation** schedule and break-glass procedure.

---

## 4. Access control

| Aspect | Status | Notes |
|--------|--------|--------|
| **End users** | Product | JWT-based access; users see own data |
| **Admin / support** | **Open** | Role-based admin access to production data must be **minimal**, logged, and documented |
| **Engineering access** | **Open** | Who can deploy, who can read prod logs — **least privilege** |

**Open:** Access review **cadence** (e.g. quarterly).

---

## 5. Vulnerability management

| Aspect | Status | Notes |
|--------|--------|--------|
| **Dependencies** | Partial | Repo uses standard package managers; **Dependabot / renovate** policy is org-level |
| **Patch SLAs** | **Open** | Define critical vs non-critical patch windows |

---

## 6. Launch-day operational checklist (minimal)

Use as a **starting template**; customise per environment.

- [ ] Production env vars set; no test keys in prod
- [ ] Supabase project region and DPA confirmed against UK posture intent
- [ ] Gemini / Google processing settings reviewed for health-adjacent data
- [ ] Backup enabled; restore drill scheduled
- [ ] Monitoring/alerting on API errors and auth anomalies (minimum)
- [ ] Incident contacts and escalation list published internally
- [ ] Privacy / Terms / Contact routes live and accurate (OPS-S1A)
- [ ] Legal/privacy sign-off on external claims

---

## 7. Relation to other docs

- Hosting honesty: `UK_HOSTING_AND_RESIDENCY_PHASE1.md`
- Vendors: `VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md`
- Privacy risks: `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md`
