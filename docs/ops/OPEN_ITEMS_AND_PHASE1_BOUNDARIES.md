# Open items and Phase 1 boundaries (OPS-S1B)

**Purpose:** Make **gaps explicit** so documentation does not imply false completeness. Aligns with launch posture: Phase 1 is a **credible baseline**, not enterprise-maximal compliance.

---

## 1. What OPS-S1B **did** deliver (in-repo)

| Area | Delivered artefact |
|------|-------------------|
| UK hosting / residency honesty | `docs/ops/UK_HOSTING_AND_RESIDENCY_PHASE1.md` |
| Vendor / subprocessor inventory | `docs/ops/VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md` |
| Privacy risk review (structured) | `docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md` |
| Data flow | `docs/compliance/DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md` |
| Operational controls baseline | `docs/ops/OPERATIONAL_CONTROLS_BASELINE_PHASE1.md` |
| Wedge metrics note | `docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md` |

User-facing legal surfaces (Privacy, Terms, Contact) were **OPS-S1A**; not reworked here.

---

## 2. What remains **outside** Phase 1 scope (explicit)

| Item | Reason |
|------|--------|
| SOC 2 / ISO 27001 certification programme | Excluded as Phase 1 hard dependency per launch posture |
| HIPAA-led operational baseline | UK-first posture; not default |
| Full product analytics implementation | Deferred; see wedge metrics note |
| Infrastructure replatforming | OPS-S1B is evidence, not rebuild |
| Substituting documents for **legal** sign-off | Documents support decisions; counsel still required |

---

## 3. Open dependencies (non-repo completion required)

| Dependency | Owner | Notes |
|------------|-------|--------|
| **Prove** production UK / EEA / acceptable routing for Supabase + hosting + Gemini | Ops + Legal | Console exports, DPAs, IDTAs as needed |
| **Production** backup RPO/RTO and tested restore | Ops | Not verifiable from code |
| **Incident** playbooks and tabletop | Ops + Security | |
| **Legal** basis and Privacy notice final text | Legal | Schema supports consent — wording is legal |
| **Named DPO / privacy lead** if required | Org | Posture expects accountability |
| **Monitoring and on-call** for production | Ops | Mentioned as gap in preflight |

---

## 4. Distinction key

| Label | Meaning |
|-------|---------|
| **Completed in repo** | Artefact exists under `docs/ops/` or `docs/compliance/` from OPS-S1B |
| **Documented requirement** | Stated as expectation in posture or this pack |
| **Operational dependency** | Requires human action, vendor console, or legal — **not** done by merging docs |

---

## 5. When to refresh

Update this file when: vendors change, regions change, or Phase 2 scope is defined.
