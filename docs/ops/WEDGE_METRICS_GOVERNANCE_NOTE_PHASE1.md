# Wedge metrics — governance note (Phase 1)

**Purpose:** Record that **bridge metrics** in `docs/HealthIQ_Phase1_Launch_Posture.md` §335–372 are **strategically required** but **not fully instrumented** by OPS-S1B.

---

## 1. Position

- **Governance:** Metrics (conversion, repeat upload, retention, clinician report download, trust signals, etc.) should be **owned** by product and ops with **privacy-by-design** when instrumentation is added.
- **Scope:** OPS-S1B does **not** implement product analytics pipelines, billing hooks, or full event schemas.

---

## 2. Deferred work (typical next steps)

- Define **minimum event contract** (what to log, where, retention).
- Align with Privacy notice and consent for **non-essential** analytics if any.
- Choose tooling (first-party vs third-party) with **subprocessor** update to inventory.

---

## 3. Honesty

Absence of full instrumentation in the repo is **not** hidden: see `docs/investigations/OPS_S1_PREFLIGHT.md` §3.5.
