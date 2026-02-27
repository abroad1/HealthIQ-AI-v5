# HealthIQ v5.2 — Single Source of Truth Navigation

**Open this document first.** It tells you what governs the project, what sprint we're on, and what to ignore.

---

## Authoritative Baseline

This README is the required entry-point to the authoritative baseline set.

For v5.2 execution, the three baseline documents below are authoritative:

| Document | Purpose |
|----------|---------|
| [Master_PRD_v5.2.md](./Master_PRD_v5.2.md) | Constitutional document — defines *what* we build |
| [Delivery_Sprint_Plan_v5.2.md](./Delivery_Sprint_Plan_v5.2.md) | Sprint sequencing and implementation order |
| [architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md](./architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md) | Analytical assets inventory and SSOT alignment |

All sprint execution and implementation must reference these documents explicitly.

---

## Current Sprint

**Sprint 11 complete (v5.2 Phase 2 complete).**

Execution sequencing authority:

- `docs/Delivery_Sprint_Plan_v5.2.md`
- `docs/MASTER_ROADMAP_v5.2_to_v5.3.md`

## Completed Sprints (v5.2 to date)

- Sprint 1-3: Unit registry, lab-origin metadata, criticality/missing-data confidence
- Sprint 4-6: Ratio registry/centralisation and cluster schema refactor
- Sprint 7-8: InsightGraph boundary hardening and confidence contract freeze
- Sprint 9-11: ReplayManifest + deterministic replay stamps, RelationshipRegistry_v1, BiomarkerContext_v1

Latest stable savepoint tags present:

- `v5.2-p2-sprint10-stable`
- `v5.2-p2-sprint11-stable`

## Next Up (Depth-Oriented v5.2 Priorities)

1. Move remaining scoring policy thresholds/weights into SSOT so inference policy is fully versioned and auditable.
2. Converge runtime clustering to one production path and quarantine inactive engines from production execution.
3. Standardise deterministic failure artifacts so failed runs remain replay-compatible and governance-safe.

---

## How to Continue in a New Chat Window

**For ChatGPT / Cursor:**

1. **Always open this file first:** `docs/README_V5.2_BASELINE.md`
2. **Then read in order:**
   - `docs/Master_PRD_v5.2.md`
   - `docs/Delivery_Sprint_Plan_v5.2.md`
   - `docs/architecture/ANALYTICAL_ASSETS_INVENTORY_v5.2.md`
3. Use those documents as the authoritative baseline for all decisions and implementation.

---

## Deprecated / Historical Docs

The following documents are **NOT authoritative** for v5.2 execution. Do not use them for sprint planning or implementation decisions:

| Document | Reason |
|----------|--------|
| `docs/context/PRD.md` | Older PRD; superseded by `Master_PRD_v5.2.md` |
| `docs/context/ROADMAP.md` | Legacy roadmap; superseded by `Delivery_Sprint_Plan_v5.2.md` |
| `docs/sprint_plan_canonization_refactor.md` | One-off refactor plan; not current sprint authority |
| `docs/ARCHITECTURE_REVIEW_REPORT.md` | Synthesis report; not the v5.2 baseline |
| `docs/ARCHITECTURE_INSIGHT_MODULARITY_REVIEW.md` | Older architecture review |
| `docs/context/IMPLEMENTATION_PLAN_V5.md` | Superseded by Delivery_Sprint_Plan_v5.2 |
| `docs/context/IMPLEMENTATION_BLUEPRINT.md` | Superseded by v5.2 docs |
| `docs/sprint_1_2_fix_plan.md` | Historical fix plan |
| `docs/architecture/PHASE_0_AS_IS_ARCHITECTURE_AUDIT.md` | Phase 0 audit; not sprint authority |
| Synthesized technical architecture (`.pdf`, `.docx`) | Do not use for planning |

These files remain in `/docs` for historical reference only.
