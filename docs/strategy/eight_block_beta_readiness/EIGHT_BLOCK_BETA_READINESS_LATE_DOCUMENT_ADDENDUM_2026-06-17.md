# Eight-Block Beta Readiness — Late Document Addendum

**Date:** 2026-06-17  
**Purpose:** Record authority documents discovered **after** the original eight-block estate audits (2026-06-17)  
**Does not:** Rerun the estate audit or rewrite original Cursor/Claude findings  
**Companion:** `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md`

---

## 1. Executive summary

The original eight-block audits remain **valid**. Late discovery changes **authority ranking and framing**, not core estate conclusions.

**No full re-audit is required** unless a formal line-by-line Cursor vs Claude comparison is requested.

**Next steps (per programme decision):**
1. Layer authority index r2 ✅ (this addendum's companion)
2. This addendum ✅
3. Layer-boundary reconciliation ADR (pending)
4. Cursor/Claude comparison and multi-sprint programme (pending)

---

## 2. Missed documents

| Document | Path | Why missed |
|----------|------|------------|
| **Strategic Vision v1.5 FINAL ADOPTED** | `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | Not in original search terms (focused on Layer B/C contracts, Pass 3, runtime paths); cited only indirectly via `AUTHORITY_MAP` |
| **FE Visualisation Surface Policy (v1 fresh)** | `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Proposal_v1_fresh.md` | Archive/draft path; not in `AUTHORITY_MAP`; audit searched Results Journey v6 and FE-R audits instead |
| **Strategic Vision v1.4 amended** | `docs/archive/superseded/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` | Superseded; not required for layer authority |
| **Strategic Vision v1.3 (no suffix)** | `docs/archive/superseded/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` | Superseded; not required for layer authority |

---

## 3. Classification

| Document | Status | Layer / block relevance |
|----------|--------|-------------------------|
| v1.5 FINAL ADOPTED §2.3 | **AUTHORITATIVE** (`AUTHORITY_MAP`) | **All blocks** — especially 3 (Layer B), 4 (Layer C), 5 (UX philosophy) |
| v1.5 First Market Addendum | **AUTHORITATIVE** (read with parent) | Strategy context — not layer-defining |
| v1.4 amended | **SUPERSEDED** | Historical sprint roadmap — **no** full §2.3 |
| v1.3 (archive) | **SUPERSEDED** | Historical — **no** full §2.3 |
| FE Surface Policy Proposal v1 fresh | **Draft, not in AUTHORITY_MAP** | **Block 5** supporting UX policy only |
| FE Surface Policy Final v3 | **SUPPORTING** (`AUTHORITY_MAP`) | Block 5 historical context |

---

## 4. AUTHORITY_MAP confirmations

| Document | In AUTHORITY_MAP? | Status |
|----------|-------------------|--------|
| `HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | **Yes** | **AUTHORITATIVE** — Master strategic record |
| `HealthIQ_FE_VISUALISATION_Surface_Policy_Proposal_v1_fresh.md` | **No** | Not listed |
| `HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` | **Yes** | **SUPPORTING** — Historical surface policy |

---

## 5. Do original audit conclusions change?

### Unchanged (core estate verdict)

```text
- Not externally beta-ready
- Layer B estate is real
- Layer B owns WHY / surfacing / medical logic (strategic + product boundary)
- Layer C is presentation / translation only (strategic north star)
- Gemini narrative remains inactive
- 3 of 6 launch domains currently implemented on consumer cards
- Boilerplate / prose coverage incomplete
- Test estate exists; beta gates distributed not consolidated
- Pass 3 not read at runtime; promotion pipeline incomplete
- Reconciling ADR still needed for Layer C naming drift
```

### Strengthened

| Conclusion | Strengthened by |
|------------|-----------------|
| Layer B owns signals, WHY, root-cause, clinician reporting | v1.5 §2.3 explicit list inside Layer B |
| Layer C must not become analytical engine | v1.5 §2.3: "translates governed truth; does not invent or replace it" |
| Do not treat UX polish as substitute for Layer B | v1.5 §2.3 anti-drift paragraph; FE proposal §1 "engine output becomes product reality" |
| Frontend render-only / tiered disclosure | FE proposal §6 — aligns with ADR-007, launch estate gate |
| Educational content separate from personalised interpretation | FE proposal §9 — aligns with RETAIL_EXPLAINER, IDL Design Lock |

### Not overturned

| Original finding | Still true |
|------------------|------------|
| 3/6 launch domains on cards | Yes |
| MED-REV-1 subsystem collapse | Yes — **tensions** with FE proposal "show systems" |
| Gemini inactive for narrative | Yes |
| `NarrativePayloadV1` is handoff contract | Yes — now sits under v1.5 §2.3 strategically |
| Full eight-block re-audit unnecessary | **Confirmed** |

---

## 6. Recommendations reordered

| Priority | Was (implicit in audits) | Now (after r2) |
|----------|--------------------------|----------------|
| 1 | Map Layer B estate | **Adopt v1.5 §2.3 as strategic north star** + patch authority index |
| 2 | ADR_WP2 / NarrativePayload | Unchanged — tier 3–4 in r2 stack |
| 3 | Reconciling ADR | **Elevated** — still required before Gemini sprint |
| 4 | UX retail polish | **Deprioritised** vs Layer B / reconciliation — FE proposal supports this |
| 5 | Full estate re-audit | **Removed** — not recommended |

---

## 7. Block-by-block impact (late docs only)

| Block | Impact |
|-------|--------|
| 1 Systems | v1.5 reinforces phenotype-aware systems ambition — no count change |
| 2 Subsystems | FE proposal tensions with MED-REV-1 — **document, don't resolve here** |
| 3 Layer B | **Strengthened** by v1.5 §2.3 |
| 4 Layer C / Gemini | **Strengthened** — v1.5 confirms C is translation/presentation only |
| 5 UX | FE proposal **supporting** for tiered disclosure; does not override UAT findings |
| 6–8 | No material change |

---

## 8. Full re-audit recommendation

**Not recommended.**

Sufficient to:
- Use r2 layer index
- Write reconciling ADR
- Proceed to multi-sprint programme

**Optional later:** Formal Cursor vs Claude eight-block line-by-line comparison (separate exercise).

---

## 9. Pointers

| Original report | Post-audit note |
|-----------------|-----------------|
| `EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md` | See this addendum + `LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` |
| `EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md` | See this addendum + `LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` |
| `LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17.md` (r1) | Superseded for **ranking only** by r2; r1 retained as historical record |

---

*End of addendum — 2026-06-17.*
